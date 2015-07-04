# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView

from .models import Sponsor


class SponsorsList(ListView):
    model = Sponsor
    template_name = "sponsors/sponsors_list.html"
