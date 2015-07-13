from . import widgets as _widgets
from wtforms.fields import *

_FileField = FileField

class FileField(_FileField):
    '''
    Used for handling single file field.
    '''
    def process_formdata(self, valuelist):
        if len(valuelist) > 1:
            raise ValueError(self.gettext('Only accept one file if the field is present.'))
        # valuelist will be [] if the field is not present, set data to None
        # valuelist will be [b''] if no file uploaded, set data to None
        if valuelist == [] or valuelist == [b'']:
            self.data = None
        else:
            self.data = valuelist[0]

class MultiFilesField(_FileField):
    '''
    Used for handling multi files field.
    '''
    widget = _widgets.MultiFilesInput()

    def process_formdata(self, valuelist):
        # valuelist will be [b''] if no files uploaded, so set data to None
        if valuelist == [b'']:
            self.data = None
        else:
            self.data = valuelist
