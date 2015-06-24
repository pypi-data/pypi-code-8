# coding: utf-8

from ..models import Image
from ..forms import UploadImageForm
from django.shortcuts import render

def images_home(request, template_name='media/images_home.html'):
    form = UploadImageForm(request.POST or None)
    if form.is_valid():
        pass
    images = Image.objects.all()
    return render(request, template_name, {'form': form, 'images': images})


def upload_image(request):
    form = UploadImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        image = form.save()
        image.tags.set(*form.cleaned_data['tags'])
    from django.http import HttpResponse
    return HttpResponse('')
