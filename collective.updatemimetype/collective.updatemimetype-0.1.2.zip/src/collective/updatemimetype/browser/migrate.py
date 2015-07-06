from Products.Five import BrowserView
from collective.updatemimetype.migration import migrate


class MigrateView(BrowserView):

    def __call__(self):
        query = self.request.form.get('query', {})
        migrate(self.context, query=query)
        return 'migrated'
