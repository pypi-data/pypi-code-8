# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin
from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool


class CatalogPlugin(CMSPlugin):
    PANEL_STYLE = (
        ("primary", "primary"),
        ("success", "success"),
        ("info", "info"),
        ("warning", "warning"),
        ("danger", "danger"),
    )
    CHILD = "child"
    CURRENT = "current"
    CURRENT_AND_CHILD = "currchild"
    DISPLAY_LEVEL = (
        (CHILD, _('Child catalog pages')),
        (CURRENT, _('Current catalog pages')),
        (CURRENT_AND_CHILD, _('Current and child catalog pages')),
    )
    panel_type = models.CharField(
        _('Bootstrap panel type'), choices=PANEL_STYLE, max_length=10, default="info", blank=True)
    panel_header_link = models.BooleanField(_('Panel header link to catalog page'), default=True, blank=True)
    panel_footer_text = models.CharField(_('Panel footer text'), max_length=500, null=True, blank=True)
    panel_footer_link = models.BooleanField(_('Panel footer link to catalog page'), default=False, blank=True)
    panel_after_content = models.BooleanField(_('After the panel body has a placeholder'), default=False, blank=True)
    display_panel_header = models.BooleanField(_('Display panel header'), default=True, blank=True)
    display_level = models.CharField(
        _('Which level catalog to show'), choices=DISPLAY_LEVEL, default=CURRENT_AND_CHILD, max_length=50)
    line_length = models.PositiveSmallIntegerField(
        _('Length of every line'), default=30, help_text=_('Zero mean unlimited.'))
    page_count = models.PositiveSmallIntegerField(_('How much page display'), default=5)
    display_date = models.BooleanField(_('Show page date in line'), default=True, blank=True)
    catalog = models.ForeignKey('CatalogExtension', verbose_name=_('Catalog'), null=True)

    def title(self):
        return self.catalog.get_page().get_title()

    def pages(self):
        if self.display_level == self.CHILD:
            pages = self.catalog.get_page().get_descendants()
        elif self.display_level == self.CURRENT:
            pages = self.catalog.get_page().get_leafnodes()
        else:
            pages = self.catalog.get_page().get_descendants()
        return pages[:self.page_count]

    def get_absolute_url(self):
        return self.catalog.get_page().get_absolute_url()


class CatalogExtension(PageExtension):
    is_catalog = models.BooleanField(_('This page is a catalog'), default=True)

    def __unicode__(self):
        return self.get_page().get_title()

    def __str__(self):
        return self.__unicode__().encode("utf-8")

extension_pool.register(CatalogExtension)
