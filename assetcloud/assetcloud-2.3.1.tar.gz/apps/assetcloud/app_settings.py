from django.conf import settings

ASSET_METADATA_MODELS = getattr(settings, "ASSET_METADATA_MODELS", [])

HOMEPAGE_TAG_MAX_ASSET_COUNT = getattr(settings, "HOMEPAGE_TAG_MAX_ASSET_COUNT", 20)

DEFAULT_LIST_THUMBNAIL_OPTIONS = getattr(settings, "DEFAULT_LIST_THUMBNAIL_OPTIONS", {
    'geometry_string': '120x120',
    'crop': 'center'
})
