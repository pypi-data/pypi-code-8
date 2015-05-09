from django.shortcuts import render
from goblin.settings import GOBLIN_TEMPLATE_DIR

from goblin.models import *

# Create your views here.

def list_projects(request):
    template = '%s/project_list.html'%GOBLIN_TEMPLATE_DIR
    context = {
        'projects' : Project.objects.with_statuses(['public']),
    }
    return render(request, template, context)

def show_project(request, project_slug):
    p = Project.objects.get(slug=project_slug)
    context = {
        'project' : p,
    }
    template = '%s/project.html'%GOBLIN_TEMPLATE_DIR
    return render(request, template, context)

def project_release(request, project_slug, version):
    p = Project.objects.get(slug=project_slug)
    v = Version.from_str(version)
    release = Release.objects.get(project=project, version=v)
    context = {
        'project' : p,
        #'version' : v,
        'release' : release,
    }
    template = '%s/release.html'%GOBLIN_TEMPLATE_DIR
    return render(request, template, context)
