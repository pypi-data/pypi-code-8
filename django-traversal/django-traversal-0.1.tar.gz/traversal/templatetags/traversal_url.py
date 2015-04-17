# coding=utf-8
from django import template

register = template.Library()

@register.simple_tag
def get_url_for_context(context, *params):
    """
    Шаблонный тег, для формирования URL по контексту
    :param context: ресурс, в контексте которого находится искомый URL
    :param params: имя view, последовательно параметры в URL
    :return: возвращает URL
    """
    root_url = context.get_absolute_url()
    abs_url = root_url
    for param in params:
        abs_url += u'/' + str(param)

    return abs_url

@register.simple_tag
def get_url_for_path(path,  *params):
    """
    Практически ручное формирование URL
    :param path: путь к искомому рессурсу, или часть пути. понимает разделение через точку
    :param params: любые динамические параметры, которые требуется присоединить к URL, списком
    :return: возвращает URL
    Пример:
    {% get_url_for_path 'blog.list' post.id %}
    """
    path_list = path.split('.')
    url = u'/' + u'/'.join(path_list)
    for param in params:
        url += u'/' + str(param)
    return url


@register.simple_tag
def get_first_in_context(context, resource_class_name,  *params):
    """
    Похоже на get_url_for_context, с той разницей, что в качестве контекста может быть использован не текущий,
    а первый, который является экземпляром или наследником указанного в resource_class_name класса
    :param context:
    :param resource_class_name:
    :param params:
    :return:
    """
    context_class = context.get_first_resource_for_class_name(resource_class_name)
    context.filter([context_class, ])
    url = context.list[0].get_absolute_url()
    for param in params:
        url += u'/' + str(param)
    return url
