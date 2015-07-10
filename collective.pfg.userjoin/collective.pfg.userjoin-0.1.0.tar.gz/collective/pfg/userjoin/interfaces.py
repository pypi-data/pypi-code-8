# -*- coding: utf-8 -*-

from zope.interface import Interface


class IUserJoinAdapter(Interface):
    """A form action adapter that will save form input data and
       keep them until Manager use this data to create new site's members
    """
