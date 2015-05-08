# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from assetcloud.fields import EmailField, ClientsideTagField
from assetcloud.model_shortcuts import max_field_length, get_or_none
from assetcloud.models import Account, OrganisationType, get_user_profile_class
from django.contrib.auth import forms, views, models
from django.utils.translation import ugettext as _
import assetcloud_auth
import django.forms
import json

UserProfile = get_user_profile_class()


class LoginForm(views.AuthenticationForm):
    """
    Form for the login action.

    See: https://docs.djangoproject.com/en/dev/ref/forms/api/#configuring-html-label-tags
    """
    def __init__(self, *args, **kwargs):
        if kwargs.get('auto_id') is None:
            kwargs['auto_id'] = '%s'
        super(LoginForm, self).__init__(*args, **kwargs)

    username = EmailField(
        label='Email',
        max_length=max_field_length(models.User, 'email')
    )


class ChangePasswordForm(forms.PasswordChangeForm):
    new_password2 = django.forms.CharField(
        label='Confirm new password',
        widget=django.forms.PasswordInput
    )


class ActivateUserForm(forms.SetPasswordForm):
    new_password1 = django.forms.CharField(
        label='Choose password',
        widget=django.forms.PasswordInput
    )
    new_password2 = django.forms.CharField(
        label='Confirm password',
        widget=django.forms.PasswordInput
    )


class ResetPasswordForm(forms.SetPasswordForm):
    new_password1 = django.forms.CharField(
       label='Choose a new password',
        widget=django.forms.PasswordInput
    )
    new_password2 = django.forms.CharField(
        label='Confirm new password',
        widget=django.forms.PasswordInput
    )

    def save(self):
        password = self.cleaned_data['new_password1']
        self.user.get_profile().reset_password(password)
        return self.user


class ForgottenPasswordForm(django.forms.Form):
    email = django.forms.EmailField(
        label='Email',
        max_length=max_field_length(models.User, 'email')
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        self.user = get_or_none(models.User,
                                email=assetcloud_auth.emailcase(email))

        error = None
        if self.user is None:
            error = 'No user with this email exists.'
        elif self.user.get_profile().is_deleted:
            error = "This account has been deleted."
        elif self.user.get_profile().is_pending:
            error = 'This account is pending activation.'

        if error:
            raise django.forms.ValidationError(error)

        return email

    def save(self):
        UserProfile.create_new_activation_key(self.user)
        return self.user


class AccountForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)

    name = django.forms.CharField(
        max_length=max_field_length(Account, 'name'),
        label="Organisation name",
        required=False)
    organisation_type = django.forms.ModelChoiceField(
        queryset=OrganisationType.objects.all(),
        empty_label="Please select",
        required=False)

    class Meta:
        model = Account
        fields = (
            'name',
            'organisation_type',
            )


class RegisterUserForm(django.forms.Form):
    email = EmailField(
        max_length=max_field_length(models.User, 'email'),
        widget=EmailField.widget(autocomplete=False),
        required=True
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        user = get_or_none(models.User, email=assetcloud_auth.emailcase(email))

        if user is not None:
            error = 'This user already exists.'
            raise django.forms.ValidationError(error)

        return email


class SocialRegisterUserForm(django.forms.Form):
    email = EmailField(
        max_length=max_field_length(models.User, 'email'),
        widget=EmailField.widget(autocomplete=False),
        required=True
        )


class CreateUserForm(RegisterUserForm):
    role = django.forms.ChoiceField(
        widget=django.forms.widgets.RadioSelect,
        label='Role',
        choices=UserProfile.ROLE_NAME_HELP_2_TUPLES
    )

    tags = ClientsideTagField()

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.account = None

    def get_tags(self):
        return [{'name': t, 'is_user_tag': True}
                for t in json.loads(self.data.get('tags', []))]

    def clean_role(self):
        role = self.cleaned_data['role']
        if role not in UserProfile.ROLE_NAMES:
            error = _('Please select a valid role.')
            raise django.forms.ValidationError(error)

        return role

    def clean_email(self):
        if UserProfile.account_user_email_is_valid(self.cleaned_data['email'],
                                                   self.account):
            return self.cleaned_data['email']
        else:
            return super(CreateUserForm, self).clean_email()

    def is_valid(self, account):
        self.account = account
        return super(CreateUserForm, self).is_valid()


class UpdateUserForm(CreateUserForm):
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        del self.fields['email']

    def get_tags(self):
        return self.user.get_profile().visible_tags.all()

    def save(self, user):
        role = self.cleaned_data['role']
        user.get_profile().update_role(role)
        if user.get_profile().tags_allowed:
            user.get_profile().ensure_tags(self.cleaned_data['tags'])
        return user

    def is_valid(self):
        return super(UpdateUserForm, self).is_valid(
            self.user.get_profile().account)
