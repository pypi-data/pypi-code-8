
from __future__ import unicode_literals

import os

from django import forms
from django.conf import settings
from django.contrib.admin import widgets
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _, ugettext
from feincms.views.decorators import standalone

from leonardo.module.media.models import Clipboard, Folder, FolderRoot, Image, tools


@standalone
def directory_detail_fullscreen(request, category_id):
    object = Folder.objects.get(id=category_id)

    return render_to_response(
        'media/directory_detail.html', {
            'object': object,
        },
        context_instance=RequestContext(request)
    )
