from tg import TGController, expose, request, config
from tgext.pluggable import utils
from turbopress import model


class RootController(TGController):
    def __call__(self, *args, **kwargs):
        request.identity = request.environ.get('repoze.who.identity')
        return super(RootController, self).__call__(*args, **kwargs)

    @expose()
    def index(self):
        return 'HELLO'

    @expose()
    def call_partial(self, partial, **kwargs):
        if 'article' in kwargs:
            kwargs['article'] = model.provider.get_obj(model.Article, params=dict(uid=kwargs['article'],
                                                                                  _id=kwargs['article']))
        if 'tags' in kwargs:
            kwargs['tags'] = kwargs['tags'].split(',')

        return utils.call_partial(partial, **kwargs)