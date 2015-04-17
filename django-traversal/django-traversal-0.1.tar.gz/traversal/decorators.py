# coding: utf-8
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse


class render_with_context:
    """
    Декоратор для view, позволяющий вместо того, чтобы каждый раз писать render_to_response возвращать
    только список переменных в контексте. Кроме того, в отличие от других подобных декораторов,
    обязательно сам передаёт в шаблон переменную context, с текущим рессурсом
    """
    def __init__(self, template_name):
        self.template_name = template_name

    def __call__(self, func):

        # our decorated function
        def _render_with_context(request, context, *args, **kwargs):
            context_or_response = func(request, context, *args, **kwargs)
            if isinstance(context_or_response, HttpResponse):
                # it's already a response, just return it
                return context_or_response
            else:
                context_or_response['context'] = context
            # it's a context
            return render_to_response(self.template_name, context_or_response,
                                      context_instance=RequestContext(request))

        _render_with_context.__doc__ = func.__doc__
        _render_with_context.__name__ = func.__name__
        _render_with_context.__module__ = func.__module__

        return _render_with_context