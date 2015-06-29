from smtpcom.router import Router

class APIBase(object):

    def __init__(self, content_type='json'):
        self.__router = Router()
        self.__router.set_content_type(content_type)

    @property
    def router(self):
        return self.__router
