from django.template import TemplateDoesNotExist
from dbtemplate.models import Template

try:
    from django.template.loaders.base import Loader as BaseLoader
except ImportError:  # Django < 1.8
    from django.template.loader import BaseLoader


class DatabaseLoader(BaseLoader):
    """
    A custom template loader to load templates from the database.
    """
    is_usable = True

    def load_template_source(self, template_name, template_dirs=None):
        try:
            template = Template.objects.get(slug=template_name)
        except Template.DoesNotExist:
            raise TemplateDoesNotExist(template_name)
        return template.data, "dbtemplate:%s" % template_name
