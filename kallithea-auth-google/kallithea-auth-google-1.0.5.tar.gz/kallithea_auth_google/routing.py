"""Routes configuration."""


def make_map(config):
    """Create, configure and return the routes Mapper."""
    rmap = config['routes.map']
    # OAUTH2 callback
    rmap.connect(
        'oauth2callback', '/oauth2callback', controller='kallithea_auth_google.controllers:GoogleAuthController',
        action='oauth2callback', condition=dict(method=["GET"]))
