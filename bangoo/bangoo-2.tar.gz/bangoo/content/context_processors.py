from .models import Content
from django.utils.safestring import mark_safe

def widgets(request):
    sidebars = Content.objects.language(request.LANGUAGE_CODE)\
                              .filter(title__startswith='sidebar')\
                              .order_by('title').values_list('text', flat=True)
    sidebars = [mark_safe(s) for s in sidebars]
    footers = Content.objects.language(request.LANGUAGE_CODE)\
                             .filter(title__startswith='footer')\
                             .order_by('title').values_list('text', flat=True)
    footers = [mark_safe(f) for f in footers]
    return {'sidebars': sidebars, 'footers': footers}
