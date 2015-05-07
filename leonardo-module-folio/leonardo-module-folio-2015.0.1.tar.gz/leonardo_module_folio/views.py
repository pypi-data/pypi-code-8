# -*- coding: UTF-8 -*-

from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import get_language_from_request

from .models import (Category, CategoryTranslation, Client, Project,
                     ProjectTranslation, Service)


def project_list(request):
    category_list = Category.objects.filter(active=True, parent=None)
    client_list = Client.objects.filter(active=True)
    object_list = Project.objects.filter(active=True)
    context = RequestContext(request, {
        'object_list': object_list,
        'client_list': client_list,
        'xx': 'xxxxxx',
        'category_list': category_list,
        'in_appcontent_subpage': True
    })
    return render_to_response('folio/project_list.html', {}, context_instance=context)


def project_detail(request, project_slug=None):
    object = ProjectTranslation.objects.get(slug=project_slug).parent
    return render_to_response(
        'folio/project_detail.html', {
            'object': object,
            'in_appcontent_subpage': True
        },
        context_instance=RequestContext(request)
    )
