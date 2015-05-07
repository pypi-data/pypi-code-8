# -*- coding: utf-8 -*-
# (c) 2011-2013 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from django.conf import settings
from django.core.mail import get_connection, \
                             EmailMessage, EmailMultiAlternatives
from django.template import loader, Context
from django.template.loader_tags import BlockNode, ExtendsNode
from django.utils.html import strip_tags


def _get_node(nodelist, name, context):
    """
    Get a named node from a template.
    Returns `None` if a node with the given name does not exist.
    """
    for node in nodelist:
        if isinstance(node, BlockNode) and node.name == name:
            return node
        elif isinstance(node, ExtendsNode):
            parent_template = node.get_parent(context)
            parent_template._render(context)
            return _get_node(parent_template.nodelist, name, context=context)
    return None


def _render_node(template, node_name, context):
    """
    Shortcut to render a named node from a template, using the given context.
    Returns `None` if a node with the given name does not exist.

    Note that leading and trailing whitespace is stripped from the output.
    """
    template._render(context)
    node = _get_node(template.nodelist, node_name, context=context)
    if node is None:
        return None
    return node.render(context).strip()


def create_message(subject, plain, html,
                   from_email, recipient_list, connection):
    """
    Return an EmailMessage or EmailMultiAlternatives instance, containing
    either a plaintext or multipart html/plaintext representations.

    If only `plain` is supplied, a plaintext email will be created.
    If only `html` is supplied, a multipart email will be created, and
      the plaintext representation will be automatically created from the html.
    If both `plain` and `html` are supplied
    """
    if plain is None and html is None:
        plain = ''
    elif plain is None:
        plain = strip_tags(html)

    if html:
        message = EmailMultiAlternatives(
            subject,
            plain,
            from_email,
            recipient_list,
            connection=connection,
        )
        message.attach_alternative(html, 'text/html')

    else:
        message = EmailMessage(
            subject,
            plain or '',
            from_email,
            recipient_list,
            connection=connection,
        )

    return message


def send_mail(template_name, from_email, recipient_list,
              dictionary=None, context_instance=None,
              fail_silently=False, auth_user=None, auth_password=None,
              connection=None):
    """
    Similar to the standard Django `send_mail`, but renders the subject
    and body of the email from a template.

    The body text can be plaintext, or html, or both
    (in which case the email client will display whichever it supports).

    The template should contain a block named 'subject',
    and either or both of a 'plain' and/or 'html' block.

    Required arguments:
    `template_name` - The template that should be used to render the email.
    `from_email` - The sender's email address.
    `recipient_list` - A list of reciepient's email addresses.

    Optional arguments:
    `dictionary` - The context dictionary used to render the template.
                   By default, this is an empty dictionary.
    `context_instance` - The Context instance used to render the template.
                         By default, the template will be rendered with a
                         Context instance (filled with values from dictionary).
    `fail_silently` - As in Django's send_mail.
    `auth_user`     - As in Django's send_mail.
    `auth_password` - As in Django's send_mail.
    `connection`    - As in Django's send_mail.
    """
    if dictionary is None:
        dictionary = {}
    if context_instance is None:
        context_instance = Context()
    context_instance.push()
    if connection is None:
        connection = get_connection(username=auth_user,
                                    password=auth_password,
                                    fail_silently=fail_silently)

    context_instance.update(dictionary)

    if hasattr(settings, 'PROJECT_NAME'):
        context_instance['PROJECT_NAME'] = settings.PROJECT_NAME

    template = loader.get_template(template_name)

    subject = _render_node(template, 'subject', context_instance)
    plain = _render_node(template, 'plain', context_instance)
    html = _render_node(template, 'html', context_instance)

    if subject is None:
        subject = ''
    else:
        subject = ' '.join(subject.splitlines())  # Strip newlines

    message = create_message(subject, plain, html,
                             from_email, recipient_list, connection)
    result = message.send()
    context_instance.pop()
    return result
