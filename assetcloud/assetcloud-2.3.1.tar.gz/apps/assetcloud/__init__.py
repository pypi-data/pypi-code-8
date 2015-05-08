# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from django.conf import settings


__version__ = '2.3.1'


def site_url(request=None):
    """
    Get the fully qualified URL of the Asset Cloud site.

    request parameter is optional but the result will be less accurate without
    it (it'll just be constructed from the PROTOCOL and DOMAIN settings, instead
    of dynamically built from the request).
    """

    protocol = settings.PROTOCOL
    host_and_port = settings.DOMAIN

    if request:
        if request.is_secure():
            protocol = 'https'

        # HTTP_HOST is set based on the Host: header sent by the browser and
        # SERVER_NAME is set based on the Host apache directive (in the vhost
        # config).
        # I prioritise HTTP_HOST over SERVER_NAME here because I am confident
        # that HTTP_HOST will include the account's custom subdomain
        # (Account.subdomain) if the user is accessing the site via the
        # custom subdomain URL, but I'm not confident that SERVER_NAME will
        # do so.
        if 'HTTP_HOST' in request.META:
            host_and_port = request.META['HTTP_HOST']
        elif 'SERVER_NAME' in request.META:
            host_and_port = request.META['SERVER_NAME']

    return '%s://%s' % (protocol, host_and_port)
