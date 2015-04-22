"""Auth middleware."""
from .routing import make_map


def make_middleware(app, config, **kwargs):
    """Make google auth middleware.

    Middleware is only needed to register additional routes
    """
    make_map(app.config)
    return app
