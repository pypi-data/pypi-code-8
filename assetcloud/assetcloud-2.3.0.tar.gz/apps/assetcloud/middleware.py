# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.contrib.auth.views import redirect_to_login
from assetcloud.models import get_user_profile_class
from assetcloud.views.utils import view_is_public

UserProfile = get_user_profile_class()


class LoginRequiredMiddleware(object):
    """
    Requires a login for every view, except:
    - the login view itself
    - views decorated with @assetcloud.views.decorators.public
    - requests whose paths are covered by one of the regexes in settings.PUBLIC_URLS
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_is_public(request, view_func, view_args, view_kwargs):
            try:
                request.account = request.user.get_profile().account
            except (UserProfile.DoesNotExist, AttributeError):
                pass
            return

        if request.user.is_anonymous() or not request.user.is_active:
            return redirect_to_login(request.path)

        try:
            request.account = request.user.get_profile().account
        except UserProfile.DoesNotExist:
            raise AssertionError('No account')
