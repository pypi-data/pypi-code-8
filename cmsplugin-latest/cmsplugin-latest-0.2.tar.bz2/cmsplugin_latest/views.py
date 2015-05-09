from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import get_object_or_404

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

import json

from cmsplugin_latest.utils import (
    get_model_field_choices,
    get_fields_for_model,
    get_model_field_choices_flattened,
    get_model_by_name
)
from cmsplugin_latest.models import OrderBy, Latest

import logging, pprint
logger = logging.getLogger('cmsplugin_latest')

def get_model_fields(request):
    model_name = request.POST['model']
    selected_model = get_model_by_name(model_name)

    selected_field = None
    if OrderBy.objects.filter(model=model_name).exists():
        selected_field = OrderBy.objects.get(model=model_name)

    fields = get_fields_for_model(selected_model)
    
    logger.debug("Rendering fields for %s"%model_name)
    response = '<option value=""></option>\n'

    for f in fields:
        response = response + '<option value="%s" '%f
        if f == selected_field:
            response = response + 'selected=1 '
        response = response + '>%s</option>\n'%f
    return HttpResponse(mark_safe(response))

def index(request):
    if request.method == 'POST':
        logger.debug("POST DATA")
        logger.debug(pprint.pformat(request.POST))
    if request.method == 'GET':
        logger.debug("GET DATA")
        logger.debug(pprint.pformat(request.GET))

    return HttpResponse("<p>Go away. I don't like you.</p>")


def CMSPluginLatestFeed(Feed):

    title = None
    description = None

    def __init__(self, *args, **kwargs):
        self.title = kwargs.pop('title')
        self.description = kwargs.pop('description')

    def get_object(self, request, model_name=None, model_pk=None):
        return get_object_or_404(Latest, model=model_name)

