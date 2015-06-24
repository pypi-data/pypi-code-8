#encoding: utf8
import os
import re
import shutil
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

theme_name_re = re.compile(r'^[a-zA-Z0-9_]+$')

class Command(BaseCommand):
    help_text = "Create new theme with the default directory structure"
    args = "[theme name]"
    can_import_settings = True

    def handle(self, *args, **kwargs):
        try:
            name = args[0]
        except IndexError:
            print(_('Please specify the theme name'))
            return
        if not theme_name_re.match(name):
            print(_('The theme name should contian english ABC letters, numbers and underscores'))
        theme_dir = os.path.join(settings.THEMES_BASE_DIR, name)
        if os.path.exists(theme_dir):
            print(_("The can't be created because the '%(directory)s' directory already exist!" % {'directory': theme_dir}))
            return
        empty_theme_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static/empty_theme")
        empty_theme_dir = getattr(settings, 'EMPTY_THEME_DIR', empty_theme_dir)
        shutil.copytree(empty_theme_dir, theme_dir)
        print(_("The theme directory is created!"))