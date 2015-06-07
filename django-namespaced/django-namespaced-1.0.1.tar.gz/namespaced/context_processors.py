''' Automatically set `current_app` into context based on URL namespace. '''


def namespaced(request):
    ''' Set `current_app` to url namespace '''
    request.current_app = request.resolver_match.namespace
    return {}
