# -*- coding: utf-8 -*-
# (c) 2013 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from functools import wraps
from django.utils.decorators import available_attrs


def public(view_func):
    """
    Marks a view function as being public, i.e. exempt from
    LoginRequiredMiddleware
    """
    # We could just do view_func.public = True, but decorators are nicer if
    # they don't have side-effects, so we return a new function.
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.public = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)
