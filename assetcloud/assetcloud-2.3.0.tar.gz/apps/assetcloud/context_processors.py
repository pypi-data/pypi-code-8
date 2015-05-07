from django.utils.translation import to_locale, get_language
from assetcloud.models import Account, DEFAULT_COLOURS, Asset
from django.conf import settings
import logging
import re


log = logging.getLogger('assetcloud')


def custom_colours(request):
    """
    Sets context variables to the custom colours for the user's account, or
    defaults if the account doesn't have any or the user is not logged in.
    """
    extra_context = DEFAULT_COLOURS.copy()
    account = getattr(request, 'account', None)
    if not account and 'HTTP_HOST' in request.META:
        host = request.META['HTTP_HOST']
        subdomain = re.sub('\.' + settings.DOMAIN_SUFFIX + '(:[0-9]+)?$', '', host)
        try:
            account = Account.objects.get(subdomain=subdomain)
            extra_context['subdomain_matches_account'] = True
        except Account.DoesNotExist:
            pass
    if account:
        for field_name in Account.COLOUR_FIELD_NAMES:
            colour = getattr(account, field_name)
            if colour:
                extra_context[field_name] = colour
        if account.logo:
            extra_context['header_logo'] = account.logo
    return extra_context


def locale(request):
    return {'LOCALE': to_locale(get_language())}


def google_analytics(request):
    return {'GOOGLE_ANALYTICS_KEY': settings.GOOGLE_ANALYTICS_KEY}


def permissions(request):
    d = {'can_edit_assets': False,
         'is_admin': False}
    try:
        if request.user:
            d['can_edit_assets'] = request.user.get_profile().can_edit_assets()
            d['is_admin'] = request.user.get_profile().has_account_admin_permission()
    except AttributeError:
        pass
    return d


def no_assets(request):
    d = {'no_assets_at_all': False}
    # Use unrestricted objects here to truly tell if any assets exist
    if request.user and not request.user.is_anonymous():
        if not Asset.unrestricted_objects.account(request.user.get_profile().account).exists():
            d['no_assets_at_all'] = True
    return d


def testing(request):
    # Animations used by 'fade' CSS class cause intermittent failures of
    # Selenium tests, so we don't use the 'fade' class during
    # testing. Instead of referring to the fade css class directly templates
    # should use the 'fade_class' variable, which will be set to 'fade'
    # usually and '' during testing. It isn't ideal to change the behaviour
    # of the application during testing but we have spent a lot of time
    # trying to come up with another solution without managing to find a
    # reliable one.
    if settings.TESTING:
        fade_class = ''
    else:
        fade_class = 'fade'

    return {'fade_class': fade_class}


def project_name(request):
    return {'PROJECT_NAME': settings.PROJECT_NAME}
