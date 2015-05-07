# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from assetcloud.models import Upload, Asset


def last_upload(user):
    qs = Upload.objects.filter(added_by=user).order_by('-added')
    if qs.exists():
        return qs[0]


def last_upload_assets(user):
    return filter_assets_by_last_upload(Asset.unrestricted_objects.all(), user)


def filter_assets_by_last_upload(qs, user):
    """
    Filter a QuerySet or SearchQuerySet of Assets to only include assets in
    user's last upload.
    """
    upload = last_upload(user)
    if upload:
        return qs.filter(upload=upload.id)
    else:
        return qs.none()


_UPLOAD_ID_KEY = __name__ + '.upload_id'


def current_upload(request):
    if _UPLOAD_ID_KEY in request.session:
        upload_id = request.session[_UPLOAD_ID_KEY]
        upload = Upload.objects.get(id=upload_id)
        return upload
    else:
        return None


def set_current_upload(request, upload):
    if not upload.id:
        raise ValueError('upload has no ID, is it saved?')
    request.session[_UPLOAD_ID_KEY] = upload.id


def start_new_upload(request):
    if _UPLOAD_ID_KEY in request.session:
        del request.session[_UPLOAD_ID_KEY]


def upload_asset(asset, upload=None, request=None, added_by=None):
    """
    Create an asset.

    If upload is specified or exists in the user's session then add the asset
    to an existing Upload batch, if not create a new one.
    """
    if request:
        added_by = request.user
        upload = current_upload(request)

    if upload is None:
        upload = Upload(added_by=added_by)
        upload.save()
        if request:
            set_current_upload(request, upload)

    asset.upload = upload
    asset.save()
