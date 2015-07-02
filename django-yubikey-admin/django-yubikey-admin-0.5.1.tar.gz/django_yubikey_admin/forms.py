from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.admin.forms import AdminAuthenticationForm
from yubico_client import Yubico


class AuthenticationForm(AdminAuthenticationForm):

    username = forms.CharField(label=_("Username"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    otp = forms.CharField(label=_("OTP"), widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        otp = self.cleaned_data.get('otp')

        # lifted from django.contrib.auth admin field
        if username and password and otp:

            self.user_cache = authenticate(username=username,
                                           password=password, otp=otp)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )

            # verify the yubikey
            try:
                client = Yubico(settings.YUBIKEY_CLIENT_ID,
                                settings.YUBIKEY_SECRET_KEY)
                client.verify(otp)
            except:
                raise forms.ValidationError(_("Yubikey confirmation failed."))

        return self.cleaned_data
