# coding: utf-8

from django.contrib.admin.views.main import ChangeList

# Anche e svilupato totalmente indipendentemente, 
# ho visto che una soluzione euivalente è questa
# djangosnippets.org/snippets/2322

class JmbChangeList(ChangeList):
    def __init__(self, request, *args):
        super(JmbChangeList, self).__init__(request, *args)

        # Cambio il titolo della pagina se viene aggiunto il parametro list_title
        if hasattr(self.model_admin, 'list_title'):
            self.title = self.model_admin.list_title

 
    def get_filters(self, request):
        """
        clean self.params settings the values cleaned by the
        search_form, so that dates can be localized
        """
        # we cannot just pop these params: it breaks pagination
        # that must attach them
        # but if we leave them these will be reproccessed by 
        # ChangeList.get_filters in a way that is different from
        # filterset one
        original_params = self.params.copy()
        if hasattr(self.model_admin, 'search_form'):
            search_form = self.model_admin.search_form
            search_form.is_valid()

            if search_form.is_valid():
                for name in self.model_admin._lookup_names:
                    self.params.pop(name, None)
        filters = ChangeList.get_filters(self, request)
        self.params = original_params
        return filters
