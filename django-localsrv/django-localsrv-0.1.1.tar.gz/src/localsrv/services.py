from django.shortcuts import get_object_or_404

from . import models


def get_content_and_headers_for_path(path_info):
    """

    :type path_info: str
    :param path_info:
    :return:
    """
    servable_content = get_object_or_404(
        models.ServableContent.objects.filter(path=path_info))

    return servable_content.to_string(), {
        header.name: header.value for header in servable_content.headers.all()
    }