from django import template
from django.template.loader import render_to_string
from bangoo.media.models import Image

register = template.Library()

@register.simple_tag(name='image_rotator', takes_context=True)
def image_rotator(context, tags, template_name='media/helper/image_rotator.html'):
    tags = [tag.strip() for tag in tags.split(',')]
    images = Image.objects.filter(tags__name__in=tags)
    return render_to_string(template_name, {'images': images}, context_instance=context)
