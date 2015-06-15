"""
libspg - Python library for interacting with Brazil NPAC SPG


Copyright (c) 2013 Andre Sencioles Vitorio Oliveira <andre@bcp.net.br>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""

__title__ = 'libspg'
__summary__ = 'Python library for interacting with Brazil NPAC SPG'
__url__ = 'http://bitbucket.org/asenci/libspg'

__version__ = '0.2'

__author__ = 'Andre Sencioles Vitorio Oliveira'
__email__ = 'andre@bcp.net.br'

__license__ = 'ISC License'


from datetime import datetime
from lxml import etree
from lxml.builder import ElementMaker

import os
import re


#
# Variables
#

LNP_URI = 'urn:brazil:lnp:1.0'
LNP_NSMAP = {None: LNP_URI, 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}


#
# XML
#

class ElementBase(etree.ElementBase):

    def __str__(self):
        return self.to_string(self)

    def __unicode__(self):
        return str(self).decode('utf-8')

    def find(self, path, namespaces=None):
        if isinstance(path, (str, unicode)) and path[0] not in ['{', '/', '.']:
            path = QName(LNP_URI, path)

        return super(ElementBase, self).find(path, namespaces)

    def findall(self, path, namespaces=None):
        if isinstance(path, (str, unicode)) and path[0] not in ['{', '/', '.']:
            path = QName(LNP_URI, path)

        return super(ElementBase, self).findall(path, namespaces)

    def findtext(self, path, default=None, namespaces=None):
        if isinstance(path, (str, unicode)) and path[0] not in ['{', '/', '.']:
            path = QName(LNP_URI, path)

        return super(ElementBase, self).findtext(path, default, namespaces)

    @staticmethod
    def from_string(string, validate=False):
        """Create an Element object from a string"""

        if validate:
            parser = XMLParserValidate
        else:
            parser = XMLParser

        # Avoid unicode strings with encoding declaration
        if isinstance(string, unicode):
            string = string.encode('utf-8')

        # Parse the XML string and validate the document
        return etree.fromstring(string, parser=parser)

    @staticmethod
    def to_string(element, validate=False):
        if callable(element):
            element = element()

        if validate:
            XSDSchema.assertValid(element)

        return etree.tostring(
            element,
            encoding='utf-8',
            xml_declaration=True,
            pretty_print=True,
            standalone=False,
        )


XSDSchema = etree.XMLSchema(
    etree.parse(os.path.join(os.path.dirname(__file__), 'schema.xsd'))
)

XMLParser = etree.XMLParser(encoding='utf-8')
XMLParser.set_element_class_lookup(
    etree.ElementDefaultClassLookup(element=ElementBase))

# noinspection PyArgumentList
XMLParserValidate = etree.XMLParser(encoding='utf-8', schema=XSDSchema)
XMLParserValidate.set_element_class_lookup(
    etree.ElementDefaultClassLookup(element=ElementBase))

E = ElementMaker(
    typemap={type(None): lambda e, i: None},
    namespace=LNP_URI,
    nsmap=LNP_NSMAP,
    makeelement=XMLParser.makeelement
)

QName = etree.QName


#
# Meta classes
#

class XMLObjectMeta(type):
    def __new__(mcs, name, bases, attrs):
        # Get initial descriptors list from class attributes
        desc_list = attrs.get('__descriptors__', [])

        # Extend descriptor list with inherited descriptors
        for cls in bases:
            if hasattr(cls, '__descriptors__'):
                desc_list.extend(cls.__descriptors__)

        # Extend descriptor list with class descriptors
        for attr_name, attr_value in attrs.items():

            # Define attribute name for BaseType instances
            if isinstance(attr_value, BaseType):
                attr_value.name = attr_name
                desc_list.append(attr_value)

        attrs['__descriptors__'] = sorted(desc_list, key=hash)

        return super(XMLObjectMeta, mcs).__new__(mcs, name, bases, attrs)


#
# Main classes
#

class BaseType(object):

    instance_count = 0
    name = None
    tag = None
    blank = False

    def __init__(self, tag=None, blank=False):
        self.__doc__ = '{0} value'.format(self.__class__.__name__)

        if tag:
            self.tag = tag

        if blank:
            self.blank = blank

        self.instance_number = BaseType.instance_count
        BaseType.instance_count += 1

    def __hash__(self):
        return hash(self.instance_number)

    def __repr__(self):
        return '<{0} "{1}">'.format(self.__class__.__name__, self.name)

    # noinspection PyUnusedLocal
    def __get__(self, instance, owner):
        if instance is None:
            return self

        value = instance.__dict__.get(self.name, None)

        if value is not None:
            return self.format_for_get(value)

    def __set__(self, instance, value):
        if instance is not None:

            try:
                if value is not None:
                    value = self.format_for_set(value)

            except TypeError as e:

                # Error string defined in exception
                if str(e):
                    raise e

                # Default error string
                raise TypeError('Invalid type "{0}" for {1} "{2}"'.format(
                    type(value).__name__, self.__class__.__name__, self.name))

            instance.__dict__[self.name] = value

    def __delete__(self, instance):
        if instance is not None:
            if self.name in instance.__dict__:
                del instance.__dict__[self.name]

    def format_for_get(self, value):
        return value

    def format_for_set(self, value):
        return value

    @property
    def tag(self):
        return self.__dict__.get('tag', self.name)

    @tag.setter
    def tag(self, value):
        self.__dict__['tag'] = value

    @tag.deleter
    def tag(self):
        if 'tag' in self.__dict__:
            del self.__dict__['tag']


class XMLObject(object):

    __metaclass__ = XMLObjectMeta
    __descriptors__ = []

    def __call__(self):
        return E(self.tag, *self)

    def __iter__(self):
        for attr in self.__descriptors__:
            value = self.__dict__.get(attr.name, None)

            if value is not None or not attr.blank:
                element = E(attr.tag)

                if value is not None:
                    if isinstance(value, (str, unicode)):
                        element.text = value

                    elif isinstance(value, list):
                        for e in value:
                            if attr.inner_tag:
                                element.append(E(attr.inner_tag, *e))
                            else:
                                element.extend(e)
                    else:
                        element.extend(value)

                yield element

    def __new__(cls, *args, **kwargs):
        if cls == XMLObject:
            raise NotImplementedError('{0} must be sub-classed'.format(
                cls.__name__))
        else:
            return super(XMLObject, cls).__new__(cls)

    def __str__(self):
        return str(self())

    def __unicode__(self):
        return str(self).decode('utf-8')

    @property
    def tag(self):
        """XML root tag name"""
        return self.__dict__.get('tag', self.__class__.__name__)

    @tag.setter
    def tag(self, value):
        self.__dict__['tag'] = value

    @tag.deleter
    def tag(self):
        if 'tag' in self.__dict__:
            del self.__dict__['tag']

    @classmethod
    def from_xml(cls, element):
        """Return an object instance from a XML  element"""

        if element is None:
            return None

        kwargs = {}

        for attr in cls.__descriptors__:
            kwargs[attr.name] = element.find(attr.tag)

        return cls(**kwargs)


#
# Descriptors
#

class Instance(BaseType):

    cls = XMLObject

    def __init__(self, tag=None, blank=False, cls=XMLObject):
        super(Instance, self).__init__(tag, blank)

        if cls:
            self.cls = cls

    def format_for_set(self, value):
        if etree.iselement(value):
            value = self.cls.from_xml(value)

            if value is None:
                return

        if isinstance(value, self.cls):
            return value

        raise TypeError


class InstanceList(BaseType):

    cls = XMLObject
    inner_tag = None

    def __init__(self, tag=None, blank=False, cls=XMLObject, inner_tag=None):
        super(InstanceList, self).__init__(tag, blank)

        if cls:
            self.cls = cls

        if inner_tag:
            self.inner_tag = inner_tag

    def format_for_set(self, value):
        if etree.iselement(value):
            if self.inner_tag:
                value = [self.cls.from_xml(e)
                         for e in value.findall(self.inner_tag)]
            else:
                value = self.cls.from_xml(value)

            if value is None:
                return

        if isinstance(value, list):
            for i in value:
                if not isinstance(i, self.cls):
                    raise TypeError(
                        'Invalid type for a member of "{0}": "{1}"'.format(
                            self.__class__.__name__, type(i).__name__))

            return value

        raise TypeError


class String(BaseType):

    length = None
    min_length = None
    max_length = None

    def __init__(self, tag=None, blank=False, length=None, min_length=None,
                 max_length=None):
        super(String, self).__init__(tag, blank)

        if length:
            self.length = length

        if self.length:
            self.min_length = self.max_length = self.length

        else:
            if min_length:
                self.min_length = min_length
            if max_length:
                self.max_length = max_length

    def format_for_set(self, value):
        if etree.iselement(value):
            value = value.text

            if value is None:
                return

        if isinstance(value, (str, unicode)):
            try:
                self.validate(value)

            except ValueError as e:
                if str(e):
                    raise e

                raise ValueError('Invalid value for {0} "{1}": "{2}"'.format(
                    self.__class__.__name__, self.name, value))

            return value

        raise TypeError

    def validate(self, value):
        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError('String is too short: "{0}"'.format(value))
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError('String is too long: "{0}"'.format(value))


class Boolean(String):

    def format_for_get(self, value):
        return value in ['1', 'true']

    def format_for_set(self, value):
        if isinstance(value, bool):
            value = '1' if value else '0'

        return super(Boolean, self).format_for_set(value)

    def validate(self, value):
        if value not in ['0', '1', 'true', 'false']:
            raise ValueError


class DateTime(String):

    # Date formatting string
    datetime_format = '%Y-%m-%dT%H:%M:%SZ'

    def format_for_get(self, value):
        return datetime.strptime(value[:19] + 'Z', self.datetime_format)

    def format_for_set(self, value):
        if isinstance(value, datetime):
            value = value.strftime(self.datetime_format)

        elif isinstance(value, (str, unicode)):
            value = value[:19] + 'Z'

        return super(DateTime, self).format_for_set(value)

    def validate(self, value):
        datetime.strptime(value[:19] + 'Z', self.datetime_format)


class Integer(String):

    def format_for_get(self, value):
        return int(value)

    def format_for_set(self, value):
        if isinstance(value, int):
            value = str(value)

        return super(Integer, self).format_for_set(value)

    def validate(self, value):
        int(value)


class NumericString(String):
    def validate(self, value):
        super(NumericString, self).validate(value)

        if not re.match(r'^\d*$', value):
            raise ValueError


class CNL(NumericString):
    length = 5


class CNPJ(String):
    max_length = 14


class CPF(String):
    max_length = 11


class ConfirmationStatus(String):
    def validate(self, value):
        if value not in ['success', 'failed']:
            raise ValueError


class CustomerName(String):
    max_length = 40


class CustomerType(String):
    def validate(self, value):
        if value not in ['legal_entity', 'individual']:
            raise ValueError


class DownloadReason(String):
    def validate(self, value):
        if value not in ['new', 'delete', 'modified']:
            raise ValueError


class DownloadReplyStatus(String):
    def validate(self, value):
        if value not in ['success', 'failed']:
            raise ValueError


class EOT(String):
    length = 3


class ErrorNumber(Integer):
    pass


class ErrorStatus(String):
    def validate(self, value):
        if value not in ['success', 'session-invalid', 'failed']:
            raise ValueError


class FraudErrorJustification(String):
    max_length = 255


class FraudErrorType(String):
    def validate(self, value):
        if value not in ['fraud', 'error']:
            raise ValueError


class GenericID(String):
    max_length = 20


class LineType(String):
    def validate(self, value):
        if value not in ['Basic', 'DDR', 'CNG']:
            raise ValueError


class LNPType(String):
    def validate(self, value):
        if value not in ['lspp', 'lisp']:
            raise ValueError


class OptionalData(String):
    pass


class PhoneNumber(NumericString):
    min_length = 10
    max_length = 11


class QueryExpression(String):
    pass


class RN1(NumericString):
    length = 5


class ServiceProvAuthorization(Boolean):
    pass


class ServiceProvId(String):
    length = 4


class ServiceProvName(String):
    max_length = 40


class SubscriptionPreCancellationStatus(String):
    def validate(self, value):
        if value not in ['conflict', 'pending', 'disconnect_pending']:
            raise ValueError


class SubscriptionStatusChangeCauseCode(Integer):
    pass


class SubscriptionVersionId(Integer):
    pass


class VersionStatus(String):
    def validate(self, value):
        if value not in ['conflict', 'active', 'pending', 'sending',
                         'download-failed', 'download-failed-partial',
                         'disconnect-pending', 'old', 'cancelled',
                         'cancel-pending', 'suspended']:
            raise ValueError


#
# Message components
#

class BdoCompletionTS(XMLObject):
    version_id = SubscriptionVersionId()
    completion_ts = DateTime()
    download_reason = DownloadReason()

    def __init__(self, version_id, completion_ts, download_reason):
        self.version_id = version_id
        self.completion_ts = completion_ts
        self.download_reason = download_reason


class CustomerID(XMLObject):

    # todo: Element '{urn:brazil:lnp:1.0}CPF': This element is not expected. Expected is one of ( {urn:brazil:lnp:1.0}individual, {urn:brazil:lnp:1.0}legal_entity )

    def __call__(self):
        # noinspection PySuperArguments
        return E(self.tag, super(CustomerID, self).__call__())

    @classmethod
    def from_xml(cls, element):
        """Return an object instance from a XML element"""

        if cls is not CustomerID:
            # noinspection PySuperArguments
            return super(CustomerID, cls).from_xml(element)

        if element is None:
            return None

        # Get id type from message content
        id_type = QName(element[0]).localname

        if id_type == 'individual':
            return IndividualId.from_xml(element[0])

        if id_type == 'legal_entity':
            return LegalEntityId.from_xml(element[0])

        raise NotImplementedError(
            'Costumer ID type not implemented: "{0}"'.format(id_type))


class IndividualId(CustomerID):

    tag = 'individual'

    cpf = CPF('CPF', blank=True)
    generic_id = GenericID(blank=True)

    def __init__(self, cpf=None, generic_id=None):
        self.cpf = cpf
        self.generic_id = generic_id


class LegalEntityId(CustomerID):

    tag = 'legal_entity'

    cnpj = CNPJ('CNPJ', blank=True)
    generic_id = GenericID(blank=True)

    def __init__(self, cnpj=None, generic_id=None):
        self.cnpj = cnpj
        self.generic_id = generic_id


class DownloadReply(XMLObject):
    status = DownloadReplyStatus()
    error_info = String(blank=True)
    bdo_completion_ts = Instance(blank=True, cls=BdoCompletionTS)

    def __init__(self, status, error_info=None, bdo_completion_ts=None):
        self.status = status
        self.error_info = error_info
        self.bdo_completion_ts = bdo_completion_ts


class ErrorReason(XMLObject):
    error_number = ErrorNumber()
    error_info = String(blank=True)

    def __init__(self, error_number, error_info=None):
        self.error_number = error_number
        self.error_info = error_info


class ErrorData(XMLObject):
    error_status = ErrorStatus()
    error_reason = Instance(blank=True, cls=ErrorReason)

    def __init__(self, error_status, error_reason=None):
        self.error_status = error_status
        self.error_reason = error_reason


class FailedSP(XMLObject):
    service_prov_id = ServiceProvId()
    service_prov_name = ServiceProvName()

    def __init__(self, service_prov_id, service_prov_name):
        self.service_prov_id = service_prov_id
        self.service_prov_name = service_prov_name

    @classmethod
    def from_xml(cls, element):
        if element is None:
            return None

        service_prov_id_list = element.findall('service_prov_id')
        service_prov_name_list = element.findall('service_prov_name')

        def map_func(service_prov_id, service_prov_name):
            return cls(service_prov_id.text, service_prov_name.text)

        return map(map_func, service_prov_id_list, service_prov_name_list)


class FraudInformation(XMLObject):
    subscription_fraud_error_version_id = SubscriptionVersionId()
    subscription_recipient_fraud_error_type = FraudErrorType()
    subscription_recipient_fraud_error_justification = \
        FraudErrorJustification(blank=True)
    subscription_adjust_fraud_error_duedate = Boolean(blank=True)

    def __init__(self, subscription_fraud_error_version_id,
                 subscription_recipient_fraud_error_type,
                 subscription_recipient_fraud_error_justification=None,
                 subscription_adjust_fraud_error_duedate=None):

        self.subscription_fraud_error_version_id = \
            subscription_fraud_error_version_id
        self.subscription_recipient_fraud_error_type = \
            subscription_recipient_fraud_error_type
        self.subscription_recipient_fraud_error_justification = \
            subscription_recipient_fraud_error_justification
        self.subscription_adjust_fraud_error_duedate = \
            subscription_adjust_fraud_error_duedate


class FraudSuspicionInformation(XMLObject):
    subscription_donor_fraud_error_type = FraudErrorType()
    subscription_donor_fraud_error_justification = \
        FraudErrorJustification(blank=True)

    def __init__(self, subscription_donor_fraud_error_type,
                 subscription_donor_fraud_error_justification=None):

        self.subscription_donor_fraud_error_type = \
            subscription_donor_fraud_error_type
        self.subscription_donor_fraud_error_justification = \
            subscription_donor_fraud_error_justification


class MessageHeader(XMLObject):
    """Object representing an SPG message header"""

    service_prov_id = ServiceProvId()
    invoke_id = Integer()
    message_date_time = DateTime()

    def __init__(self, service_prov_id, invoke_id, message_date_time):
        super(MessageHeader, self).__init__()
        self.service_prov_id = service_prov_id
        self.invoke_id = invoke_id
        self.message_date_time = message_date_time


class OperationReplyStatus(XMLObject):
    status = ConfirmationStatus()
    error_reason = Instance(blank=True, cls=ErrorReason)

    def __init__(self, status, error_reason=None):
        self.status = status
        self.error_reason = error_reason


class PrePortData(XMLObject):
    customer_id = Instance(cls=CustomerID)
    customer_name = CustomerName(blank=True)
    customer_type = CustomerType()

    def __init__(self, customer_id, customer_type, customer_name=None):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_type = customer_type


class QueryBdoSVsData(XMLObject):
    query_expression = QueryExpression()

    def __init__(self, query_expression):
        self.query_expression = query_expression


class SubscriptionData(XMLObject):
    subscription_recipient_sp = ServiceProvId()
    subscription_recipient_eot = EOT()
    subscription_activation_timestamp = DateTime()
    broadcast_window_start_timestamp = DateTime(blank=True)
    subscription_rn1 = RN1()
    subscription_new_cnl = CNL(blank=True)
    subscription_lnp_type = LNPType()
    subscription_download_reason = DownloadReason()
    subscription_line_type = LineType()
    subscription_optional_data = OptionalData(blank=True)

    def __init__(self, subscription_recipient_sp,
                 subscription_recipient_eot, subscription_activation_timestamp,
                 subscription_rn1, subscription_lnp_type,
                 subscription_download_reason, subscription_line_type,
                 broadcast_window_start_timestamp=None,
                 subscription_new_cnl=None, subscription_optional_data=None):

        self.subscription_recipient_sp = subscription_recipient_sp
        self.subscription_recipient_eot = subscription_recipient_eot
        self.subscription_activation_timestamp = \
            subscription_activation_timestamp
        self.broadcast_window_start_timestamp = \
            broadcast_window_start_timestamp
        self.subscription_rn1 = subscription_rn1
        self.subscription_new_cnl = subscription_new_cnl
        self.subscription_lnp_type = subscription_lnp_type
        self.subscription_download_reason = subscription_download_reason
        self.subscription_line_type = subscription_line_type
        self.subscription_optional_data = subscription_optional_data


class SubscriptionDownloadDeleteData(XMLObject):
    subscription_download_reason = DownloadReason()
    broadcast_window_start_timestamp = DateTime(blank=True)

    def __init__(self, subscription_download_reason,
                 broadcast_window_start_timestamp=None):
        self.subscription_download_reason = subscription_download_reason
        self.broadcast_window_start_timestamp = \
            broadcast_window_start_timestamp


class SubscriptionVersionObjectData(XMLObject):
    subscription_version_id = SubscriptionVersionId()
    subscription_version_tn = PhoneNumber()
    subscription_recipient_sp = ServiceProvId()
    subscription_recipient_eot = EOT(blank=True)
    subscription_donor_sp = ServiceProvId()
    subscription_pre_port_data = Instance(blank=True, cls=PrePortData)
    subscription_fraud_error_data = \
        Instance(blank=True, cls=FraudInformation)
    subscription_customer_extended_port_date = Boolean(blank=True)
    subscription_fixed_special = Boolean(blank=True)
    subscription_documentation_receipt_confirmation = Boolean(blank=True)
    subscription_group_id = Integer(blank=True)
    subscription_donor_sp_authorization_due_date = DateTime(blank=True)
    subscription_activation_timestamp = DateTime(blank=True)
    subscription_rn1 = RN1(blank=True)
    subscription_new_cnl = CNL(blank=True)
    subscription_old_cnl = CNL(blank=True)
    subscription_lnp_type = LNPType()
    subscription_download_reason = DownloadReason()
    subscription_version_status = VersionStatus()
    subscription_due_date = DateTime(blank=True)
    subscription_recipient_sp_creation_ts = DateTime(blank=True)
    subscription_recipient_completion_ts = DateTime(blank=True)
    subscription_donor_completion_ts = DateTime(blank=True)
    subscription_donor_sp_authorization = \
        ServiceProvAuthorization(blank=True)
    subscription_fraud_error_suspicion_data = \
        Instance(blank=True, cls=FraudSuspicionInformation)
    subscription_status_change_cause_code = \
        SubscriptionStatusChangeCauseCode(blank=True)
    subscription_cancellation_cause_code = Integer(blank=True)
    subscription_donor_sp_authorization_ts = DateTime(blank=True)
    subscription_broadcast_timestamp = DateTime(blank=True)
    subscription_conflict_timestamp = DateTime(blank=True)
    subscription_customer_disconnect_date = DateTime(blank=True)
    subscription_effective_release_date = DateTime(blank=True)
    subscription_disconnect_complete_timestamp = DateTime(blank=True)
    subscription_cancellation_timestamp = DateTime(blank=True)
    subscription_creation_timestamp = DateTime(blank=True)
    failed_service_provs = InstanceList(blank=True, cls=FailedSP)
    subscription_modified_timestamp = DateTime(blank=True)
    subscription_old_timestamp = DateTime(blank=True)
    subscription_recipient_sp_cancellation_timestamp = \
        DateTime(blank=True)
    subscription_recipient_sp_conflict_resolution_timestamp = \
        DateTime(blank=True)
    subscription_porting_to_original_sp = Boolean()
    subscription_precancellation_status = \
        SubscriptionPreCancellationStatus(blank=True)
    subscription_timer_type = Integer(blank=True)
    subscription_business_type = Integer(blank=True)
    subscription_line_type = LineType()
    subscription_optional_data = OptionalData(blank=True)

    def __init__(self, subscription_version_id, subscription_version_tn,
                 subscription_recipient_sp, subscription_donor_sp,
                 subscription_lnp_type, subscription_download_reason,
                 subscription_version_status, failed_service_provs,
                 subscription_porting_to_original_sp, subscription_line_type,
                 subscription_recipient_eot=None,
                 subscription_pre_port_data=None,
                 subscription_fraud_error_data=None,
                 subscription_customer_extended_port_date=None,
                 subscription_fixed_special=None,
                 subscription_documentation_receipt_confirmation=None,
                 subscription_group_id=None,
                 subscription_donor_sp_authorization_due_date=None,
                 subscription_activation_timestamp=None, subscription_rn1=None,
                 subscription_new_cnl=None, subscription_old_cnl=None,
                 subscription_due_date=None,
                 subscription_recipient_sp_creation_ts=None,
                 subscription_recipient_completion_ts=None,
                 subscription_donor_completion_ts=None,
                 subscription_donor_sp_authorization=None,
                 subscription_fraud_error_suspicion_data=None,
                 subscription_status_change_cause_code=None,
                 subscription_cancellation_cause_code=None,
                 subscription_donor_sp_authorization_ts=None,
                 subscription_broadcast_timestamp=None,
                 subscription_conflict_timestamp=None,
                 subscription_customer_disconnect_date=None,
                 subscription_effective_release_date=None,
                 subscription_disconnect_complete_timestamp=None,
                 subscription_cancellation_timestamp=None,
                 subscription_creation_timestamp=None,
                 subscription_modified_timestamp=None,
                 subscription_old_timestamp=None,
                 subscription_recipient_sp_cancellation_timestamp=None,
                 subscription_recipient_sp_conflict_resolution_timestamp=None,
                 subscription_precancellation_status=None,
                 subscription_timer_type=None, subscription_business_type=None,
                 subscription_optional_data=None):
        self.subscription_version_id = subscription_version_id
        self.subscription_version_tn = subscription_version_tn
        self.subscription_recipient_sp = subscription_recipient_sp
        self.subscription_recipient_eot = subscription_recipient_eot
        self.subscription_donor_sp = subscription_donor_sp
        self.subscription_pre_port_data = subscription_pre_port_data
        self.subscription_fraud_error_data = subscription_fraud_error_data
        self.subscription_customer_extended_port_date = \
            subscription_customer_extended_port_date
        self.subscription_fixed_special = subscription_fixed_special
        self.subscription_documentation_receipt_confirmation = \
            subscription_documentation_receipt_confirmation
        self.subscription_group_id = subscription_group_id
        self.subscription_donor_sp_authorization_due_date = \
            subscription_donor_sp_authorization_due_date
        self.subscription_activation_timestamp = \
            subscription_activation_timestamp
        self.subscription_rn1 = subscription_rn1
        self.subscription_new_cnl = subscription_new_cnl
        self.subscription_old_cnl = subscription_old_cnl
        self.subscription_lnp_type = subscription_lnp_type
        self.subscription_download_reason = subscription_download_reason
        self.subscription_version_status = subscription_version_status
        self.subscription_due_date = subscription_due_date
        self.subscription_recipient_sp_creation_ts = \
            subscription_recipient_sp_creation_ts
        self.subscription_recipient_completion_ts = \
            subscription_recipient_completion_ts
        self.subscription_donor_completion_ts = \
            subscription_donor_completion_ts
        self.subscription_donor_sp_authorization = \
            subscription_donor_sp_authorization
        self.subscription_fraud_error_suspicion_data = \
            subscription_fraud_error_suspicion_data
        self.subscription_status_change_cause_code = \
            subscription_status_change_cause_code
        self.subscription_cancellation_cause_code = \
            subscription_cancellation_cause_code
        self.subscription_donor_sp_authorization_ts = \
            subscription_donor_sp_authorization_ts
        self.subscription_broadcast_timestamp = \
            subscription_broadcast_timestamp
        self.subscription_conflict_timestamp = subscription_conflict_timestamp
        self.subscription_customer_disconnect_date = \
            subscription_customer_disconnect_date
        self.subscription_effective_release_date = \
            subscription_effective_release_date
        self.subscription_disconnect_complete_timestamp = \
            subscription_disconnect_complete_timestamp
        self.subscription_cancellation_timestamp = \
            subscription_cancellation_timestamp
        self.subscription_creation_timestamp = subscription_creation_timestamp
        self.failed_service_provs = failed_service_provs
        self.subscription_modified_timestamp = subscription_modified_timestamp
        self.subscription_old_timestamp = subscription_old_timestamp
        self.subscription_recipient_sp_cancellation_timestamp = \
            subscription_recipient_sp_cancellation_timestamp
        self.subscription_recipient_sp_conflict_resolution_timestamp = \
            subscription_recipient_sp_conflict_resolution_timestamp
        self.subscription_porting_to_original_sp = \
            subscription_porting_to_original_sp
        self.subscription_precancellation_status = \
            subscription_precancellation_status
        self.subscription_timer_type = subscription_timer_type
        self.subscription_business_type = subscription_business_type
        self.subscription_line_type = subscription_line_type
        self.subscription_optional_data = subscription_optional_data


class SubscriptionVersionQueryReplyData(XMLObject):
    query_status = Instance(cls=OperationReplyStatus)
    version_list = InstanceList(
        blank=True, cls=SubscriptionVersionObjectData, inner_tag='data')

    def __init__(self, query_status, version_list=None):
        self.query_status = query_status
        self.version_list = version_list


class SubscriptionVersionQueryRequestData(XMLObject):
    version_id = SubscriptionVersionId()
    query_expression = QueryExpression()

    # todo: choices

    def __init__(self, version_id, query_expression):
        self.version_id = version_id
        self.query_expression = query_expression


class TNVersionId(XMLObject):
    tn = PhoneNumber()
    version_id = SubscriptionVersionId()

    def __init__(self, tn, version_id):
        self.tn = tn
        self.version_id = version_id


class SubscriptionVersionData(XMLObject):
    subscription_tn_version_id = Instance(cls=TNVersionId)
    subscription_data = Instance(cls=SubscriptionData)

    def __init__(self, subscription_tn_version_id, subscription_data):
        self.subscription_tn_version_id = subscription_tn_version_id
        self.subscription_data = subscription_data


class SubscriptionVersionDeleteData(XMLObject):
    subscription_version_id = SubscriptionVersionId()
    subscription_delete_data = \
        Instance(cls=SubscriptionDownloadDeleteData)

    def __init__(self, subscription_version_id, subscription_delete_data):
        self.subscription_version_id = subscription_version_id
        self.subscription_delete_data = subscription_delete_data


#
# Generic message
#

class Message(XMLObject):
    """Generic SPG message"""

    message_header = Instance('messageHeader', cls=MessageHeader)
    message_content = None  # defined in the subclass

    def __init__(self, message_header, message_content):
        self.message_header = message_header
        self.message_content = message_content

    def __new__(cls, *args, **kwargs):
        if cls == Message:
            raise NotImplementedError('{0} must be sub-classed'.format(
                cls.__name__))
        else:
            return super(Message, cls).__new__(cls)

    def __str__(self):
        return ElementBase.to_string(self, validate=True)

    @property
    def invoke_id(self):
        return self.message_header.invoke_id

    @property
    def message_date_time(self):
        return self.message_header.message_date_time

    @property
    def service_prov_id(self):
        return self.message_header.service_prov_id

    @classmethod
    def from_string(cls, string):
        """Return an object instance from a XML string"""

        # Get XML element from string
        element = ElementBase.from_string(string, validate=True)

        # Return object from XML element
        return cls.from_xml(element)

    @classmethod
    def from_xml(cls, element):
        """Return an object instance from a XML element"""

        if element is None:
            return None

        from libspg.bdo import BDOMessage

        # Get the message type
        msg_type = QName(element).localname

        # Get the message class from the message type
        msg_cls = locals().get(msg_type, None)

        if not msg_cls:
            raise NotImplementedError(
                'Message type not implemented: "{0}"'.format(msg_type))

        return msg_cls.from_xml(element)
