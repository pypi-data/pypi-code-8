from django.views.generic.base import TemplateResponseMixin
from django.template.response import TemplateResponse


class ResponseGenerator(object):
    serializer_class = None
    serializer_kwargs = {}

    def __init__(self, request):
        self.request = request

    def get_serialized_data(self, obj):
        serializer = self.serializer_class()
        return serializer.serialize(obj, **self.serializer_kwargs)

    def get_response(self, obj):
        raise NotImplementedError('.get_response(obj) must be implemented')


class WebFormAutoSubmitGenerator(TemplateResponseMixin, ResponseGenerator):
    method = 'POST'
    field = 'data'
    action = ''
    intro_text = ''
    send_button_text = 'Continue'
    template_name = 'rts/webform_autosubmit.html'
    response_class = TemplateResponse

    def get_context_data(self, obj):
        data = self.get_serialized_data(obj)
        context = {
            'field': self.field,
            'action': self.action,
            'method': self.method,
            'data': data,
            'intro_text': self.intro_text,
            'send_button_text': self.send_button_text,
        }

        return context

    def get_response(self, obj):
        context = self.get_context_data(obj)
        return self.render_to_response(context)
