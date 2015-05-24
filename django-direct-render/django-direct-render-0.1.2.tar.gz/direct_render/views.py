from django.shortcuts import render
import os.path

# Create your views here.


def direct_render(request, template_name):
    return render(request, os.path.join('direct_render', template_name))
