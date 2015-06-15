# -*- coding: utf-8 -*-
"""Viewlets used on the package."""
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from collective.blueline.config import BASE_REGISTRY


class BluelineViewletBase(ViewletBase):

    """Base class for Blueline viewlets."""

    def show(self):
        """Return True if the viewlet will be visible.

        Viewlets will be visible for anonymous users only, unless
        we define in the control panel configlet that authenticated
        users will also see the code.

        As a security measure, viewlets are never shown in the context
        of the configlet. This way we can revert the inclusion of any
        code that breaks the layout.
        """
        context_state = api.content.get_view(
            u'plone_context_state', self.context, self.request)
        is_configlet = '@@blueline-settings' in context_state.current_page_url()
        show = api.user.is_anonymous() or self.show_authenticated
        return not is_configlet and show


class HtmlHeadViewlet(BluelineViewletBase):

    """Viewlet to be rendered inside the head tag."""

    def update(self):
        """Update viewlet with the content of the html_head record."""
        self.show_authenticated = api.portal.get_registry_record(BASE_REGISTRY + 'show_authenticated')
        self.code = api.portal.get_registry_record(BASE_REGISTRY + 'html_head')


class HeaderViewlet(BluelineViewletBase):

    """Viewlet to be rendered at the top of the page."""

    def update(self):
        """Update viewlet with the content of the header record."""
        self.show_authenticated = api.portal.get_registry_record(BASE_REGISTRY + 'show_authenticated')
        self.code = api.portal.get_registry_record(BASE_REGISTRY + 'header')


class AboveContentViewlet(BluelineViewletBase):

    """Viewlet to be rendered above the content of the page."""

    def update(self):
        """Update viewlet with the content of the above_content record."""
        self.show_authenticated = api.portal.get_registry_record(BASE_REGISTRY + 'show_authenticated')
        self.code = api.portal.get_registry_record(BASE_REGISTRY + 'above_content')


class BelowContentViewlet(BluelineViewletBase):

    """Viewlet to be rendered below the content of the page."""

    def update(self):
        """Update viewlet with the content of the below_content record."""
        self.show_authenticated = api.portal.get_registry_record(BASE_REGISTRY + 'show_authenticated')
        self.code = api.portal.get_registry_record(BASE_REGISTRY + 'below_content')


class BelowContentBodyViewlet(BluelineViewletBase):

    """Viewlet to be rendered below the body of the content of the page."""

    def update(self):
        """Update viewlet with the content of the below_content record."""
        self.show_authenticated = api.portal.get_registry_record(BASE_REGISTRY + 'show_authenticated')
        self.code = api.portal.get_registry_record(BASE_REGISTRY + 'below_content_body')


class FooterViewlet(BluelineViewletBase):

    """Viewlet to be rendered at the end of the page."""

    def update(self):
        """Update viewlet with the content of the footer record."""
        self.show_authenticated = api.portal.get_registry_record(BASE_REGISTRY + 'show_authenticated')
        self.code = api.portal.get_registry_record(BASE_REGISTRY + 'footer')
