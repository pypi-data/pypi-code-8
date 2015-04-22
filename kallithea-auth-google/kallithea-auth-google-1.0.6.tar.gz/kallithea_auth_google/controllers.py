"""Auth controller."""
import logging
from pylons.i18n.translation import _
from pylons import request
from pylons.controllers.util import redirect

import kallithea.lib.helpers as h
from kallithea.lib.base import BaseController

from .auth_google import KallitheaAuthPlugin

log = logging.getLogger(__name__)


class GoogleAuthController(BaseController):

    """Controller to handle authenticated callback."""

    def oauth2callback(self):
        """Handle oauth2 callback."""
        state = request.GET.get('state')
        code = request.GET.get('code')
        plugin = KallitheaAuthPlugin()
        plugin.store_user_info(code=code)
        h.flash(_('Successfully authenticated'), 'success')
        redirect(state)
