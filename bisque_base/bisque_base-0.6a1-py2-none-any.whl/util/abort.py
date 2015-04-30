



def abort (code=None, comment=None):
    import pyramid.httpexceptions as exc
    raise exc.exception_response (code or 500, comment=comment)
