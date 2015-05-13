from django.conf import settings

from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        super(StaticStorage, self).__init__(*args, **kwargs)
        self.location = settings.STATICFILES_STORAGE_DIR


class MediaStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        super(MediaStorage, self).__init__(*args, **kwargs)
        self.location = settings.MEDIAFILES_STORAGE_DIR
