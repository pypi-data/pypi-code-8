from django.http.response import HttpResponse
from django.views.generic import View


class RtsView(View):
    request_handler_class = None
    transformer_class = None
    response_generator_class = None

    def dispatch(self, request, *args, **kwargs):
        request_handler = self.request_handler_class()
        transformer = self.transformer_class()
        response_generator = self.response_generator_class(request)

        obj = request_handler.get_object(request)
        obj = transformer.transform(obj)

        response = response_generator.get_response(obj)

        return response
