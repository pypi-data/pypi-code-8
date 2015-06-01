# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig

import collective.navigationtitle


class CollectiveNavigationtitleLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.file(
            'configure.zcml',
            collective.navigationtitle,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.navigationtitle:default')


COLLECTIVE_NAVIGATIONTITLE_FIXTURE = CollectiveNavigationtitleLayer()


COLLECTIVE_NAVIGATIONTITLE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_NAVIGATIONTITLE_FIXTURE,),
    name='CollectiveNavigationtitleLayer:IntegrationTesting'
)


COLLECTIVE_NAVIGATIONTITLE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_NAVIGATIONTITLE_FIXTURE,),
    name='CollectiveNavigationtitleLayer:FunctionalTesting'
)


COLLECTIVE_NAVIGATIONTITLE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_NAVIGATIONTITLE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveNavigationtitleLayer:AcceptanceTesting'
)
