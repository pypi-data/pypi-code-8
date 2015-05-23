# -#- coding: utf-8 -#-

from django.utils.translation import ugettext_lazy as _

from leonardo.module.web.models import Widget

from team.models import Person


class TeamWidget(Widget):

    def get_team(self):
        return Person.objects.all()

    class Meta:
        abstract = True
        verbose_name = _("team")
        verbose_name_plural = _("team")
