from . import mustache

def includeme(config): # pragma: no cover
    """
    Adds renderers for .mustache
    """
    config.add_renderer('.mustache', mustache.renderer_factory)
