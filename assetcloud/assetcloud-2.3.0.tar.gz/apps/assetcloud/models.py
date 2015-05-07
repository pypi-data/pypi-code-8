# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
import importlib
import logging
import mimetypes
import os
import tempfile
import time

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import get_current_site
from django.core.exceptions import ValidationError
from django.core.files.storage import DefaultStorage
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Q
from django.db.models.aggregates import Count
from django.db.models.fields import IntegerField, BigIntegerField
from django.db.models.fields.files import FileField
from django.db.models.loading import get_model
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.template.defaultfilters import filesizeformat
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import PassThroughManager
from sorl import thumbnail
from sorl.thumbnail.fields import ImageField
from south.modelsinspector import add_introspection_rules
from taggit.managers import TaggableManager, _TaggableManager
from taggit.models import Tag, TaggedItem
import taggit.models
import validate_on_save

from assetcloud import site_url, app_settings
from assetcloud import app_settings as assetcloud_settings
from assetcloud import srand
from assetcloud.asset_metadata_util import get_metadata_model_and_form_classes
from assetcloud.mail import send_mail
from assetcloud_auth import groups
from assetcloud.model_shortcuts import get_or_none, max_field_length
from assetcloud.random_utils import random_alphanumeric
import assetcloud_auth


logger = logging.getLogger(__name__)


def get_asset_storage():
    asset_storage_module = getattr(settings, 'ASSET_FILE_STORAGE', None)

    if asset_storage_module:
        mod_str, cls_str = asset_storage_module.rsplit('.', 1)
        asset_storage_class = getattr(importlib.import_module(mod_str), cls_str)
    else:
        asset_storage_class = DefaultStorage

    return asset_storage_class()


class ProxyTag(taggit.models.Tag):
    """ Proxy for taggit's Tag object to allow us to add our own methods """
    class Meta:
        # This line ensures this class won't require a database table
        proxy = True

    @property
    def is_user_tag(self):
        return self.taggit_taggeditem_items.filter(content_type=ContentType.objects.get_for_model(get_user_profile_class())).exists()


def user_tags():
    return TaggedItem.tags_for(get_user_profile_class())


class AssetCloudTaggableManager(_TaggableManager):
    """ The underlying taggit manager. This is confusing, but taggit instantiates a new 'inner' manager every time a
        property on its 'outer' manager is requested.

        This can be imagined as asset.tags.all() becoming return InnerTaggableManager(asset, Asset).all().
        The main reason is that tags can be related to ANY other object, so this bit of trickery ensures we always have
        a capable manager for the model on which we're requesting tags. Without it, things like
        Asset.tags.filter(asset=10) would probably throw errors for not knowing what asset is in the context of a
        related query.

        As a result, we subclass the 'inner' manager, and use this as the manager for our TaggableManager
    """

    def get_queryset(self):
        qs = super(AssetCloudTaggableManager, self).get_queryset()
        # Make all the Tags actually be ProxyTags
        qs.model = ProxyTag
        return qs


