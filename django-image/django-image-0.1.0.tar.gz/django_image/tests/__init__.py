from django.conf import settings


settings.IMAGES_BACKEND = 'django_image.tests.backend.DummyBackend'
