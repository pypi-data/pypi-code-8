from zope.formlib.form import Fields, PageAddForm, PageEditForm, applyChanges

from zope.app.container.interfaces import INameChooser
from eea.faceted.tool.interfaces import IPortalType
from eea.faceted.tool.storage.portaltype import PortalType

class AddPage(PageAddForm):
    """ Add page
    """
    form_fields = Fields(IPortalType)

    def create(self, data):
        name = INameChooser(self.context).chooseName(data.get('title', ''), None)
        ob = PortalType(id=name)
        applyChanges(ob, self.form_fields, data)
        return ob

    def add(self, obj):
        name = obj.getId()
        self.context[name] = obj
        self._finished_add = True
        return obj

    def nextURL(self):
        return "./@@view"

class EditPage(PageEditForm):
    """ Edit page
    """
    form_fields = Fields(IPortalType)
