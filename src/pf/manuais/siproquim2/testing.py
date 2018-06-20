# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import pf.manuais.siproquim2


class PfManuaisSiproquim2Layer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=pf.manuais.siproquim2)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'pf.manuais.siproquim2:default')


PF_MANUAIS_SIPROQUIM2_FIXTURE = PfManuaisSiproquim2Layer()


PF_MANUAIS_SIPROQUIM2_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PF_MANUAIS_SIPROQUIM2_FIXTURE,),
    name='PfManuaisSiproquim2Layer:IntegrationTesting'
)


PF_MANUAIS_SIPROQUIM2_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PF_MANUAIS_SIPROQUIM2_FIXTURE,),
    name='PfManuaisSiproquim2Layer:FunctionalTesting'
)


PF_MANUAIS_SIPROQUIM2_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        PF_MANUAIS_SIPROQUIM2_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='PfManuaisSiproquim2Layer:AcceptanceTesting'
)
