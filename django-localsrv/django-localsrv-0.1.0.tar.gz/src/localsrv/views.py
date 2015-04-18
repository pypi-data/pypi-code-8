from django.http import HttpResponse

from . import services
# from .services import ContentServingService
# Create your views here.


def serve_all(request):
    # import pydevd; pydevd.settrace()
    content, headers = services.get_content_and_headers_for_path(
        request.path_info)

    response = HttpResponse(content)

    for header, value in headers.items():
        response[header] = value

    return response


def default(response):
    return HttpResponse('ok')

