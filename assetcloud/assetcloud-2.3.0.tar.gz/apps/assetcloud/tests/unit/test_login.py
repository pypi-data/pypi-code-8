# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
Unit Tests for login.

Tests in this module are unit tests, and therefore:
 - must run quickly,
 - must have minimal dependencies (for example, they must not use a database).
"""
from django.conf import settings
from django.test.utils import override_settings
from django.core.urlresolvers import reverse, resolve

from assetcloud.middleware import LoginRequiredMiddleware
from assetcloud.models import get_user_profile_class
from assetcloud.tests.contract.utils import TNABotContractTest
from .utils import UnitTestCase


UserProfile = get_user_profile_class()


class MockUserProfile(object):
    def __init__(self):
        self.account = 'Hello World, I am a string pretending to be a account.'


class MockUser(object):
    def __init__(self, anonymous, is_active):
        self.anonymous = anonymous
        self.profile = MockUserProfile()
        self.is_active = not anonymous if is_active is None else is_active

    def is_anonymous(self):
        return self.anonymous

    def get_profile(self):
        if self.profile is None:
            raise UserProfile.DoesNotExist()
        return self.profile


class MockRequest(object):
    def __init__(self, path, anonymous=True, is_active=None):
        self.path = path
        self.user = MockUser(anonymous, is_active)


class LoginRequiredMiddlewareTests(UnitTestCase):
    """
    Unit tests for LoginRequiredMiddleware.
    """

    def test_login_not_required_for_static(self):
        self._assert_login_not_required_for_path(
            'static/foo.png', resolve_path=False)

    @override_settings(PUBLIC_URLS=('public', '^open/', '^justthis$'))
    def test_login_not_required_for_path_matched_by_public_urls_setting(self):
        self._assert_login_not_required_for_path(
            '/publicsuffix', resolve_path=False)
        self._assert_login_not_required_for_path(
            '/prefixpublic', resolve_path=False)

        self._assert_login_not_required_for_path(
            '/open/foo', resolve_path=False)
        self._assert_login_required_for_path(
            '/prefixopen/foo', resolve_path=False)

        self._assert_login_not_required_for_path(
            '/justthis', resolve_path=False)
        self._assert_login_required_for_path(
            '/prefixjustthis', resolve_path=False)
        self._assert_login_required_for_path(
            '/justthissuffix', resolve_path=False)

    # Test that login is required for a somewhat random set of URLs
    def test_login_required_for_home(self):
        self._assert_login_required_for_path(reverse('home'))

    def test_login_required_for_assets(self):
        self._assert_login_required_for_path(reverse('asset-list'))

    def test_login_required_for_upload(self):
        self._assert_login_required_for_path(reverse('asset-upload'))

    def test_login_required_for_arbitrary_path(self):
        self._assert_login_required_for_path(
            'abcdef', resolve_path=False)

    @override_settings(LOGIN_URL="alternative_login")
    def test_login_required_does_not_cause_redirect_loop_on_alternative_login(self):
        self._assert_login_not_required_for_path(
            settings.LOGIN_URL, resolve_path=False)

    @TNABotContractTest
    def test_login_not_required_for_public_view(self):
        # support_thank_you is an arbitrarily-chosen view decorated
        # with assetcloud.views.decorators.public
        url = reverse('forgotten-password')
        self._assert_login_not_required_for_path(url)

    def test_login_not_required_if_already_logged_in(self):
        middleware = LoginRequiredMiddleware()

        response = middleware.process_view(MockRequest(reverse('home'), anonymous=False),
                                           _fake_view, (), {})
        self.assertIsNone(response)

    @TNABotContractTest
    def test_access_is_prevented_if_user_account_is_not_active(self):
        middleware = LoginRequiredMiddleware()

        response = middleware.process_view(MockRequest(reverse('home'), anonymous=False, is_active=False),
                                       _fake_view, (), {})

        self._assert_response_required_login_for_path(response, reverse("home"))

    def test_middleware_adds_account_to_request(self):
        middleware = LoginRequiredMiddleware()

        request = MockRequest(reverse('home'), anonymous=False)
        middleware.process_view(request,
                                _fake_view, (), {})
        #noinspection PyUnresolvedReferences
        self.assertEqual('Hello World, I am a string pretending to be a account.', request.account)

    def test_middleware_survives_no_user_profile_on_public_paths(self):
        middleware = LoginRequiredMiddleware()
        request = MockRequest('/static/foo.img', anonymous=False)
        request.user.profile = None
        try:
            middleware.process_view(request,
                                    _fake_view, (), {})
        except ValueError as e:
            self.fail('Middleware raised %s on no user profile' % e)

    def test_middleware_sets_account_on_reserved_paths(self):
        middleware = LoginRequiredMiddleware()
        request = MockRequest('/accounts', anonymous=False)
        middleware.process_view(request,
                                _fake_view, (), {})
        self.assertEqual('Hello World, I am a string pretending to be a account.', request.account)

    def _assert_login_required_for_path(self, path, resolve_path=True):
        view_func, args, kwargs = self._maybe_resolve(path, resolve_path)
        middleware = LoginRequiredMiddleware()
        response = middleware.process_view(
            MockRequest(path), view_func, args, kwargs)
        self._assert_response_required_login_for_path(response, path)

    def _assert_response_required_login_for_path(self, response, path):
        self.assertIsNotNone(response, ('LoginRequiredMiddleware should have returned a redirect for "%s", but it returned None' % path))
        self.assertEqual(302, response.status_code)
        self.assertEqual(settings.LOGIN_URL + '?next=' + path, response['Location'])

    def _assert_login_not_required_for_path(self, path, resolve_path=True):
        view_func, args, kwargs = self._maybe_resolve(path, resolve_path)
        middleware = LoginRequiredMiddleware()
        response = middleware.process_view(
            MockRequest(path), view_func, args, kwargs)
        self.assertIsNone(response)

    def _maybe_resolve(self, path, resolve_path):
        if resolve_path:
            match = resolve(path)
            view_func, args, kwargs = match
        else:
            view_func, args, kwargs = _fake_view, (), {}
        return view_func, args, kwargs


def _fake_view():
    return None
