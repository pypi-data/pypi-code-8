from django.conf import settings

from storages.backends.s3boto import S3BotoStorage


class StaticStorage(S3BotoStorage):
    location = settings.AWS_STATICFILES_STORAGE_DIR


class MediaStorage(S3BotoStorage):
    location = settings.AWS_MEDIAFILES_STORAGE_DIR
