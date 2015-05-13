# -*- coding: utf-8 -*-
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _
from django import forms

from .models import CatalogExtension, CatalogPlugin as Plugin


class CatalogPluginForm(forms.ModelForm):
    catalog = forms.ModelChoiceField(
        queryset=CatalogExtension.objects.filter(
            is_catalog=True,
            extended_object__publisher_is_draft=False
        )
    )

    class Meta:
        model = Plugin


class CatalogPlugin(CMSPluginBase):
    name = _('Catalog Plugin')
    model = Plugin
    module = _("Catalog")
    render_template = "cms/plugins/catalog_list_panel.html"
    allow_children = True
    form = CatalogPluginForm
    fieldsets = (
        (None, {
            'fields': (
                'catalog',
                'display_level',
                'display_date',
                ('line_length', 'page_count'),
            )
        }),
        (_('Advanced Settings'), {
            'classes': ('collapse',),
            'fields': (
                'panel_type',
                ('display_panel_header', 'panel_header_link'),
                ('panel_footer_link', 'panel_after_content'),
                'panel_footer_text',
            ),
        }),
    )


plugin_pool.register_plugin(CatalogPlugin)
