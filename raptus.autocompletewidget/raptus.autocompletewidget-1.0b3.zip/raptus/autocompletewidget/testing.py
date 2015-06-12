# -*- coding: utf-8 -*-
"""Test layers to tests"""

from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from zope.configuration import xmlconfig

import raptus.autocompletewidget


class RaptusAutocompletewidgetLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.file(
            'configure.zcml',
            raptus.autocompletewidget,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'raptus.autocompletewidget:default')


RAPTUS_AUTOCOMPLETEWIDGET_FIXTURE = RaptusAutocompletewidgetLayer()


RAPTUS_AUTOCOMPLETEWIDGET_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(RAPTUS_AUTOCOMPLETEWIDGET_FIXTURE,),
    name='RaptusAutocompletewidgetLayer:FunctionalTesting'
)
