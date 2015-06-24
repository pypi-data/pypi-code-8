# coding: utf-8

from django import template
from django.core.urlresolvers import NoReverseMatch, reverse
from django.template.defaulttags import url as django_url
from django.template.defaulttags import URLNode
from django.template.loader import render_to_string
from django.utils.encoding import smart_text

register = template.Library()

from bangoo.navigation.models import Menu
from bangoo.navigation.utils import get_urlconf


@register.simple_tag(name='menu', takes_context=True)
def generate_menu(context, custom_classes='', template_name='navigation/default.html'):
    lang = context['request'].LANGUAGE_CODE
    items = Menu.objects.language(lang).filter(parent__isnull=True).order_by('tree_id')
    if not context.get('request').user.is_authenticated():
        items = items.exclude(login_required=True)
    active = ''
    for item in items:
        if context['request'].path_info.startswith(item.path) and len(item.path) > len(active):
            active = item.path
    return render_to_string(template_name, {'items': items, 'active': active, 'custom_classes': custom_classes},
                            context_instance=context)


class MenuURLNode(URLNode):
    def render(self, context):
        # TODO: This method works on frontend only
        try:
            return super(MenuURLNode, self).render(context)
        except NoReverseMatch as ex:
            act_menu = context.get('act_menu', None)
            if not act_menu:
                raise ex
            prefix = '/%s/%s' % (context.get('LANGUAGE_CODE'), act_menu.path[1:-1])
            args = [arg.resolve(context) for arg in self.args]
            kwargs = dict((smart_text(k, 'ascii'), v.resolve(context)) for k, v in self.kwargs.items())
            url = reverse(self.view_name.resolve(context), args=args, kwargs=kwargs, urlconf=get_urlconf(act_menu.plugin))
            return prefix + url


@register.tag
def url(parser, token):
    #Just like {% url %} but ads the path of the current menu as prefix.
    node_instance = django_url(parser, token)
    return MenuURLNode(view_name=node_instance.view_name,
                       args=node_instance.args,
                       kwargs=node_instance.kwargs,
                       asvar=node_instance.asvar)


@register.simple_tag(name='admin_url', takes_context=True)
def admin_url(context, *args, **kwargs):
    act_menu = context.get('act_menu', None)
    if not act_menu:
        raise NoReverseMatch
    view_name, args = args[0], args[1:]
    uconf = get_urlconf(act_menu.plugin, frontend_urls=False)
    url1 = reverse('admin:edit-in-menu', args=[act_menu.pk])
    url2 = reverse(view_name, args=args, kwargs=kwargs, urlconf=uconf)
    if url1.endswith('/') and url2.startswith('/'):
        url1 = url1[:-1]
    return url1 + url2
