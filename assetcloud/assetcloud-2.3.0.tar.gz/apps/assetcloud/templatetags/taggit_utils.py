# -*- coding: utf-8 -*-
# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from taggit.utils import edit_string_for_tags
from django import template

register = template.Library()


class _FakeTag(object):
    def __init__(self, name):
        self.name = name


@register.filter
def tag_escape(value):
    return edit_string_for_tags([_FakeTag(value)])
