# -*- coding: utf-8 -*-
from plone.app.registry.browser import controlpanel
from collective.blueline import _
from collective.blueline.interfaces import IBluelineSettings


class BluelineSettingsEditForm(controlpanel.RegistryEditForm):

    """Control panel edit form."""

    schema = IBluelineSettings
    label = _(u'Blueline')
    description = _(u'Settings for the collective.blueline package')


class BluelineSettingsControlPanel(controlpanel.ControlPanelFormWrapper):

    """Control panel form wrapper."""

    form = BluelineSettingsEditForm
