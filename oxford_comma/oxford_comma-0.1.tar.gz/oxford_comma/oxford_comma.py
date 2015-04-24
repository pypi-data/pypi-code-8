# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.tag
def oxford_comma(parser, token):
    # Given a list of items, properly comma and 'and' them together
    try:
        tag_name, list_of_items = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "{tag_name} tag requires exactly one argument".format(tag_name=token.contents.split()[0])
        )
    else:
        return OxfordCommaNode(list_of_items)


class OxfordCommaNode(template.Node):

    def __init__(self, list_of_items):
        self.list_of_items = template.Variable(list_of_items)

    def render(self, context):
        try:
            list_of_items = self.list_of_items.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        else:
            if len(list_of_items) == 2:
                return "{first} and {second}".format(first=list_of_items[0], second=list_of_items[1])
            else:
                list_of_items[-1] = "and " + list_of_items[-1]
                return ", ".join(list_of_items)
