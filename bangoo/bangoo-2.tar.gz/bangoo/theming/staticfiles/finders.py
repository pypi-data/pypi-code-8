from django.conf import settings
from django.contrib.staticfiles.finders import BaseStorageFinder
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.contrib.staticfiles.utils import check_settings, get_files


class ThemeStaticFilesStorage(StaticFilesStorage):
    prefix = 'themes'

    def __init__(self, *args, **kwargs):
        location = settings.THEMES_BASE_DIR
        base_url = settings.STATIC_URL + 'themes/'
        super(ThemeStaticFilesStorage, self).__init__(location, base_url, *args, **kwargs)


class FileSystemFinder(BaseStorageFinder):
    storage = ThemeStaticFilesStorage

    def find(self, path, all=False):
        if not path.startswith('themes/'):
            return []
        path = '%s/%s' % (settings.THEMES_BASE_DIR.strip('themes'), path, )
        return super(FileSystemFinder, self).find(path, all)

    def list(self, ignore_patterns):
        ignore_patterns += ['templates', '*.html']
        return super(FileSystemFinder, self).list(ignore_patterns)