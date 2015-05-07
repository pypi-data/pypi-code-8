# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django import template
from django.conf import settings
from django.forms import widgets
from django.template.loader import get_template
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape, escape
from django.utils.safestring import mark_safe

TOP_ERRORS_TEMPLATE = "assetcloud/snippets/form/top_errors.html"
STANDARD_FIELD_TEMPLATE = "assetcloud/snippets/form/standard_field.html"
CHECKBOX_FIELD_TEMPLATE = "assetcloud/snippets/form/checkbox_field.html"
HIDDEN_FIELD_TEMPLATE = "assetcloud/snippets/form/hidden_field.html"
RADIO_SELECT_TEMPLATE = "assetcloud/snippets/form/radio_select_field.html"
SUBDOMAIN_TEMPLATE = "assetcloud/snippets/form/subdomain.html"

register = template.Library()


@register.simple_tag(takes_context=True)
def render_form(context, form, field_class=None, mark_required=False):
    """
    Render a form with Asset Cloud style HTML.
    """
    # Render the non field and hidden field errors
    output = render_top_errors(context, form)

    # Render the fields
    for field in form:
        output += render_field(context, field, field_class, mark_required)

    return output


@register.simple_tag(takes_context=True)
def render_asset_form(context, form, field_class=None, mark_required=False):
    output = render_form(context, form, field_class=field_class, mark_required=mark_required)

    if hasattr(form, "metadata_forms"):
        for metadata_form in form.metadata_forms:
            for field in metadata_form:
                output += render_field(context, field, field_class, mark_required)
    return output


@register.simple_tag(takes_context=True)
def render_top_errors(context, form):
    """
    Render non-field errors and other errors that can't be rendered with a
    field (e.g. hidden field errors).
    """
    top_errors = form.non_field_errors()

    add_hidden_field_errors(form, top_errors)

    template = get_template(TOP_ERRORS_TEMPLATE)
    context.push()
    context['top_errors'] = top_errors
    context['form'] = form
    result = template.render(context)
    context.pop()
    return result


def add_hidden_field_errors(form, errors):
    """
    Add errors for hidden fields in form to errors.
    """
    # based on Django's BaseForm._html_output
    for name, field in form.fields.items():
        bf = form[name]
        if bf.is_hidden:
            bf_errors = form.error_class(
                [conditional_escape(error) for error in bf.errors])
            if bf_errors:
                errors.extend(
                    [mark_safe(u'(Hidden field %s) %s' % (escape(name), force_unicode(e))) for e in
                     bf_errors])


@register.simple_tag(takes_context=True)
def render_field(context, field, field_class=None, mark_required=False):
    """
    Render a field with Asset Cloud style html.
    """
    old_attrs = field.field.widget.attrs
    if field_class:
        old_attrs['class'] = field_class

    context.push()

    if field.is_hidden:
        template = get_template(HIDDEN_FIELD_TEMPLATE)
    elif field.field.widget.__class__ == widgets.CheckboxInput:
        template = get_template(CHECKBOX_FIELD_TEMPLATE)
    elif field.field.widget.__class__ == widgets.RadioSelect:
        template = get_template(RADIO_SELECT_TEMPLATE)
    elif field.name == "subdomain":
        context['DOMAIN_SUFFIX'] = settings.DOMAIN_SUFFIX
        template = get_template(SUBDOMAIN_TEMPLATE)
    else:
        template = get_template(STANDARD_FIELD_TEMPLATE)

    field.field.widget.attrs = old_attrs

    context['field'] = field
    context['mark_required'] = mark_required
    result = template.render(context)
    context.pop()
    return result
