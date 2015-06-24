"""
Handling media content in redactor.js
"""

from django.conf import settings
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from bangoo.media.models import Image

@csrf_exempt
@require_POST
@login_required
def upload_images(request):
    retval = []
    for f in request.FILES.getlist("file"):
        if f.content_type.find('image') == -1:
            raise Http404()  # TODO: very ugly type check
        i = Image(file=f)
        i.save()
        i.tags.add('article')
        retval.append({"filelink": settings.MEDIA_URL + i.file.name})
    return JsonResponse(retval, safe=False)


@login_required
def list_images(request):
    images = [
        {"thumb": settings.MEDIA_URL + img.file.get_thumbnail({'size': (150, 150)}).name, 
         "image": settings.MEDIA_URL + img.file.name}
        for img in Image.objects.filter(tags__name='article')
    ]
    return JsonResponse(images, safe=False)
