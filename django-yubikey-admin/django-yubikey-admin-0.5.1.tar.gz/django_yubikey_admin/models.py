from django.db import models
from django.contrib.auth.models import User


class YubiKey(User):
    """Storage of yubikey prefixes - if only for validation when the variable is set"""
    user = models.ForeignKey(User, related_name='yubikey_user')
    otp = models.CharField("Yubikey OTP Prefix", max_length=12, unique=True)
