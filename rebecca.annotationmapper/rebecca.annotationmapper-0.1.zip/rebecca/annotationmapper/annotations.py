class FromMatchDict(object):
    def __init__(self, name=None):
        self.name = name

    def __call__(self, request):
        return request.matchdict.get(self.name)


class FromParam(object):
    def __init__(self, name=None):
        self.name = name

    def __call__(self, request):
        return request.params.get(self.name)


class FromSession(object):
    def __init__(self, name=None):
        self.name = name

    def __call__(self, request):
        return request.session.get(self.name)


class FromHeader(object):
    def __init__(self, name=None):
        self.name = name

    def __call__(self, request):
        return request.headers.get(self.name)


class FromAttr(object):
    def __init__(self, name=None):
        self.name = name

    def __call__(self, request):
        return getattr(request, self.name)
