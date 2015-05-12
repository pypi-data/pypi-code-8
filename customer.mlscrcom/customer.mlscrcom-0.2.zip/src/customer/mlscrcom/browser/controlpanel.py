# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) 2011 Propertyshelf, Inc. and its Contributors.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
###############################################################################
"""mls-cr.com Settings Control Panel."""

# zope imports
from plone.app.registry.browser import controlpanel

# local imports
from customer.mlscrcom.i18n import _
from customer.mlscrcom.interfaces import IMLSCRComSettings


class MLSCRComSettingsEditForm(controlpanel.RegistryEditForm):
    """mls-cr.com Settings Form"""

    schema = IMLSCRComSettings
    label = _(
        u"heading_mls_settings",
        default=u"mls-cr.com Settings",
    )
    description = _(
        u"help_mls_settings",
        default=u"Settings for the custom front page.",
    )

    def updateFields(self):
        super(MLSCRComSettingsEditForm, self).updateFields()

    def updateWidgets(self):
        super(MLSCRComSettingsEditForm, self).updateWidgets()


class MLSCRComSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """mls-cr.com Settings Control Panel"""

    form = MLSCRComSettingsEditForm
