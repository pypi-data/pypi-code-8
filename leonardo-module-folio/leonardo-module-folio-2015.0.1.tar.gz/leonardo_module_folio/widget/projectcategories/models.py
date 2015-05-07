# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _

from leonardo.module.web.models import Widget

from leonardo_module_folio.models import Category


class ProjectCategoriesWidget(Widget):

    def get_categories(self):
        return Category.objects.filter(active=True)

    class Meta:
        abstract = True
        verbose_name = _("project categories")
        verbose_name_plural = _("project categories")
