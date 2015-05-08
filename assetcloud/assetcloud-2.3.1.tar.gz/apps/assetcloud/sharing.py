# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from assetcloud import site_url
from assetcloud.models import Asset, SharedAsset, Share, get_user_profile_class
from assetcloud.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
import datetime
import logging

UserProfile = get_user_profile_class()

logger = logging.getLogger(__name__)


class SharingStatus:
    STATUS_VALID = 'valid'
    STATUS_EXPIRED = 'expired'
    STATUS_ASSET_NOT_FOUND = 'asset_not_found'
    # There is no 'bad key' status because instead of returning such a status
    # check_share_status raises PermissionDenied
    #STATUS_BAD_KEY = 'bad_key'

    def __init__(self, status, share=None, asset=None, shared_asset=None):
        self.status = status
        self.share = share
        self.asset = asset
        self.shared_asset = shared_asset

    @staticmethod
    def create_valid_for_share(share):
        """
        Create a valid SharingStatus for a share as a whole (not a particular
        asset).
        """
        return SharingStatus(SharingStatus.STATUS_VALID, share)

    @staticmethod
    def create_valid_for_asset(share, shared_asset, asset):
        """
        Create a valid SharingStatus for a particular asset.
        """
        return SharingStatus(SharingStatus.STATUS_VALID,
                             share=share, shared_asset=shared_asset, asset=asset)

    # Next 2 don't put the asset into the SharingStatus to try to reduce the
    # risk of the asset accidentally being shared
    @staticmethod
    def create_asset_not_found(share, shared_asset):
        return SharingStatus(SharingStatus.STATUS_ASSET_NOT_FOUND,
                             share=share,
                             shared_asset=shared_asset)

    @staticmethod
    def create_expired(share):
        return SharingStatus(SharingStatus.STATUS_EXPIRED, share=share)

    @property
    def valid(self):
        return self.status == self.STATUS_VALID

    @property
    def asset_not_found(self):
        return self.status == self.STATUS_ASSET_NOT_FOUND


def check_share_status(share_id, key):
    """
    Raise PermissionDenied if it looks like someone is doing something nasty
    (e.g. key was never valid).

    Otherwise return the status of the share if it is valid or if it is invalid
    for an innocent reason (asset deleted or key has expired).
    """
    share_id = int(share_id)
    try:
        share = Share.objects.get(id=share_id, key=key)
    except Share.DoesNotExist:
        logger.error('Somebody tried to use an invalid share ID and sharing key, '
                     'they are probably trying to do something nasty. '
                     'share_id = %s, key = %s',
                     share_id, key)
        raise PermissionDenied()

    if not share.expiry or datetime.datetime.now() < share.expiry:
        return SharingStatus.create_valid_for_share(share)
    else:
        return SharingStatus.create_expired(share)


def check_asset_share_status(share_id, key, asset_id):
    status = check_share_status(share_id, key)
    if not status.valid:
        return status

    share = status.share

    try:
        shared_asset = SharedAsset.objects.get(share=share, asset_id=asset_id)
    except SharedAsset.DoesNotExist:
        logger.error('Somebody tried to use download an asset that was not part of the specified share, '
                     'they are probably trying to do something nasty. '
                     'share_id = %s, key = %s, asset_id = %s',
                     share_id, key, asset_id)
        raise PermissionDenied()

    try:
        asset = Asset.unrestricted_objects.get(pk=asset_id)
        status.asset = asset
    except Asset.DoesNotExist:
        return SharingStatus.create_asset_not_found(share, shared_asset)

    return status


def all_asset_statuses(share):
    assets_dict = _assets_dict(share)
    statuses = []
    for shared_asset in share.shared_assets.all().order_by('asset_id'):
        asset_id = shared_asset.asset_id
        if asset_id in assets_dict:
            asset = assets_dict[asset_id]
            status = SharingStatus.create_valid_for_asset(share, shared_asset, asset)
        else:
            status = SharingStatus.create_asset_not_found(share, shared_asset)
        statuses.append(status)
    return statuses


def _assets_dict(share):
    asset_ids_qs = share.shared_assets.values('asset_id').query
    assets = Asset.unrestricted_objects.filter(id__in=asset_ids_qs)
    return dict([(asset.id, asset) for asset in assets])


def share_asset(sharer_user, asset, *args, **kwargs):
    return share_assets(sharer_user, [asset], *args, **kwargs)


# sentinel used to indicate the default expiry
# (can't use None because that means 'never').
# See http://effbot.org/zone/default-values.htm for an explanation of sentinels
# and their use with default arguments in Python.
default_expiry = object()


def _actualise_expiry(expiry):
    """
    If expiry is not an actual (i.e. concrete, non-sentinel) datetime then
    return the actual datetime that it symbolises.

    If it is already an actual datetime then just return it unmodified.

    Not idempotent because it may return times relative to the current time.
    """
    if expiry is default_expiry:
        expiry = datetime.datetime.now() + settings.SHARE_EXPIRY_PERIOD
    return expiry


def share_assets(sharer_user, assets, recipient, expiry=default_expiry,
                 domain=None, message='', request=None):
    """
    Share some assets.

    :param assets: a sequence containing the Assets to share.
    :param expiry: the date and time when the share should expire
    :type expiry: datetime.datetime or default_expiry
    """
    if not domain:
        domain = settings.DOMAIN
    expiry = _actualise_expiry(expiry)

    share = create_share_for_assets(assets, expiry, message)
    link = site_url(request) + share.get_absolute_url()

    send_sharing_email(sharer_user, assets, link, recipient, expiry,
                       domain, message=message)
    if request:
        messages.add_message(request, messages.SUCCESS, 'Success! Email sent to %s' % recipient)

    return share


def send_sharing_email(sharer_user, assets, link, recipient, expiry,
                       domain, message=''):
    sharer_user_profile = sharer_user.get_profile()
    from_address = sharer_user_profile.get_from_address(domain)
    send_mail('assetcloud/emails/shared_assets.html',
              from_address, [recipient],
              {'sharer': sharer_user_profile,
               'link': link,
               'assets': assets,
               'asset_count': len(assets),
               'expiry': expiry,
               'message': message})


def create_share_for_asset(asset, expiry=default_expiry):
    """
    Create an asset share. This is a low level method, it doesn't send email
    etc., if you want to do that then look at share_asset(), which indirectly
    calls this method.
    """
    return create_share_for_assets([asset], expiry)


def create_share_for_assets(assets, expiry=default_expiry, message=''):
    """
    Create an asset share. This is a low level method, it doesn't send email
    etc., if you want to do that then look at share_assets(), which calls this
    method.

    :param assets: a sequence containing the Assets to share.
    :param expiry: the date and time when the share should expire
    :type expiry: datetime.datetime or default_expiry
    """
    expiry = _actualise_expiry(expiry)
    share = Share(expiry=expiry, message=message,
                  key=UserProfile.random_shared_asset_key())
    share.save()
    for asset in assets:
        SharedAsset(share=share, asset=asset).save()
    return share
