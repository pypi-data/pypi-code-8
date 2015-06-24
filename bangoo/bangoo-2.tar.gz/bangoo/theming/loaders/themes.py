from django.conf import settings
from django.template.loaders.filesystem import Loader as FileSystemLoader


class Loader(FileSystemLoader):
    def get_template_sources(self, template_name, template_dirs=None):
        if not template_dirs:
            template_dirs = ()
        template_dirs = ("%s/%s/templates" % (settings.THEMES_BASE_DIR, settings.THEME), ) + template_dirs
        return super(Loader, self).get_template_sources(template_name, template_dirs)