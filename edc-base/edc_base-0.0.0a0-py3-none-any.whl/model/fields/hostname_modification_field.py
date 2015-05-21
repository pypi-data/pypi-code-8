import socket

from django.db.models import CharField
from django.utils.translation import ugettext as _


class HostnameModificationField (CharField):

    description = _("Custom field for hostname modified")

    def pre_save(self, model, add):
        """Updates socket.gethostname() on each save."""
        value = socket.gethostname()
        setattr(model, self.attname, value)
        return value

    def get_internal_type(self):
        return "CharField"
