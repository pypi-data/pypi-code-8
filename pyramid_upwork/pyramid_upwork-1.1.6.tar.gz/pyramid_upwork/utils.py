import upwork


def get_upwork_client(request, **attrs):
    """Construct an Upwork client.

    *Parameters:*
      :attrs:   keyword arguments that will be
                attached to the ``client.auth`` as attributes
                (``request_token``, etc.)
    """
    client_kwargs = {
        'oauth_access_token': attrs.pop('oauth_access_token', None),
        'oauth_access_token_secret': attrs.pop(
            'oauth_access_token_secret', None)

    }

    settings = request.registry.settings
    client = upwork.Client(settings['upwork.api.key'],
                           settings['upwork.api.secret'], **client_kwargs)

    for key, value in attrs.items():
        setattr(client.auth, key, value)

    return client
