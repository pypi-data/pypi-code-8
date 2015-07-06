# -*- coding: utf-8 -*-
"""Init and utils."""

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('collective.updatemimetype')

from collective.updatemimetype.migration import migrate

migrate  # please pep8
