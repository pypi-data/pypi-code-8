# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from assetcloud_auth import email_to_username
from assetcloud.models import Asset, AssetImageInfo, Account, Folder, Share, SharedAsset, Upload, AccountCancellation, get_user_profile_class, AssetDownloadLog
from django import forms
from django.contrib import admin
from django.template.loader import render_to_string
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class UserCreationForm(forms.ModelForm):
    """
    Our customized UserCreationForm, based on
    django.contrib.auth.forms.UserCreationForm, with some modifications,
    to ensure the email gets duplicated to the username.

    Creates a user, with no privileges, from the given email and password.
    """
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label=("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification.")

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError("A user with that email already exists.")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't "
                                        "match.")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = email_to_username(self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Our customised UserChangeForm, based on
    django.contrib.auth.forms.UserChangeForm, with some modifications,
    to ensure the email gets duplicated to the username.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')


class UserProfileInline(admin.StackedInline):
    model = get_user_profile_class()


class UserAdmin(UserAdmin):
    """
    Our customized UserAdmin, which is a simpler verison of the standard
    UserAdmin, and which uses our custom user forms.
    """
    inlines = [UserProfileInline]

    login_as_user = lambda u: render_to_string(
        'assetcloud/snippets/login_as_user_link.html', {'user': u})
    login_as_user.short_description = 'Login as user'
    login_as_user.allow_tags = True

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'date_joined', 'last_login',
                    login_as_user)
    list_filter = ('is_staff', 'date_joined', 'last_login')
    search_fields = ('email',)

    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff',
                                      'is_superuser', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )


class AccountAdmin(admin.ModelAdmin):
    pass


class AssetImageInfoInline(admin.StackedInline):
    model = AssetImageInfo


class AssetAdmin(admin.ModelAdmin):
    inlines = [AssetImageInfoInline]
    list_filter = ['account']
    list_display = ('filename', 'file', 'title', 'added')


class SharedAssetInline(admin.StackedInline):
    model = SharedAsset


class ShareAdmin(admin.ModelAdmin):
    inlines = [SharedAssetInline]


class AssetDownloadLogAdmin(admin.ModelAdmin):
    readonly_fields = ["datetime", "user", "asset"]
    list_display = ["__str__", "user", "asset", "datetime"]


admin.site.unregister(User)
admin.site.register(Account, AccountAdmin)
admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetDownloadLog, AssetDownloadLogAdmin)
admin.site.register(Folder)
admin.site.register(Share, ShareAdmin)
admin.site.register(Upload)
admin.site.register(User, UserAdmin)
admin.site.register(AccountCancellation)
