import pyramid.httpexceptions as exc

##################################################
# add_slash_route (config, route_name, "/service_name/')
#  will add both /service_name and /service_name/ to same place
def add_slash_route(config,name, pattern, **kw):
    """Add both the route and route/ to point to the same view
    """
    if pattern.endswith('/'):
        config.add_route(name, pattern, **kw)
    pattern = pattern.rstrip ('/')
    config.add_route(name + '_auto', pattern)
    def redirector(request):
        return exc.HTTPMovedPermanently(request.route_url(name,_query=request.GET,**request.matchdict))
    config.add_view(redirector, route_name=name + '_auto')

