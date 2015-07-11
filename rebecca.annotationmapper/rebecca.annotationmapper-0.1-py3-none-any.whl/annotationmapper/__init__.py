from . import mappers


def includeme(config):
    config.set_view_mapper(mappers.AnnotationViewMapper)