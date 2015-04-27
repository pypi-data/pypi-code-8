# coding=utf-8
from __future__ import unicode_literals

import re

from django import template
from django.conf import settings
from django.core.urlresolvers import reverse as django_reverse


register = template.Library()


class SetVarNode(template.Node):
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""


def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])

register.tag('set', set_var)


@register.filter
def active(url, request):
    if request.get_full_path().startswith(url):
        return True
    else:
        return False

@register.filter
def replace(string, args):
    split = args.split(args[0])
    old_value = split[1]
    new_value = split[2]
    return re.sub(old_value, new_value, string)


@register.filter
def timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    if hours:
        return '%02i:%02i:%02i' % (hours, minutes, seconds)
    return '%02i:%02i' % (minutes, seconds)


@register.filter
def seconds_to_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    if hours:
        return '%02i:%02i:%02i' % (hours, minutes, seconds)
    return '%02i:%02i' % (minutes, seconds)


class SettingsValueNode(template.Node):
    def __init__(self, parts):
        self.key = parts[1]
        self.return_name = parts[3] if len(parts) == 4 else None

    def render(self, context):
        try:
            if self.key.startswith('\'') and self.key.endswith('\''):
                key = self.key.replace('\'', '')
            elif self.key.startswith('\"') and self.key.endswith('\"'):
                key = self.key.replace('\"', '')
            else:
                key = template.Variable(self.key).resolve(context)
            if key:
                data = getattr(settings, key)
                if self.return_name:
                    context[self.return_name] = data
                else:
                    return unicode(data)
        except:
            pass
        return ''


@register.tag
def settings_value(parser, token):
    """
        {% settings_value 'key' as <variable> %}
    """
    parts = token.split_contents()
    if len(parts) < 2:
        raise template.TemplateSyntaxError(
            "'settings_value' tag must be of the form:  {% settings_value 'key' %}"
            " or {% settings_value 'key' as <variable> %}")
    return SettingsValueNode(parts)


class UrlReverseNode(template.Node):
    def __init__(self, parts):
        self.url = parts[1]
        if len(parts) > 3 and parts[-2] == 'as':
            self.args = parts[2:-2]
            self.return_name = parts[-1]
        else:
            self.args = parts[2:]
            self.return_name = None

    def render(self, context):
        try:
            url = self.prepare_part(self.url, context)
            args = [self.prepare_part(item, context) for item in self.args]
            if url:
                data = django_reverse(url, args=args)
                if self.return_name:
                    context[self.return_name] = data
                else:
                    return unicode(data)
        except:
            pass
        return ''

    def prepare_part(self, var, context):
        if var.startswith('\'') and var.endswith('\''):
            return var.replace('\'', '')
        if var.startswith('\"') and var.endswith('\"'):
            return var.replace('\"', '')
        return template.Variable(var).resolve(context)


@register.tag
def reverse(parser, token):
    """
        {% reverse url as <variable> %}

        url - can be in context or string named url
    """
    parts = token.split_contents()
    if len(parts) < 2:
        raise template.TemplateSyntaxError(
            "'reverse' tag must be of the form:  {% reverse 'url_name' %} or {% reverse url_var %} or {% reverse url as <variable> %}")
    return UrlReverseNode(parts)