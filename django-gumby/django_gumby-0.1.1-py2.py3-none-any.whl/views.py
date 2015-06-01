import json

from django.http import HttpResponse, HttpResponseServerError
from gumby.healthchecks import healthchecks_dir


def home(request):
    healthchecks = []
    works = None
    for healthcheck_class, healthcheck in healthchecks_dir._registry.items():
        healthcheck = healthcheck_class()
        if works is not False:
            works = healthcheck.status
        healthchecks.append(healthcheck.get_response())

    if works:
        return HttpResponse(json.dumps(healthchecks), content_type="application/json")
    else:
        return HttpResponseServerError(json.dumps(healthchecks), content_type="application/json")

def check(request, check_name):

    response = None

    for healthcheck_class, healthcheck in healthchecks_dir._registry.items():
        healthcheck = healthcheck_class()
        if healthcheck.identifier() == check_name:
            response = healthcheck.get_response()

    if response["status"]:
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponseServerError(json.dumps(response), content_type="application/json")
