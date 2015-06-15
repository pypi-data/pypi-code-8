"""
BDO
"""

import libspg


class BDOMessage(libspg.Message):

    @classmethod
    def from_xml(cls, element):
        # Get the message command name
        msg_cmd = libspg.QName(element.find('messageContent')[0][0]).localname

        # Get the message class from the command name
        msg_cls = globals().get(msg_cmd, None)

        if not msg_cls:
            raise NotImplementedError(
                'Message type not implemented: "{0}"'.format(msg_cmd))

        return msg_cls.from_xml(element)


#
# BDOtoBDR
#

class BDOtoBDR(BDOMessage):
    def __call__(self):
        element = super(BDOtoBDR, self).__call__()

        return libspg.E.BDOMessage(
            element.find('messageHeader'),
            libspg.E.messageContent(
                libspg.E.BDOtoBDR(
                    libspg.E(self.tag, *element.find('messageContent'))
                )
            )
        )

    @classmethod
    def from_xml(cls, element):
        message_header = element.find('messageHeader')
        message_content = \
            element.find('messageContent').find('BDOtoBDR').find(cls.__name__)

        return cls(message_header, message_content)


class SVQueryRequest(BDOtoBDR):
    """Pedido de Consulta de SV"""

    message_content = libspg.Instance(
        'messageContent', cls=libspg.SubscriptionVersionQueryRequestData)


class QueryBdoSVsReply(BDOtoBDR):
    """Resposta de Consulta dos SVs pela BDO"""

    message_content = libspg.InstanceList(
        'messageContent', blank=True, inner_tag='subscription_version',
        cls=libspg.SubscriptionVersionData)


class DownloadReply(BDOtoBDR):
    """Resposta a mensagem de Download"""

    message_content = \
        libspg.Instance('messageContent', cls=libspg.DownloadReply)


#
# BDRtoBDO
#

class BDRtoBDO(BDOMessage):
    def __call__(self):
        element = super(BDRtoBDO, self).__call__()

        return libspg.E.BDOMessage(
            element.find('messageHeader'),
            libspg.E.messageContent(
                libspg.E.BDRtoBDO(
                    libspg.E(self.tag, *element.find('messageContent'))
                )
            )
        )

    @classmethod
    def from_xml(cls, element):
        message_header = element.find('messageHeader')
        message_content = \
            element.find('messageContent').find('BDRtoBDO').find(cls.__name__)

        return cls(message_header, message_content)


class SVQueryReply(BDRtoBDO):
    """Resposta de Consulta de SV"""

    message_content = libspg.Instance(
        'messageContent', cls=libspg.SubscriptionVersionQueryReplyData)


class SVCreateDownload(BDRtoBDO):
    """Criar o Download de SV"""

    message_content = \
        libspg.Instance('messageContent', cls=libspg.SubscriptionVersionData)

    def reply(self, status=True, error_info=None):

        if status:
            version_id = \
                self.message_content.subscription_tn_version_id.version_id
            reply = libspg.DownloadReply(
                status='success',
                bdo_completion_ts=libspg.BdoCompletionTS(
                    version_id=version_id,
                    completion_ts=libspg.datetime.utcnow(),
                    download_reason='new'
                )
            )

        else:
            reply = libspg.DownloadReply(
                status='failed',
                error_info=error_info
            )

        return DownloadReply(
            libspg.MessageHeader(
                service_prov_id=self.service_prov_id,
                invoke_id=self.invoke_id,
                message_date_time=libspg.datetime.utcnow()
            ),
            reply
        )


class SVDeleteDownload(BDRtoBDO):
    """Excluir Download do SV"""

    message_content = libspg.Instance(
        'messageContent', cls=libspg.SubscriptionVersionDeleteData)

    def reply(self, status=True, error_info=None):

        if status:
            reply = libspg.DownloadReply(
                status='success',
                bdo_completion_ts=libspg.BdoCompletionTS(
                    version_id=self.message_content.subscription_version_id,
                    completion_ts=libspg.datetime.utcnow(),
                    download_reason='delete'
                )
            )

        else:
            reply = libspg.DownloadReply(
                status='failed',
                error_info=error_info
            )

        return DownloadReply(
            libspg.MessageHeader(
                service_prov_id=self.service_prov_id,
                invoke_id=self.invoke_id,
                message_date_time=libspg.datetime.utcnow()
            ),
            reply
        )


class QueryBdoSVs(BDRtoBDO):
    """Consulta de SVs da BDO"""

    message_content = \
        libspg.Instance('messageContent', cls=libspg.QueryBdoSVsData)

    def reply(self, sv_list):
        return QueryBdoSVsReply(
            libspg.MessageHeader(
                service_prov_id=self.service_prov_id,
                invoke_id=self.invoke_id,
                message_date_time=libspg.datetime.utcnow()
            ),
            sv_list
        )


class BDRError(BDRtoBDO):
    """Erro da BDR"""

    message_content = libspg.Instance('messageContent', cls=libspg.ErrorData)
