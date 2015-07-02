from django.contrib.auth.models import User
from django_yubikey_admin.models import YubiKey
from django.conf import settings


class YubikeyAuth:
    """Authentication, with yubikeys"""

    def authenticate(self, username=None, password=None, otp=None):
        if not username or not password:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if not user.is_staff:
            return None

        if not user.check_password(password):
            return None

        # if the key exists, and is set to True, make sure the item
        # is in the database, registered to the user
        if getattr(settings, 'DJANGO_ADMIN_YUBIKEY_CACHE', False):
            try:
                yubi = YubiKey.objects.get(user=user)
            except YubiKey.DoesNotExist:
                return None

            # check the yubikey against the stored constant
            if otp:
                if yubi.otp == otp[:12]:
                    return user
                else:
                    return None

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
