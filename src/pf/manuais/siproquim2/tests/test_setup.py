# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from pf.manuais.siproquim2.testing import PF_MANUAIS_SIPROQUIM2_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that pf.manuais.siproquim2 is properly installed."""

    layer = PF_MANUAIS_SIPROQUIM2_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if pf.manuais.siproquim2 is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'pf.manuais.siproquim2'))

    def test_browserlayer(self):
        """Test that IPfManuaisSiproquim2Layer is registered."""
        from pf.manuais.siproquim2.interfaces import (
            IPfManuaisSiproquim2Layer)
        from plone.browserlayer import utils
        self.assertIn(IPfManuaisSiproquim2Layer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PF_MANUAIS_SIPROQUIM2_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['pf.manuais.siproquim2'])

    def test_product_uninstalled(self):
        """Test if pf.manuais.siproquim2 is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'pf.manuais.siproquim2'))

    def test_browserlayer_removed(self):
        """Test that IPfManuaisSiproquim2Layer is removed."""
        from pf.manuais.siproquim2.interfaces import \
            IPfManuaisSiproquim2Layer
        from plone.browserlayer import utils
        self.assertNotIn(IPfManuaisSiproquim2Layer, utils.registered_layers())
