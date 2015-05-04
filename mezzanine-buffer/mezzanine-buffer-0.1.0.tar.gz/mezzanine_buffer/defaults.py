from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from mezzanine.conf import register_setting

register_setting(
    name="BUFFER_CLIENT_ID",
    label=_("Buffer Client ID"),
    editable=True,
    default='',
)

register_setting(
    name="BUFFER_CLIENT_SECRET",
    label=_("Buffer Client Secret"),
    editable=True,
    default='',
)

register_setting(
    name="BUFFER_ACCESS_TOKEN",
    label=_("Buffer Access Token"),
    editable=True,
    default='',
)