class OrganisationType(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return u'%s' % self.name


def _validate_logo_image(logo):
    if logo:
        if logo.size > settings.MAX_LOGO_IMAGE_SIZE:
            raise ValidationError(_('Please keep file size under %(max)s. The file you uploaded was %(actual)s.') % {
                'max': filesizeformat(settings.MAX_LOGO_IMAGE_SIZE),
                'actual': filesizeformat(logo.size),
                })


def _validate_hex_colour(colour):
    if colour:
        just_the_hex = colour[1:]
        try:
            int(just_the_hex, 16)
        except ValueError:
            raise ValidationError(_('%(actual)s is not a valid colour, colours should be in the format #RRGGBB') % {
                'actual': colour,
                })

        digits = len(just_the_hex)
        if digits < 6 and digits != 3:
            raise ValidationError(_('%(actual)s is too short, it should have 6 hex digits (#RRGGBB) but actually has %(actual_hex_len)d') % {
                'actual': colour,
                'actual_hex_len': digits
                })


class ColourField(models.CharField):
    """
    A model field for colour values represented as #RRGGBB.
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 7
        super(ColourField, self).__init__(*args, **kwargs)
        self.validators.append(_validate_hex_colour)


add_introspection_rules([], ["^assetcloud\.models\.ColourField"])
add_introspection_rules([], ["^assetcloud\.models\.NullableCharField"])


DEFAULT_COLOURS = {
    'header_background': u'#2C2C2C',
    'header_links': u'#BBBBBB',
    'header_links_active': u'#FFFFFF',
    }


class NullableCharField(models.CharField):
    description = "CharField that stores NULL but returns ''"

    def to_python(self, value):
        return "" if value is None else value

    def get_db_prep_value(self, value, **kwargs):
        return value if value else None


class DomainPartValidator(RegexValidator):
    def __init__(self, **kwargs):
        token = '[a-zA-Z0-9]'
        kwargs['regex'] = '^(%s+|(%s+\-%s+))$' % (token, token, token)
        super(DomainPartValidator, self).__init__(**kwargs)


class ReservedDomainValidator(object):
    reserved = ['www', 'web', 'ftp', 'mail', 'smtp', 'admin', 'pop', 'pop3',
                'imap', 'api', 'data', 'forum', 'support', 'media', 'static',
                'root', 'search', 'None', 'app', 'secure', 'payment',
                'torrents', 'users', 'login', 'signup',
                'register', 'irc', 'blog', 'news', 'logout', 'styleguide',
                'status', 'account']

    def __call__(self, value):
        if value in self.reserved or value is None:
            raise ValidationError(u'%s is a reserved subdomain' % value)


class Account(models.Model):
    """
    A company or group that has signed up to use AssetCloud.
    """
    name = models.CharField(max_length=32, blank=True)
    organisation_type = models.ForeignKey(OrganisationType,
                                          null=True, blank=True)
    welcome_text = models.TextField(blank=True,
        default='Welcome to Asset Share, '
        'a tool for sharing and managing your digital assets.')
    homepage_tags = TaggableManager(manager=AssetCloudTaggableManager)

    logo = models.ImageField(null=True, blank=True, upload_to='logos',
        validators=[_validate_logo_image])
    # Hex values for custom colour schemes
    header_background = ColourField(blank=True, default='')
    header_links = ColourField(blank=True, default='')
    header_links_active = ColourField(blank=True, default='')
    subdomain = NullableCharField(
        blank=True, max_length=100, unique=True,
        null=True, validators=[DomainPartValidator(),
                               ReservedDomainValidator()])
    storage = BigIntegerField(default=0,
        help_text='The storage used by this account, in bytes')
    storage_limit_override = IntegerField(default=0,
        help_text='The custom storage limit for this account, in gigabytes')

    COLOUR_FIELD_NAMES = (
        'header_background',
        'header_links',
        'header_links_active',
        )

    class Meta:
        permissions = (
            # Putting this permission on this model is somewhat arbitrary,
            # but permissions have to be on *a* model so I've picked this
            # one. My justification for putting it here that Editors have
            # permission to add and change the assets *associated with a
            # particular account*. Note that Django permissions apply to a
            # Model, not an Object so the permissions structure does not
            # actually express this.
            ("edit_assets", "Can add and change assets"),
        )

    @staticmethod
    def edit_assets_perm():
        account_ct = ContentType.objects.get_for_model(Account)
        return Permission.objects.get(content_type=account_ct,
                                      codename='edit_assets')

    def __unicode__(self):
        result = self.name
        if self.subdomain:
            result += u' (' + self.subdomain + u')'
        return result

    def full_clean(self, *args, **kwargs):
        super(Account, self).full_clean(*args, **kwargs)
        self._change_default_colours_to_blank()

    def _change_default_colours_to_blank(self):
        """
        Change any colours that are set to the defaults back to blank.
        This is so that if we change the defaults in the future then those
        defaults will be applied to accounts where the customise form has been
        saved. This is necessary because
        CustomiseForm._change_blank_colours_to_default replaces blanks with
        defaults before the page is shown.
        """
        for field_name in self.COLOUR_FIELD_NAMES:
            if getattr(self, field_name).lower() == \
               DEFAULT_COLOURS[field_name].lower():
                setattr(self, field_name, '')

    def _tags_qs(self, query):
        qs = Tag.objects.filter(asset__account=self) | \
             Tag.objects.filter(userprofile__account=self)
        if query:
            qs = qs.filter(name__istartswith=query)
        return qs

    def _tag_counts_qs(self, query):
        qs = self._tags_qs(query)
        qs = qs.annotate(num_items=Count('taggit_taggeditem_items'))
        return qs

    def tag_counts(self, query=None):
        """
        Return a dict of {tag:count} which aggregates the number of times each
        tag has been used by the account.

        If query is not None, only tags that start with the query string
        will be returned.
        """
        # Todo: This should really take a user
        qs = self._tag_counts_qs(query)
        return dict((t.name, t.num_items) for t in qs)

    def tags(self, query=None, limit=None):
        """
        Return a list of all the tags currently used by the account.
        Tags will be sorted alphabetically.
        """
        qs = self._tags_qs(query).order_by('name')[:limit]
        return [t.name for t in qs]

    def tags_by_popularity(self, query=None, limit=None):
        """
        Return a list of all the tags currently used by the account.
        Tags will be sorted by count, most popular first.
        """
        qs = self._tag_counts_qs(query).order_by('-num_items', 'name')[:limit]
        return [t.name for t in qs]

    def _suspend_all_users(self):
        for profile in self.profiles.all():
            profile.suspend()

    def cancel(self, request):
        self._suspend_all_users()

    def would_be_over_storage_limit_by_adding(self, additional_usage):
        """
        additional_usage: additional file size in bytes
        """
        return (self.storage + additional_usage) > self.storage_limit

    @property
    def storage_limit(self):
        if self.storage_limit_override > 0:
            return self.storage_limit_override * 1024 * 1024 * 1024
        else:
            return settings.TRIAL_ACCOUNT_STORAGE_LIMIT

    @property
    def storage_percentage(self):
        return 100.0 * self.storage / self.storage_limit


class UserNotUniqueError(RuntimeError):
    pass


class UnknownUserTypeError(RuntimeError):
    pass


create_new_key = object()


class BaseUserProfile(models.Model):
    """
    Extends the Django ``User`` model.

    See also:
    https://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users
    """

    class Meta:
        abstract = True

    ROLE_ADMIN = 'admin'
    ROLE_EDITOR = 'editor'
    ROLE_VIEWER = 'viewer'

    # Master tuple of 3-tuples containing (code, name, help)
    ROLE_NAME_HELP_3_TUPLES = (
        (ROLE_ADMIN, "Admin", "can do everything"),
        (ROLE_EDITOR, "Editor", "can upload, edit and tag assets"),
        (ROLE_VIEWER, "Viewer", "can only view and download assets"))

    # Derived tuple of 2-tuples containing (code, html_name_combined_with_help)
    ROLE_NAME_HELP_2_TUPLES = tuple(
        [(code, mark_safe((escape(name) + u'<span class="subtle"> &mdash; ' +
                           escape(help) + u'</span>')))
         for (code, name, help)
         in ROLE_NAME_HELP_3_TUPLES])

    ROLE_NAMES = {code: name for (code, name, help) in ROLE_NAME_HELP_3_TUPLES}

    user = models.OneToOneField(User, related_name="userprofile")
    account = models.ForeignKey(Account, null=False, related_name='profiles')
    is_admin = models.BooleanField(default=False, null=False)
    is_editor = models.BooleanField(default=False, null=False)
    activation_key = models.CharField(default='', max_length=32, blank=True)
    is_registered = models.BooleanField(default=False, null=False)
    visible_tags = TaggableManager(manager=AssetCloudTaggableManager, blank=True)

    # This is used when a user is deleted
    original_email = models.EmailField(blank=True)

    def __init__(self, *args, **kwargs):
        super(BaseUserProfile, self).__init__(*args, **kwargs)
        self._activation_email_sent = False

    def filter_search(self, sqs):
        """
        Filters a haystack SearchQuerySet to only include results that this
        user has permission to see.
        """
        return AssetQuerySet.filter_for_user(sqs, self.user)

    def filter_tags_for_restrictions(self, tag_names):
        if not self.all_tags_visible():
            visible_tag_names = {tag.name for tag in self.visible_tags.all()}
            user_tag_names = {tag.name for tag in user_tags()}
            # return all the tags that are either:
            # - NOT user (permission) tags
            # OR
            # - user tags that are visible to this user
            tag_names = [t for t in tag_names
                         if t in visible_tag_names or t not in user_tag_names]
        return tag_names

    def can_delete_user(self, user):
        user_account = user.get_profile().account
        return self.is_admin and self.account == user_account

    def can_update_user(self, user):
        return self.can_delete_user(user)

    def has_account_admin_permission(self):
        try:
            return not self.user.is_anonymous() and self.is_admin
        except AttributeError:
            return False

    def can_edit_assets(self):
        return self.user.has_perm('assetcloud.edit_assets')

    def can_login_as(self, other_user):
        return self.user.is_superuser

    @property
    def is_editor(self):
        return (groups.editors in self.user.groups.all()) and not self.is_admin

    @property
    def is_viewer(self):
        return not self.is_editor and not self.is_admin

    @property
    def rolename(self):
        return BaseUserProfile.ROLE_NAMES[self.role]

    @property
    def tags_allowed(self):
        """
        Is restricting this user by tag allowed?
        """
        return self.is_viewer

    def all_tags_visible(self):
        return not self.visible_tags.exists()

    @property
    def role(self):
        if self.is_admin:
            return BaseUserProfile.ROLE_ADMIN
        elif self.is_editor:
            return BaseUserProfile.ROLE_EDITOR
        elif self.is_viewer:
            return BaseUserProfile.ROLE_VIEWER
        else:
            raise UnknownUserTypeError('The user is not an admin, editor or viewer user.')

    @property
    def folder(self):
        return self.user.folders.get()

    @property
    def is_active(self):
        return self.user.is_active

    @property
    def forgotten_password(self):
        return self.user.is_active and self.activation_key != ''

    @property
    def is_pending(self):
        return not self.user.is_active and self.activation_key != ''

    @property
    def is_deleted(self):
        return not self.user.is_active and self.activation_key == ''

    @property
    def is_valid(self):
        return self.user.email != ''

    @property
    def is_complete(self):
        return self.is_valid and self.is_active and self.activation_key == ''

    def is_social_auth(self):
        return self.user.social_auth.count() > 0

    def can_be_activated(self):
        return self.is_pending and (self.has_password() or self.is_social_auth())

    def has_password(self):
        return self.user.has_usable_password()

    def send_forgotten_password_email(self, request):
        from_address = self.get_from_address(request=request)
        self.send_activation_url(request, 'assetcloud/emails/user_forgotten_password.html',
                                 from_address, self.user.email)

    def reset_password(self, new_password):
        assert self.activation_key
        assert self.is_active

        self.user.set_password(new_password)
        self.activation_key = ''
        self.user.save()
        self.save()

    def delete_user(self, domain):
        if self.activation_key:
            self.activation_key = ''
        # Store user's email in original email
        self.original_email = self.user.email
        # Mung the email and username fields to 'delete' the user
        self.user.email = "deleted_%s@%s" % (self.user.id,
                                             int(time.time() * 1000))
        self.user.username = assetcloud_auth.email_to_username(self.user.email)
        self.user.is_active = False
        self.user.save()
        self.save()
        from_address = self.get_from_address(domain)
        send_mail('assetcloud/emails/user_deleted.html', from_address,
                  [self.original_email])

    def complete_profile(self, email='', request=None):
        original_email = self.user.email
        self.user.email = email
        self.user.save()
        self.is_registered = True
        if self.user.email != original_email:
            # User changed email from provider (or there wasn't one)
            # so they need to activate
            self.activation_key = ''  # Force reset of key
            self.send_activation_email(request)
        self.save()

    def ensure_tags(self, tags):
        self.visible_tags.set(*tags)

    def update_role(self, role):
        self.user.groups.clear()
        self.is_admin = False

        if role == BaseUserProfile.ROLE_ADMIN:
            self.user.groups.add(groups.account_admins)
            self.is_admin = True
        elif role == BaseUserProfile.ROLE_EDITOR:
            self.user.groups.add(groups.editors)
        elif role == BaseUserProfile.ROLE_VIEWER:
            pass
        else:
            raise UnknownUserTypeError('The user is not an admin, editor or viewer user.')

        # Only viewers can have tag restrictions applied to them
        if role != BaseUserProfile.ROLE_VIEWER:
            self.visible_tags.clear()

        self.save()

    def suspend(self):
        self.user.is_active = False
        self.user.save()

    def activate(self, request=None):
        self.activation_key = ''
        self.user.is_active = True
        self.save()
        self.user.save()
        if request:
            self.send_activated_email(request)

    def send_activated_email(self, request):
        from_address = self.get_from_address(request=request)
        login_url = '%s%s' % (site_url(request), reverse('login'))
        send_mail('assetcloud/emails/user_activated.html',
                  from_address, [self.user.email],
                  {'login_url': login_url})

    @property
    def activation_email_sent(self):
        return self._activation_email_sent

    def send_activation_email(self, request):
        if not self.activation_key:
            self.activation_key = BaseUserProfile.random_activation_key()
            self.save()
        from_address = self.get_from_address(request=request)
        self.send_activation_url(request,
                                 'assetcloud/emails/user_created.html',
                                 from_address, self.user.email)
        self._activation_email_sent = True

    def send_activation_url(self, request, email_template, from_address,
                            to_address):
        activation_url = '%s%s' % (site_url(request), self.activation_url)
        send_mail(email_template, from_address, [to_address],
                  {'activation_url': activation_url,
                   'user': self.user})

    @property
    def activation_url(self):
        if not self.activation_key:
            return None

        if self.is_pending:
            return reverse('activate-user', kwargs={'key': self.activation_key})
        elif self.forgotten_password:
            return reverse('password-reset', kwargs={'key': self.activation_key})
        else:
            assert False

    @staticmethod
    def register_new_user(account=None, email='', password=None, request=None, **kwargs):

        user = BaseUserProfile._create_admin_user(
            account=account,
            email=email,
            password=password,
            **kwargs)
        profile = user.get_profile()

        if not profile.is_active:
            if profile.is_valid:
                if request:
                    profile.is_registered = True
                    profile.save()
                    profile.send_activation_email(request)
                else:
                    logger.error('Could not send activation email because no request given')
            else:
                logger.error('Registering new user with invalid email? '
                              'Id: %s, Email: %s' % (profile.user.id,
                                                     profile.user.email))
        else:
            logger.error('Registering new user already active? '
                          'Id: %s' % profile.user.id)
        return user

    @staticmethod
    def initialise_social_auth_user(user):
        account = Account()
        account.save()

        user, profile = get_user_profile_class()._initialise_and_save_user(
            user, account,
            is_admin=True, is_editor=False,
            is_active=False,
            activation_key=BaseUserProfile.random_activation_key())
        return user

    @staticmethod
    def create_account_user(account=None, email='', password=None,
                            role="viewer",
                            request=None, tags=[],
                            **kwargs):
        """
        kwargs are passed to the user profile class's constructor
        """
        user = get_or_none(User, email=assetcloud_auth.emailcase(email))
        if role == "admin":
            kwargs['is_admin'] = True
        elif role == "editor":
            kwargs['is_editor'] = True
        if user is None:
            user = BaseUserProfile._create_user(account=account,
                                                email=email, password=password,
                                                **kwargs)
            profile = user.get_profile()

            # User is registered because they're just pending activation
            profile.is_registered = True
            profile.save()

            if profile.tags_allowed:
                profile.ensure_tags(tags)

            if not user.is_active:
                if request:
                    profile.send_activation_email(request)
                else:
                    logger.error('Could not send activation email because '
                                  'no request given')
            return user
        else:
            if user.get_profile().account.id == account.id:
                user = BaseUserProfile._recreate_user(user, request,
                                                  **kwargs)
            else:
                raise UserNotUniqueError('The given email exists for a '
                                         'user of a different account. '
                                         'Email: %s, Creator acc id: %s'
                                         'Target user acc id: %s' %
                                         (email, account.id,
                                          user.get_profile().account.id))
        return user

    @staticmethod
    def account_user_email_is_valid(email, account):
        user = get_or_none(User, email=assetcloud_auth.emailcase(email))
        return user and user.get_profile().is_deleted and user.get_profile().account == account

    @staticmethod
    def _recreate_user(user, request, is_admin=False):
        user.password = BaseUserProfile.random_password()
        user.is_active = False
        user.is_admin = is_admin
        user.save()
        user.get_profile().send_activation_email(request)
        return user

    @staticmethod
    def _create_admin_user(account=None,
                           email='',
                           password='',
                           **kwargs):

        return get_user_profile_class()._create_user(account=account,
                                                     email=email,
                                                     password=password,
                                                     is_admin=True,
                                                     **kwargs)

    @staticmethod
    def _create_user(account=None, email='', password='',
                     is_admin=False,
                     is_active=False,
                     activation_key=create_new_key,
                     is_editor=False,
                     **kwargs):
        if not is_active:
            if activation_key is create_new_key:
                activation_key = BaseUserProfile.random_activation_key()
        else:
            activation_key = ""

        email = assetcloud_auth.emailcase(email)
        user = get_or_none(User, email=email)
        if user:
            raise ValidationError('Cannot create user with same email: %s' % email)

        username = assetcloud_auth.email_to_username(email)
        user = User.objects.create_user(
            username=username, email=email, password=password)

        user, profile = get_user_profile_class()._initialise_and_save_user(
            user, account,
            is_admin=is_admin, is_editor=is_editor,
            is_active=is_active,
            activation_key=activation_key,
            **kwargs)
        return user

    @staticmethod
    def _initialise_and_save_user(user, account,
                                  is_admin, is_active, activation_key,
                                  is_editor=False,
                                  **kwargs):
        """
        Do user setup that is common to both social-auth and non-social-auth
        users.
        """
        user.is_admin = is_admin
        user.is_editor = is_editor
        user.is_active = is_active
        user.save()

        # Create default folder for user
        Folder.create_default_folder(user)

        # Create user's profile
        profile = BaseUserProfile._create_user_profile(
            user=user, account=account, is_admin=is_admin,
            is_editor=is_editor, activation_key=activation_key,
            **kwargs)

        return user, profile

    @staticmethod
    def _create_user_profile(user=None, **kwargs):
        profile = get_user_profile_class()(user=user, **kwargs)
        if kwargs.get('is_editor'):
            user.groups.add(groups.editors)
        elif kwargs.get('is_admin'):
            user.groups.add(groups.account_admins)
        profile.save()
        return profile

    @classmethod
    def get_from_address(cls, domain=None, request=None):
        if request and not domain:
            domain = get_current_site(request).domain
        if not domain:
            domain = settings.DOMAIN
        from_address = 'noreply@%s'
        if domain == settings.DOMAIN:
            return from_address % settings.DOMAIN
        else:
            return from_address % domain.partition(':')[0]

    @staticmethod
    def random_activation_key():
        return BaseUserProfile.random_key(max_field_length(BaseUserProfile,
                                                       'activation_key'))

    @staticmethod
    def random_shared_asset_key():
        return BaseUserProfile.random_key(max_field_length(Share,
                                                       'key'))

    @staticmethod
    def random_key(length):
        return srand.random_alphanumeric(length)

    @staticmethod
    def create_new_activation_key(user):
        assert user.is_active
        user_profile = user.get_profile()
        user_profile.activation_key = BaseUserProfile.random_activation_key()
        user_profile.save()

    @staticmethod
    def random_password():
        return random_alphanumeric(max_field_length(User,
                                                    'password'))


def _validate_add_tag_to_user_profile(user_profile):
    if not user_profile.tags_allowed:
        raise ValidationError(
            'Only viewer users (not %s users) may have tag restrictions' %
            user_profile.rolename)


def _is_a_user_profile(object):
    return ContentType.objects.get_for_model(get_user_profile_class()) ==\
           ContentType.objects.get_for_model(object)


def get_user_profile_class():
    return get_model(*settings.AUTH_PROFILE_MODULE.split('.', 1))


@receiver(pre_save, sender=taggit.models.TaggedItem)
def _validate_add_tag(sender, instance, raw, **kwargs):
    if not raw:
        if _is_a_user_profile(instance.content_object):
            _validate_add_tag_to_user_profile(instance.content_object)


class AccountCancellation(models.Model):
    account = models.ForeignKey(Account, related_name='cancellations',
                                blank=False)
    too_expensive = models.BooleanField(default=False, blank=True)
    budget = models.CharField(max_length=100, blank=True)
    doesnt_have_features = models.BooleanField(default=False, blank=True)
    missing_features = models.CharField(max_length=100, blank=True)
    found_something_better = models.BooleanField(default=False, blank=True)
    better_product = models.CharField(max_length=100, blank=True)
    dont_use_it_enough = models.BooleanField(default=False, blank=True)

    extra_detail = models.TextField(blank=True)
    should_keep_data = models.BooleanField(
        default=True,
        choices=((True, "OK, that's fine"),
                 (False, "No, please delete all my data as soon as you can")))

    def __unicode__(self):
        return unicode(self.account)


class Upload(models.Model):
    """
    A batch of uploaded assets.
    """
    added_by = models.ForeignKey(User, verbose_name='Uploaded by')
    added = models.DateTimeField(verbose_name='Date uploaded', auto_now_add=True)

    def __unicode__(self):
        return u'Upload added by %s on %s' % (self.added_by, self.added)


class AssetQuerySet(models.query.QuerySet):
    def account(self, account):
        return self.filter(AssetQuerySet.get_account_query(account))

    def with_any_tag(self, tags):
        if not tags:
            return self
        return self.filter(AssetQuerySet.get_tag_query(tags)).distinct()

    def for_user(self, user):
        return AssetQuerySet.filter_for_user(self, user).distinct()

    @staticmethod
    def get_account_query(account):
        return Q(account=account.id)

    @staticmethod
    def get_tag_query(tags):
        return Q(tags__in=[t.id for t in tags])

    @staticmethod
    def filter_for_user(queryset, user):
        profile = user.get_profile()
        queryset = queryset.filter(
            AssetQuerySet.get_account_query(profile.account))
        if not profile.all_tags_visible():
            queryset = queryset.filter(
                AssetQuerySet.get_tag_query(profile.visible_tags.all()))
        return queryset


class SizeCachingFileField(FileField):
    def __init__(self, size_field_name, *args, **kwargs):
        super(SizeCachingFileField, self).__init__(*args, **kwargs)
        self.size_field_name = size_field_name

    def pre_save(self, model_instance, add):
        """Returns field's value just before saving."""
        file = getattr(model_instance, self.attname)
        if file and not file._committed:
            setattr(model_instance, self.size_field_name, file.size)
        file = super(SizeCachingFileField, self).pre_save(model_instance, add)
        return file


size_caching_field_rules = [
  (
    (SizeCachingFileField,),
    [],
    {
        "size_field_name": ["size_field_name", {}],
    },
  )
]
add_introspection_rules(size_caching_field_rules, ["^assetcloud\.models\.SizeCachingFileField"])


class QuotaValidatingFileField(SizeCachingFileField):
    def validate(self, value, model_instance):
        super(QuotaValidatingFileField, self).validate(value, model_instance)
        file = getattr(model_instance, self.attname)
        if file and not file._committed:
            # Note: the fact that we subtract old_size here depends on this
            # code running before the pre_save receiver
            # _update_account_storage_pre_save. That does currently happen,
            # but this relies on the Django calling signal receivers in the
            # order that they are registered, which is undocumented behaviour
            # as far as I can tell.  If the order that Django calls signal
            # receivers changes then we're going to need to change our code.
            new_size = value.size
            old_size = getattr(model_instance, self.size_field_name)
            difference = new_size - old_size
            account = model_instance.account
            if account.would_be_over_storage_limit_by_adding(difference):
                args = map(filesizeformat, (new_size, account.storage, account.storage_limit,))
                raise ValidationError('Uploading this %s file would use too much storage (you are currently using %s of your %s limit)' %
                                      tuple(args))


add_introspection_rules([], ["^assetcloud\.models\.QuotaValidatingFileField"])


class Asset(models.Model):
    """
    A media file and it's metadata stored on AssetCloud.
    """
    upload = models.ForeignKey(Upload, related_name='assets')
    file = QuotaValidatingFileField(max_length=2048,
                                    size_field_name='file_size',
                                    upload_to='assets',
                                    storage=get_asset_storage())
    thumbnail = ImageField(upload_to='assets/thumbnails', storage=get_asset_storage(), blank=True, null=True)
    file_size = models.IntegerField(default=0)
    filename = models.CharField(max_length=256)
    title = models.CharField(max_length=256, default='', blank=True)
    description = models.TextField(default='', blank=True)
    created = models.DateTimeField(verbose_name='Date taken', default=None, null=True, blank=True)  # Currently unused
    added = models.DateTimeField(verbose_name='Date uploaded', auto_now_add=True)
    modified = models.DateTimeField(verbose_name='Last modified', auto_now=True)
    account = models.ForeignKey(Account, related_name='__assets')
    tags = TaggableManager(manager=AssetCloudTaggableManager)

    unrestricted_objects = PassThroughManager.for_queryset_class(AssetQuerySet)()

    def __init__(self, *args, **kwargs):
        # copy kwargs before (potentially) modifying it
        kwargs = kwargs.copy()
        # if filename is not passed then default to file.name
        if 'filename' not in kwargs and 'file' in kwargs:
            pathname = kwargs['file'].name
            filename = os.path.split(pathname)[1]
            kwargs['filename'] = filename
        super(Asset, self).__init__(*args, **kwargs)
        self._original_thumbnail = self.thumbnail

    def save(self, *args, **kwargs):
        val = super(Asset, self).save(*args, **kwargs)
        if self._original_thumbnail and self._original_thumbnail.name != self.thumbnail.name:
            try:
                thumbnail.delete(self._original_thumbnail)
            except thumbnail.helpers.ThumbnailError:
                logger.debug(
                    'Error deleting old asset thumbnail', exc_info=True)
        return val

    def delete(self, *args, **kwargs):
        self.account.storage -= self.file_size
        self.account.save()
        thumbnail.delete(self.file)
        if self.thumbnail:
            thumbnail.delete(self.thumbnail)
        super(Asset, self).delete(*args, **kwargs)
        get_asset_storage().delete(self.file.name)

    def save_to_temporary_file(self):
        # Todo: We'll need to come up with something better than this
        # Hopefully when serving directly from S3 this won't be needed
        out = tempfile.NamedTemporaryFile()
        self.file.seek(0)
        out.write(self.file.read())
        out.flush()
        self.file.seek(0)
        return out

    @property
    def basename(self):
        return self.filename

    @property
    def added_by(self):
        return self.upload.added_by

    @property
    def css_id(self):
        """
        The id that should be used in css elements representing this asset.
        """
        return 'asset-%d' % (self.id)

    @property
    def image_info(self):
        """
        Return various information about the image aspect of this asset.

        This information is derived from the file and is stored in the database,
        so if you access image_info this after the file has been changed you may
        get stale data.
        """
        # Use technique from https://code.djangoproject.com/ticket/10227#comment:5
        # to return None instead of raising DoesNotExist if there is no
        # AssetImageInfo for an asset
        try:
            return self._image_info
        except AssetImageInfo.DoesNotExist:
            return None

    @property
    def display_large_image(self):
        """
        Return True if the `file` for this Asset should be able to
        be previewed as a thumbnail.

        (IE: Do we expect sorl-thumbnail to be able to perform
        thumbnail conversion on the file?)
        """
        return self.image_info is not None

    @property
    def display_thumbnail(self):
        return self.thumbnail or self.display_large_image

    @property
    def thumbnail_source(self):
        if self.thumbnail:
            return self.thumbnail
        else:
            return self.file

    def get_list_thumbnail(self):
        """
        Return the small thumbnail of this asset as an image for use in a list
        """
        try:
            return self._get_thumbnail_form_field(self.thumbnail_source)
        except IOError:
            pass  # No thumbnail available

    def _get_thumbnail_form_field(self, image_field):
        return thumbnail.get_thumbnail(
            image_field,
            **assetcloud_settings.DEFAULT_LIST_THUMBNAIL_OPTIONS
        )

    @classmethod
    def precache_thumbnail(cls, instance, created, **kwargs):
        if created:
            # Force generation of a thumbnail by requesting it
            instance.get_list_thumbnail()

    @classmethod
    def objects(cls, user=None):
        return cls.unrestricted_objects.for_user(user)

    @staticmethod
    def infer_title(filename):
        root, ext = os.path.splitext(filename)
        return root

    def get_absolute_url(self):
        return reverse('asset', kwargs={"id": self.id})

    def __unicode__(self):
        return '%s (id: %d)' % (self.basename, self.id)


# We have both a pre_save and a post_save handler to maintain the denormalised
# account.storage total.
# It would be more efficient (1 db update vs 2 of them) to do it all in one
# handler, however:
# - if a new file is being saved then asset.file_size is not set yet in
#   pre_save
# - the old asset is not available in post_save because the database has
#   already been updated with the new data when post_save is called
def _update_account_storage_pre_save(sender, instance, raw, **kwargs):
    if not raw:
        if instance.id:
            old_version = Asset.unrestricted_objects.get(id=instance.id)
            logger.debug('Reducing account %d storage by %d' %
                         (instance.account.id, old_version.file_size))
            instance.account.storage -= old_version.file_size
            instance.account.save()


@receiver(post_save, sender=Asset)
def _update_account_storage_post_save(sender, instance, raw, **kwargs):
    if not raw:
        logger.debug('Increasing account %d storage by %d' %
                     (instance.account.id, instance.file_size))
        instance.account.storage += instance.file_size
        instance.account.save()


@receiver(post_save, sender=Asset)
def initialise_required_metadata(sender, instance, raw, **kwargs):
    for asset_metadata_model in app_settings.ASSET_METADATA_MODELS:
        metadata_model, metadata_form = get_metadata_model_and_form_classes(asset_metadata_model)
        if hasattr(metadata_model, '_metadata_meta'):
            if metadata_model._metadata_meta.create_on_save:
                metadata_model.objects.get_or_create(asset=instance)


class AssetImageInfo(models.Model):
    asset = models.OneToOneField(Asset, primary_key=True,
                                 related_name='_image_info')
    height = models.IntegerField()
    width = models.IntegerField()

    @staticmethod
    def create_for_asset(asset):
        if not AssetImageInfo._is_unsupported_image_type(asset):
            mimetype, encoding = mimetypes.guess_type(asset.filename)
            if mimetype and mimetype.split('/')[0] == 'image':
                if asset.get_list_thumbnail():
                    width, height = Image.open(asset.file).size
                    asset.file.seek(0)
                    aii = AssetImageInfo(asset=asset,
                                         height=height,
                                         width=width)
                    aii.save()
                    return aii

    @staticmethod
    def _is_unsupported_image_type(asset):
        (filename, extension) = os.path.splitext(asset.filename)
        extension = extension.lower()

        image_extensions_not_supported_by_sorl = ['.tif', '.tiff', '.psd']

        if extension in image_extensions_not_supported_by_sorl:
            return True

        return False


class Share(models.Model):
    expiry = models.DateTimeField(blank=True, null=True)
    key = models.CharField(default='', max_length=32, blank=True)
    message = models.TextField(blank=True)

    def __unicode__(self):
        return u'Share %s with key %s (expires %s)' % (self.id, self.expiry, self.key)

    def get_absolute_url(self):
        return reverse('share', kwargs={'share_id': self.id, 'key': self.key})


class SharedAsset(models.Model):
    share = models.ForeignKey(Share, related_name='shared_assets')
    asset_id = models.IntegerField()

    def __init__(self, *args, **kwargs):
        if 'asset' in kwargs:
            kwargs = kwargs.copy()
            asset = kwargs.pop('asset')
            kwargs['asset_id'] = asset.id
        super(SharedAsset, self).__init__(*args, **kwargs)

    def download_url(self):
        return reverse('shared_asset_download_action', kwargs={
            'share_id': self.share.id,
            'key': self.share.key,
            'asset_id': self.asset_id,
        })

    def __unicode__(self):
        return u'Share of Asset %d in Share %s' % (self.asset_id, self.share.id)


class Folder(models.Model):
    """
    A folder for storing assets
    """
    name = models.TextField()
    owner = models.ForeignKey(User, related_name='folders')
    assets = models.ManyToManyField(Asset, related_name='folders')

    def __unicode__(self):
        return u'%s (owned by %s)' % (self.name, self.owner)

    def contains(self, asset):
        return self.assets.filter(pk=asset.pk).exists()

    @staticmethod
    def create_default_folder(owner):
        folder = Folder(name='Favourites', owner=owner)
        folder.save()
        return folder


class IndexState(models.Model):
    updated = models.DateTimeField(verbose_name='Last updated')


class AssetDownloadLog(models.Model):

    def __unicode__(self):
        return "%s by %s" % (str(self.asset), str(self.get_user_display()))

    asset = models.ForeignKey(Asset, related_name="downloads")
    user = models.ForeignKey(User, related_name="downloads", null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def get_user_display(self):
        if self.user:
            return str(self.user)
        else:
            return "Public User"

    @staticmethod
    def log_download(asset, user, save=True):
        download_user = user
        if not user.is_authenticated():
            download_user = None

        log = AssetDownloadLog(
            asset=asset,
            user=download_user,
        )

        if save:
            log.save()

        return log


@receiver(m2m_changed, sender=Folder.assets.through)
def _validate_add_asset_to_folder(action=None, instance=None, pk_set=None,
                                  model=None, **kwargs):
    if pk_set:
        if model == Asset:
            assets = Asset.unrestricted_objects.filter(pk__in=pk_set)
            for asset in assets:
                if asset.account != instance.owner.get_profile().account:
                    raise ValidationError('Assets must be from same account as folder. Asset: %s, folder: %s, asset account: %s, folder account: %s' % (asset.pk, instance.pk, asset.account.pk, instance.owner.get_profile().account.pk))


def _reindex_asset(asset):
    from assetcloud.search_indexes import reindex_asset_maybe_later
    reindex_asset_maybe_later(asset)


@receiver(m2m_changed, sender=Folder.assets.through)
def _reindex_asset_for_folder(action=None, instance=None, pk_set=None,
                              model=None, **kwargs):
    if model == Asset and action in ['post_add', 'post_clear', 'post_remove']:
        if pk_set:
            assets = Asset.unrestricted_objects.filter(pk__in=pk_set)
            for asset in assets:
                _reindex_asset(asset)


def _reindex_for_tags(**kwargs):
    if not getattr(kwargs, 'raw', False):
        if kwargs['instance'].content_type == ContentType.objects.get_for_model(Asset):
            asset = kwargs['instance'].content_object
            _reindex_asset(asset)

models.signals.post_save.connect(_reindex_for_tags,
                                 sender=taggit.models.TaggedItem)
models.signals.post_delete.connect(_reindex_for_tags,
                                 sender=taggit.models.TaggedItem)
models.signals.post_save.connect(Asset.precache_thumbnail, sender=Asset)


validate_on_save.validate_models_on_save('assetcloud')
# Need to _update_account_storage_pre_save after validate_models_on_save so that
# _update_account_storage_pre_save, which alters account.storage, only runs if
# validation passes
pre_save.connect(_update_account_storage_pre_save, sender=Asset)


from south.modelsinspector import add_ignored_fields
add_ignored_fields(["^assetcloud.models.CustomTaggableManager"])
