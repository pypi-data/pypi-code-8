# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
Core user authentication, creation and management.
"""
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.core.exceptions import PermissionDenied
import hashlib


class Groups(object):
    @property
    def account_admins(self):
        return Group.objects.get(name=u'account_admins')

    @property
    def editors(self):
        return Group.objects.get(name=u'editors')


groups = Groups()


class EmailModelBackend(ModelBackend):
    """
    A custom authentication backend, so that we
    verify against email/password, rather than against username/password.
    """
    supports_inactive_user = True

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None


def login_user(request, user):
    """
    Login the user without suppliying the password.
    Obviously you should only *ever* use this if you know the user is valid.
    TODO: Drop this and ensure we only ever use login with
    explicit email/password, for safety.
    """
    user.backend = settings.AUTHENTICATION_BACKENDS[0]
    login(request, user)


def email_to_username(email):
    """
    Hashes an email into a unique username.
    Emails are the canonical identifier of a user.
    """
    username_field = User._meta.get_field('username')
    return _hexdigest(email, max_length=username_field.max_length)


def _hexdigest(content, max_length=None):
    """
    A short, insecure, hexdigest of the content.
    """
    ret = hashlib.md5(content).hexdigest()
    if max_length:
        return ret[:max_length]
    return ret


def notify_password_change(request):
    message = 'Success! Your password has been changed.'
    messages.add_message(request, messages.SUCCESS, message)


def notify_user_deleted(request, user):
    message = 'Deleted user "%(name)s".' % {
        'name': user.get_profile().original_email
    }
    messages.add_message(request, messages.SUCCESS, message)


def notify_no_known_social_account(request, auth_backend):
    messages.error(request, 'We do not have any records associated with your %s account. If you have already registered and have forgotten which provider you used, click forgot password to be sent a reminder' % auth_backend.name)


def notify_login_error_message(request, user):
    profile = user.get_profile()
    if not profile.is_registered:
        messages.error(request, 'This user needs to complete registration')
    elif profile.is_deleted:
        messages.error(request, 'This user has been deleted')
    elif profile.is_pending:
        messages.error(request, 'This user needs to be activated - an email has been sent to %s' % user.email)


# We replace django's user_passes_test, requires_login and requires_permission
# because they all redirect to login
# We have middleware providing this functionality so a redirect would be #
# pointless. At the point that this will be called the user will already be
# logged in so a 403 is more appropriate
def test_or_403(_test_fn=lambda x: False):
    """Decorator to raise 403 if the given callable test fails"""
    def decorator(fn):
        def new_fn(request, *args, **kwargs):
            if not _test_fn(request.user):
                raise PermissionDenied()
            return fn(request, *args, **kwargs)
        return new_fn
    return decorator


def require_can_edit_assets(fn):
    return test_or_403(lambda u: u.get_profile().can_edit_assets())(fn)


def require_account_admin(fn):
    return test_or_403(lambda u: u.get_profile().has_account_admin_permission())(fn)


def emailcase(email):
    if email is None:
        return email
    parts = email.split(u'@')
    if len(parts) < 2:
        return email
    return '%s@%s' % (parts[0], parts[1].lower())
