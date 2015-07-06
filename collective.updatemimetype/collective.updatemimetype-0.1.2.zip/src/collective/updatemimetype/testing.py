# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer
from plone.testing import z2

import collective.updatemimetype


COLLECTIVE_UPDATEMIMETYPE_FIXTURE = PloneWithPackageLayer(
    zcml_package=collective.updatemimetype,
    zcml_filename='testing.zcml',
    gs_profile_id='collective.updatemimetype:testing',
    name='CollectiveUpdatemimetypeLayer',
    additional_z2_products=()
)


COLLECTIVE_UPDATEMIMETYPE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_UPDATEMIMETYPE_FIXTURE,),
    name='CollectiveUpdatemimetypeLayer:IntegrationTesting'
)


COLLECTIVE_UPDATEMIMETYPE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_UPDATEMIMETYPE_FIXTURE,),
    name='CollectiveUpdatemimetypeLayer:FunctionalTesting'
)


COLLECTIVE_UPDATEMIMETYPE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_UPDATEMIMETYPE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveUpdatemimetypeLayer:AcceptanceTesting'
)
