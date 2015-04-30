from pyramid.interfaces import (
    IAuthenticationPolicy,
    IDebugLogger,
    )

from pyramid.authentication import CallbackAuthenticationPolicy
from zope.interface import implementer



@implementer(IAuthenticationPolicy)
class MexAuthAuthenticationPolicy(CallbackAuthenticationPolicy):
    """ A :app:`Pyramid` authentication policy which uses Mex Authentication

    Constructor Arguments

    ``debug``

        Default: ``False``.  If ``debug`` is ``True``, log messages to the
        Pyramid debug logger about the results of various authentication
        steps.  The output from debugging is useful for reporting to maillist
        or IRC channels when asking for support.


     Mex authentication is simply a token used to be passed back to the
     originating server during module processing.

    """
    def __init__(self,  debug=False):
        self.debug = debug

    def unauthenticated_userid(self, request):
        """ The userid parsed from the ``Authorization`` request header."""
        credentials = self._get_credentials(request)
        if credentials:
            return ":".join (credentials)

    def remember(self, request, principal, **kw):
        """ A no-op. Mex authentication does not remember
        """

        return []

    def forget(self, request):
        return []

    def _get_credentials(self, request):
        debug = self.debug

        authorization = request.headers.get('Authorization')
        try:
            auth = authorization.split(' ')
        except ValueError: # not enough values to unpack
            auth =  None

        if auth and auth[0].lower() == 'mex':
            if debug:
                self._log ("MexIdentify %s" % auth, "get_credentials", request)
            try:
                user, token = auth[1].split(':')
                return user,  token
            except ValueError:
                pass

        return None

