# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
Utility methods and base classes for service tests.
"""
from assetcloud import random_utils
from assetcloud.models import Asset, Account, OrganisationType, get_asset_storage, ProxyTag, AssetImageInfo, get_user_profile_class
from assetcloud.upload_history import upload_asset
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.messages.storage import default_storage
from django.core import management
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.db.models import get_models
from django.test.client import RequestFactory
from social_auth.models import UserSocialAuth
import django.test
import os
import shutil
import tempfile

UserProfile = get_user_profile_class()


def list_media_files(dirname):
    """
    Return a list of pathnames of all the files in the cache.
    """
    cache_dir = os.path.join(settings.MEDIA_ROOT, dirname)

    if not os.path.exists(cache_dir):
        return []

    cache_files = []
    for (dirpath, dirnames, filenames) in os.walk(cache_dir):
        for filename in filenames:
            cache_files.append(os.path.join(dirpath, filename))
    return cache_files


def create_fake_request(user=None, path='/'):
    """ Create a fake request object suitable for use with the messages framework"""
    rf = RequestFactory()
    request = rf.get(path)
    request.user = user
    request.GET = {}
    request.POST = {}

    # RequestFactory does not support middleware, so we need to set up the
    # session and _messages attributes ourselves instead of relying on the
    # session and messages middlewares to do it. See
    # https://code.djangoproject.com/ticket/17971
    request.session = {}
    request._messages = default_storage(request)

    return request


def create_account(name=None, org_type=None, subdomain=None):
    """
    Create, save, and return a new account instance.
    """
    if name is None:
        name = random_utils.random_domain(suffix='')
    account = Account(name=name, organisation_type=org_type,
                      subdomain=subdomain)
    account.save()
    return account


def create_organisation_type(name=None):
    if name is None:
        name = random_utils.random_alphanumeric()
    org_type = OrganisationType(name=name)
    org_type.save()
    return org_type


def create_user(account=None, email=None, password=None, is_admin=False,
                is_editor=False, is_active=True, has_activation_key=False,
                force_null_password=False, social_auth=False, tags=[],
                **kwargs):
    """
    Create, save, and return a new user instance.
    """

    test_user_defaults = getattr(settings, "CREATE_TEST_USER_DEFAULTS", {}).copy()
    test_user_defaults.update(kwargs)

    if account is None:
        account = create_account()
    if email is None:
        email = random_utils.random_email()
    if password is None and not force_null_password:
        password = random_utils.random_alphanumeric()
    if has_activation_key:
        activation_key = UserProfile.random_activation_key()
    else:
        activation_key = ''

    user = UserProfile._create_user(
        account=account, email=email, password=password, is_admin=is_admin,
        is_editor=is_editor, is_active=is_active, activation_key=activation_key,
        **test_user_defaults)
    user.plaintext_password = password
    if social_auth:
        social_auth_user = UserSocialAuth(user_id=user.id,
                                          provider='test auth',
                                          uid=random_utils.random_alphanumeric(25),
                                          extra_data='{"extra":"extras"}')
        social_auth_user.save()

    # Adding tags can only happen once we have a user
    if tags:
        user.get_profile().visible_tags.add(*tags)

    return user


def create_viewer(*args, **kwargs):
    kwargs['is_editor'] = False
    kwargs['is_admin'] = False
    return create_user(*args, **kwargs)


def create_editor(*args, **kwargs):
    kwargs['is_editor'] = True
    kwargs['is_admin'] = False
    return create_user(*args, **kwargs)


def create_admin(*args, **kwargs):
    kwargs['is_editor'] = False
    kwargs['is_admin'] = True
    return create_user(*args, **kwargs)


def create_super_admin(*args, **kwargs):
    user = create_admin(*args, **kwargs)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    return user


def create_tag(tag):
    tag = ProxyTag(name=tag)
    tag.save()
    return tag


def create_asset(account=None, user=None,
                 file_obj=None, filename=None, content_length=None,
                 title=None, description=None, tags=None, added=None,
                 upload=None, thumbnail_obj=None):
    """
    Create, save, and return a new asset instance.
    """
    if account is None:
        account = user and user.get_profile().account or create_account()
    if user is None:
        user = create_editor(account=account)
    if file_obj is None:
        file_obj = random_utils.random_file_obj(content_length=content_length,
                                         filename=filename)

    # Don't pass args that are None, because that causes Django to explicitly
    # try to save NULL to the database instead of using the default value for
    # the model field. That causes not-null constraint violations when
    # PostgreSQL is being used.
    kwargs = {}
    if title:
        kwargs['title'] = title
    if description:
        kwargs['description'] = description
    if thumbnail_obj:
        kwargs['thumbnail'] = File(thumbnail_obj)

    asset = Asset(file=File(file_obj), account=account,
                  **kwargs)
    upload_asset(asset, upload=upload, added_by=user)
    if added:
        asset.added = added
        asset.save()

    # Adding tags can only happen once we have an asset instance
    if tags:
        asset.tags.add(*tags)
        asset.save()

    return asset


def create_image_asset_with_thumbnail(thumbnail_filename=None, thumbnail_suffix=".png", **kwargs):
    thumbnail_obj = random_utils.random_image_file(thumbnail_filename, thumbnail_suffix)
    return create_image_asset(thumbnail_obj=thumbnail_obj, **kwargs)


def create_image_asset(filename=None, suffix='.png', **kwargs):
    """
    A new asset instance, with a random image file.
    """
    file_obj = random_utils.random_image_file(filename, suffix)
    asset = create_asset(file_obj=file_obj, **kwargs)
    AssetImageInfo.create_for_asset(asset)
    return asset


def create_text_asset(filename=None, suffix='.txt', **kwargs):
    """
    A new asset instance, with a random text file.
    """
    file_obj = random_utils.random_text_file(filename, suffix)
    return create_asset(file_obj=file_obj, **kwargs)


def get_last_added_user():
    return User.objects.order_by('-id')[0]


def get_last_added_account():
    return Account.objects.order_by('-id')[0]


def get_html_content(email_message):
    for (content, mime_type) in email_message.alternatives:
        if mime_type == 'text/html':
            return content
    raise ValueError('No text/html alternative found in email %s' % email_message)


class LoginFailedException(Exception):
    pass


class TestClient(django.test.client.Client):
    """
    The standard Django test client, with some slight modifications to
    make logging in easier.
    """

    def __init__(self, *args, **kwargs):
        super(TestClient, self).__init__(*args, **kwargs)
        self.logged_in_user = None

    def login(self, user=None,
              account=None, same_account_as_user=None, admin=True,
              email=None, password=None):
        """
        Returns the user instance, or raises an exception if it cannot login.
        If an existing user is already logged in, then log that user out first.

        Usage:
          login() - login, creating a new account and admin user if needed.
          login(user) - login, using a user created by `create_user`.
          login(account, admin) - login, creating a user.
          login(same_account, admin) - login, creating a user.
          login(email=email, password=password) - login explicitly.
        """
        if self.logged_in_user:
            self.logout()

        if user is None and email is None and password is None:
            if same_account_as_user:
                account = same_account_as_user.get_profile().account
            user = create_user(account=account, is_admin=admin)

        if user is not None:
            email = user.email
            password = user.plaintext_password

        if not super(TestClient, self).login(username=email,
                                             password=password):
            raise LoginFailedException('Could not log in (email "%s", '
                                       'password "%s")' % (email, password))

        if user is None:
            user = authenticate(username=email, password=password)

        self.logged_in_user = user
        return user

    def logout(self):
        super(TestClient, self).logout()
        self.logged_in_user = None


role_creators = {'viewer': create_viewer,
                 'editor': create_editor,
                 'admin': create_admin}


def login_and_make_request(self, role_test_class, role_name):
    self.user = role_creators[role_name]()
    self.account = self.user.get_profile().account
    self.client.login(self.user)
    role_test = role_test_class()
    role_test.given(self)
    response = role_test.when(self)
    return response, role_test


def make_role_can_method(role_test_class, role_name):
    """
    Makes a test method to add to the OUTER test case class (not the inner
    RoleTest subclass) that tests that a particular role can perform the action.
    """
    def can_method(self):
        response, role_test = login_and_make_request(
            self, role_test_class, role_name)

        role_test.assertCan(role_name, self, response)
    return can_method


def make_role_cant_method(role_test_class, role_name):
    """
    Makes a test method to add to the OUTER test case class (not the inner
    RoleTest subclass) that tests that a particular role is forbidden from
    performing the action.
    """
    def cant_method(self):
        response, role_test = login_and_make_request(
            self, role_test_class, role_name)

        role_test.assertCant(role_name, self, response)
    return cant_method


def create_role_tests(role_test_class_name, role_test_class):
    d = {}
    new_method_stem = 'test_%s' % role_test_class_name[8:].lower()
    for role in role_creators.keys():
        new_method_name = '%s_%s' % (new_method_stem,
                                     role)
        if role in role_test_class.can:
            new_method_name += '_can'
            d[new_method_name] = make_role_can_method(role_test_class, role)
        else:
            new_method_name += '_cant'
            d[new_method_name] = make_role_cant_method(role_test_class, role)
    return d


class RoleTestCaseCreator(type):
    """
    Metaclass that looks inside its class for inner classes whose names start
    with RoleTest and adds test methods based on these inner classes to the
    main (outer) class.
    """
    def __new__(cls, classname, bases, class_dict):
        if class_dict.get('needs_index'):
            class_dict['tags'] = class_dict.get('tags', []) + ['index']
        for key in class_dict.keys()[:]:
            if key.startswith('RoleTest'):
                class_dict.update(create_role_tests(key, class_dict[key]))
        return super(RoleTestCaseCreator, cls).__new__(cls, classname, bases, class_dict)


class MediaRootMover(object):
    """
    Relocates MEDIA_ROOT to a temp dir to avoid leaving test files in
    MEDIA_ROOT.

    Intended to be called from setUp() / tearDown() methods in TestCase
    subclasses.
    """

    def setup_temp_media_root(self):
        """
        Create a clean MEDIA_ROOT and force all models to use that for
        uploaded files.
        """
        self.tmp_dir = tempfile.mkdtemp(prefix='django-test-')
        settings.MEDIA_ROOT = os.path.join(self.tmp_dir, 'media')

        # We need to reset the storage on any class that uses it.
        for model in get_models():
            # Don't replace asset storage if it's not filesystem
            if model == Asset().__class__ and not isinstance(get_asset_storage(), FileSystemStorage):
                continue

            for field in model._meta.fields:
                if not getattr(field, 'storage', None):
                    continue

                field.storage = FileSystemStorage(location=settings.MEDIA_ROOT)

    def teardown_temp_media_root(self):
        """
        Remove the temporary MEDIA_ROOT and any uploaded files inside it.
        """
        shutil.rmtree(self.tmp_dir)


class TestCase(django.test.TestCase):
    """
    Base for all test cases which require the full Django development server
    stack, including the test client.
    """
    __metaclass__ = RoleTestCaseCreator
    tags = ['service', ]
    # By default Haystack indexing is disabled during tests. Set this to True
    # in your subclass to enable indexing.
    needs_index = False
    temp_media_root = True
    client_class = TestClient

    @classmethod
    def setUpClass(cls):
        super(TestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(TestCase, cls).tearDownClass()

    def create_editor_and_login(self):
        self.account = create_account()
        self.user = create_editor(account=self.account)
        self.client.login(self.user)

    def create_viewer_and_login(self):
        self.account = create_account()
        self.user = create_viewer(account=self.account)
        self.client.login(self.user)

    def create_admin_and_login(self):
        self.account = create_account()
        self.user = create_admin(account=self.account)
        self.client.login(self.user)

    def create_super_admin_and_login(self):
        self.account = create_account()
        self.user = create_super_admin(account=self.account)
        self.client.login(self.user)

    def setUp(self):
        """
        Make sure we have a clean environment prior to each test case.
        """
        super(TestCase, self).setUp()

        if self.temp_media_root:
            self.media_root_mover = MediaRootMover()
            self.media_root_mover.setup_temp_media_root()

        if self.needs_index:
            management.call_command('rebuild_index', remove=True,
                                    interactive=False, verbosity=0)

    def tearDown(self):
        """
        Clean up after each test case.
        """
        super(TestCase, self).tearDown()

        if self.temp_media_root:
            self.media_root_mover.teardown_temp_media_root()

    def assertStringContains(self, containing, contained):
        self.assertGreaterEqual(
            containing.find(contained),
            0,
            msg="'%s' does not contain '%s'" % (containing, contained))

    def assertCanLogin(self, *args, **kwargs):
        try:
            self.client.login(*args, **kwargs)
        except LoginFailedException, exc:
            self.fail(exc.message)
        self.client.logout()

    def assertCannotLogin(self, *args, **kwargs):
        try:
            user = self.client.login(*args, **kwargs)
            self.fail("User '%s' was logged in." % (user.email,))
        except LoginFailedException:
            pass

    def assertPksEqualIgnoreOrder(self, l1, l2):
        self.assertSetEqual({l.pk for l in l1},
                            {l.pk for l in l2})

    def assertResponseContains(self, string, response):
        self.assertIn(string, response.content)

    def assertFilesEqual(self, file1=None, file2=None):
        file1.seek(0)
        file2.seek(0)
        self.assertEquals(file1.read(), file2.read())

    def assertImagePathsEqual(self, first, second):
        self.assertEqual(self.get_url_without_parameters(first), self.get_url_without_parameters(second))

    def assertImagePathsNotEqual(self, first, second):
        try:
            self.assertImagePathsEqual(first, second)
            self.fail("Image paths should not match")
        except AssertionError:
            return

    def get_url_without_parameters(self, url):
        return url.split("?")[0]


class RoleTest(object):
    """
    Superclass for RoleTest classes that get transformed into test methods on
    their outer class by RoleTestCaseCreator.

    Attributes:
    can:    roles that should have permission to do the action being tested
    cant:   roles that should not have permission to do the action being tested

    can has precedence over can't, so subclasses just need to override
    can with the roles that should have permission.

    RoleTestCaseCreator will generate a test method for each role mentioned in
    can or cant. For each role mentioned in can this test method will:
     - create and log in as a user who has that role
     - call given(test)
     - call when(test) (where test is an instance of the outer TestCase class)
     - call assertCan(role_name, test, response)
     - assertCan will fail if the status code is 403
     - otherwise assertCan will call role_can(test, response).
    For each role mentioned in cant this method will:
     - create and log in as a user who has that role
     - call given(test)
     - call when(test)
     - call assertCant(role_name, test, response)
     - assertCant will fail if the status code is not 403
     - otherwise assertCant will call role_cant(test, response).

    Often there will be no need to override role_cant because the 403 check
    for cant roles will be sufficient. If you need more precise checking
    (i.e. not just testing for 403) override assertCan or assertCant

    The method name "when" was chosen to reflect the "given-when-then" pattern.

    The "given" role is played by setUp() methods in outer classes and the
    given() method in RoleTest subclasses.

    The "then" role is played in part by the automatic check of the status code,
    and partly by the role_can and role_cant methods.
    """
    can = []
    cant = ['admin', 'viewer', 'editor']

    def given(self, test):
        pass

    def role_can(self, test, response):
        pass

    def role_cant(self, test, response):
        pass

    def assertCan(self, role_name, test, response):
        if response.status_code == 403:
            test.fail('%s should be able to do this: %s' %
                      (role_name, self.__class__))
        else:
            self.role_can(test, response)

    def assertCant(self, role_name, test, response):
        if response.status_code != 403:
            test.fail('%s should not be able to do this: %s' %
                      (role_name, self.__class__))
        else:
            self.role_cant(test, response)


class LoggedInTestCase(TestCase):
    def setUp(self):
        super(LoggedInTestCase, self).setUp()
        self.create_user_and_login()

    def create_user_and_login(self):
        self.create_editor_and_login()

    def create_asset(self, account=None, user=None, **kwargs):
        """
        Create an asset in the logged in user's account
        """
        if account is None:
            account = self.account
        if user is None:
            user = self.user
        return create_asset(account=account, user=user, **kwargs)


class AdminLoggedInTestCase(LoggedInTestCase):
    def setUp(self):
        super(AdminLoggedInTestCase, self).setUp()
        self.create_user_and_login()

    def create_user_and_login(self):
        self.create_admin_and_login()


class SuperAdminLoggedInTestCase(AdminLoggedInTestCase):
    def create_user_and_login(self):
        self.create_super_admin_and_login()


class ViewerLoggedInTestCase(LoggedInTestCase):
    def setUp(self):
        super(ViewerLoggedInTestCase, self).setUp()
        self.create_user_and_login()

    def create_user_and_login(self):
        self.create_viewer_and_login()


def with_delete_zf(fn):
    """Decorator to automatically cleanup prepared zips"""
    def wrapped_fn(self, *args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        finally:
            try:
                if self.client.session.get('zip_file'):
                    os.remove(self.client.session['zip_file'])
            except (IOError, OSError):
                pass
    return wrapped_fn
