# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig

import collective.portlet.localevents


class CollectivePortletLocaleventsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.file(
            'configure.zcml',
            collective.portlet.localevents,
            context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.portlet.localevents:default')


COLLECTIVE_PORTLET_LOCALEVENTS_FIXTURE = CollectivePortletLocaleventsLayer()


COLLECTIVE_PORTLET_LOCALEVENTS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_PORTLET_LOCALEVENTS_FIXTURE,),
    name='CollectivePortletLocaleventsLayer:IntegrationTesting'
)


COLLECTIVE_PORTLET_LOCALEVENTS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_PORTLET_LOCALEVENTS_FIXTURE,),
    name='CollectivePortletLocaleventsLayer:FunctionalTesting'
)


COLLECTIVE_PORTLET_LOCALEVENTS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_PORTLET_LOCALEVENTS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectivePortletLocaleventsLayer:AcceptanceTesting'
)
