# -*- coding: utf-8 -*-
# (c) 2011-2013 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from PIL import Image
from assetcloud import forms, sharing, app_settings
from assetcloud.asset_metadata_util import get_asset_metadata
from assetcloud.forms import parse_asset_ids, InvalidAssetIdsError
from assetcloud.models import Asset, AssetImageInfo, ProxyTag, DEFAULT_COLOURS, AssetDownloadLog
from assetcloud.nav import Navigation
from assetcloud.search import assets_from_results
from assetcloud.templatetags import resize
from assetcloud.upload_history import start_new_upload, upload_asset
from assetcloud.views.decorators import public
from collections import OrderedDict
from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Q
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson as json
from django.utils.html import escape
from django.views.generic import View
from django.views.static import serve
import StringIO
import assetcloud.download
import assetcloud_auth
import assetcloud_auth.forms
import copy
import decimal
import haystack.views
import logging
import mimetypes
import os
import tempfile
import time
import url_history.views
import zipfile

logger = logging.getLogger(__name__)


def get_asset_ids_from_request(request):
    if request.POST.get('asset_ids'):
        if ',' in request.POST['asset_ids']:
            return parse_asset_ids(request.POST['asset_ids'])
        else:
            return parse_asset_ids(','.join(request.POST.getlist('asset_ids')))
    return []


def add_template_message(request=None, level=messages.SUCCESS,
                         template=None,
                         context={}, safe=False, extra_tags=[]):
    if safe:
        extra_tags = extra_tags[:] + ["__safe"]
    messages.add_message(request, level,
                         render_to_string(template,
                                          RequestContext(request, context)),
                         extra_tags=extra_tags)


@assetcloud_auth.require_can_edit_assets
def asset_upload(request):
    start_new_upload(request)
    return render(request, 'assetcloud/pages/upload.html', {
            'section': 'upload',
            })


@assetcloud_auth.require_can_edit_assets
def asset_upload_action(request):
    """
    Upload an asset or assets to the site, either using AJAX, or by using
    a standard file form.
    """
    validation_error = None
    try:
        for file in request.FILES.getlist('file'):
            asset = Asset(file=file, account=request.account,
                          title=Asset.infer_title(file.name))
            upload_asset(asset, request=request)
            AssetImageInfo.create_for_asset(asset)
    except ValidationError, e:
        validation_error = e

    # This handles returning the correct response to plupload AJAX uploads.
    # See:
    # http://feeding.cloud.geek.nz/2011/04/using-plupload-inside-django.html
    if request.is_ajax():
        if validation_error:
            e = '"error": {"code": 1, "message": "%s"},' % ', '.join(validation_error.messages)
        else:
            e = '"result" : null,'
        response = HttpResponse('{"jsonrpc" : "2.0", ' +
                                e +
                                ' "id" : "id"}',
                                mimetype='text/plain; charset=UTF-8')
        response['Expires'] = 'Mon, 1 Jan 2000 01:00:00 GMT'
        response['Cache-Control'] = ('no-store, no-cache, must-revalidate,'
                                     ' post-check=0, pre-check=0')
        response['Pragma'] = 'no-cache'
        return response
    else:
        if validation_error:
            raise validation_error

    return redirect('asset-upload')


def cancel_upload_action(request):
    add_template_message(
        request=request, level=messages.WARNING,
        template='assetcloud/messages/upload_cancelled.html',
        safe=True)
    return asset_upload_action(request)


def asset_download_action(request, id):
    """
    Check permissions and then download an asset,
    including setting the correct Content-Disposition headers etc...
    """
    asset = get_asset_or_404(id, request.user)
    return _asset_download_nopermchecks(request, asset)


def _asset_download_nopermchecks(request, asset):
    """
    Download an asset without any permission checks,
    including setting the correct Content-Disposition headers etc...
    """
    # We should really be serving files via s3 or via a stream
    temp_file = asset.save_to_temporary_file()
    filename = os.path.basename(temp_file.name)
    dirname = os.path.dirname(temp_file.name)
    response = serve(request, filename, dirname)
    assetcloud.download.set_download_headers_for_asset(response, asset)
    AssetDownloadLog.log_download(asset=asset, user=request.user)
    return response


def asset_resize_download_action(request, id, width=580, height=None):
    asset = get_asset_or_404(id, request.user)
    image = Image.open(asset.file)

    width = decimal.Decimal(width)

    # If height is None, preserve aspect ratio
    if height is None:
        iwidth, iheight = image.size
        height = decimal.Decimal(iheight) / decimal.Decimal(iwidth) * width
    else:
        height = decimal.Decimal(height)

    (mimetype, encoding) = mimetypes.guess_type(asset.filename)
    # This can happen if guess_type can't guess a mime type for the filename.
    # There used to be some related intermittent test failures, but they
    # should be fixed now. I've left this check in so that if this method
    # does come across a problematic (no mimetype) filename then the error
    # message will include the filename, instead of just crashing when rindex
    # is called on None.
    if mimetype is None:
        raise Exception('guess_type returned None mimetype for filename %s' % asset.filename)
    format = mimetype[mimetype.rindex('/') + 1:]

    output = StringIO.StringIO()

    image.resize((width.quantize(1), height.quantize(1))).save(output, format, quality=90)
    contents = output.getvalue()
    output.close()

    response = HttpResponse(contents)
    assetcloud.download.set_download_headers_for_asset(response, asset)
    AssetDownloadLog.log_download(asset=asset, user=request.user)
    return response


def tag_autocomplete_action(request):
    """
    Tag autocompletion.

    See:
      http://jqueryui.com/demos/autocomplete/#remote

    Be aware that the *JQuery UI* autocompletion is _not_ the same as
    the *JQuery* autocompletion given here:
      http://docs.jquery.com/Plugins/Autocomplete/autocomplete
    """
    query = request.GET['term']
    logger.debug('tag_autocomplete_action: %s', query)
    try:
        limit = int(request.GET['limit'])
    except (ValueError, KeyError):
        limit = 10

    tags = request.user.get_profile().filter_tags_for_restrictions(
        request.account.tags_by_popularity(query, limit))

    return HttpResponse(json.dumps(tags),
                        mimetype='application/json; charset=UTF-8')


def get_asset_or_error(id, user):
    try:
        return Asset.objects(user).get(id=id)
    except Asset.DoesNotExist:
        try:
            if Asset.unrestricted_objects.get(id=id):
                raise PermissionDenied()
        except Asset.DoesNotExist:
            raise http.Http404


def get_assets_or_error(asset_ids, user):
    return [get_asset_or_error(asset_id, user)
            for asset_id in asset_ids]


def get_asset_or_404(id, user):
    try:
        asset = Asset.objects(user).get(id=id)
    except Asset.DoesNotExist:
        raise http.Http404
    return asset


def get_asset_or_403(id, user):
    try:
        asset = Asset.objects(user).get(id=id)
    except Asset.DoesNotExist:
        raise PermissionDenied()
    return asset


def asset(request, section, id, form=None):
    """
    The 'asset detail' page for an asset.
    """
    asset = get_asset_or_error(id, request.user)

    if form is None:
        form = forms.AssetForm(instance=asset)

    sizes = []
    if asset.image_info:
        large_size = 1024
        if asset.image_info.width < 1024 or asset.image_info.height < 768:
            large_size = 768

        sizes = [(resize.get_resize_bounds_within(asset, w), name)
                 for w, name in
                 [(large_size, 'Large'),
                  (600, 'Medium'),
                  (240, 'Small')]
                 if w <= max(asset.image_info.width, asset.image_info.height)]

    asset_metadata = get_asset_metadata(asset)
    data = {'asset': asset,
            'asset_metadata': asset_metadata,
            'sizes': [(size[0], size[1], name) for size, name in sizes],
            'form': form,
            'asset_in_folder': request.user.get_profile().folder.contains(asset),
            'section': section,
            'nav': Navigation(request),
            }
    return render(request, 'assetcloud/pages/asset.html', data)


@assetcloud_auth.require_can_edit_assets
def asset_update_action(request, section, id):
    asset_instance = get_asset_or_error(id, request.user)

    form = forms.AssetForm(request.POST, request.FILES, instance=asset_instance)

    if form.is_valid():
        form.save()
        return redirect('asset', id=id)
    else:
        return asset(request, section, id, form)


@assetcloud_auth.require_can_edit_assets
def asset_delete_action(request, id):
    asset_instance = get_asset_or_error(id, request.user)

    asset_instance.delete()

    return redirect('asset-list')


@assetcloud_auth.require_account_admin
def account_users(request, section, form=None):
    """
    The 'users' page on a account's AssetCloud.
    """
    if not request.user.get_profile().is_admin:
        return HttpResponseForbidden()

    if form is None:
        form = assetcloud_auth.forms.CreateUserForm()

    data = {'section': section,
            'subsection': 'users'}

    # We need to use Q objects to be able to write this query
    this_account = Q(userprofile__account=request.account)
    is_active = Q(is_active=True)
    is_pending = ~Q(userprofile__activation_key='')

    users = User.objects.filter(this_account, is_active | is_pending)
    users = users.order_by('-userprofile__is_admin', 'email')

    data.update({'users': users,
                 'form': form})

    return render(request, 'assetcloud/pages/account/users.html', data)


@public
def share(request, share_id=None, key=None):
    status = sharing.check_share_status(share_id, key)
    if status.valid:
        asset_statuses = sharing.all_asset_statuses(status.share)
        return render(request, 'assetcloud/pages/logged_out/shared_assets.html', {
            'asset_statuses': asset_statuses,
            'share': status.share,
        })
    elif status.status == sharing.SharingStatus.STATUS_EXPIRED:
        return render(request, 'assetcloud/pages/logged_out/shared_asset_expired.html', {
            'share': status.share,
        })
    else:
        raise PermissionDenied


@public
def shared_asset_download_action(request, share_id, key, asset_id):
    status = sharing.check_asset_share_status(share_id, key, asset_id)
    if status.valid:
        return _asset_download_nopermchecks(request, status.asset)
    else:
        raise PermissionDenied


def _make_default_colours_available_to_template(data):
    for (field_name, colour) in DEFAULT_COLOURS.iteritems():
        data['default_' + field_name] = colour


def _add_account_saved_message(request, account_copy):
    if account_copy.subdomain:
        message = 'Your changes to <a href="{protocol}://{subdomain}.{domain_suffix}">{subdomain}.{domain_suffix}</a> have been saved'.format(
            protocol=escape(settings.PROTOCOL),
            subdomain=escape(account_copy.subdomain),
            domain_suffix=escape(settings.DOMAIN_SUFFIX))
    else:
        message = 'Your changes have been saved'

    messages.add_message(request, messages.SUCCESS, message, extra_tags='__safe')


@assetcloud_auth.require_account_admin
def customise_account(request, section):
    """
    The 'customise' page on an account's AssetCloud.
    """

    # Don't use the same object for the user profile and the form, because then
    # nav.html ends up using the object updated by the form even if the form
    # validation fails.
    account_copy = copy.copy(request.user.get_profile().account)
    form = assetcloud.forms.CustomiseForm(request.POST or None, request.FILES or None,
        instance=account_copy)
    if form.is_valid():
        form.save()
        _add_account_saved_message(request, account_copy)
        return redirect('customise-account')
    else:
        data = {'section': section,
                'subsection': 'customise',
                'form': form,
                'max_logo_image_size': settings.MAX_LOGO_IMAGE_SIZE,
                'domain_suffix': settings.DOMAIN_SUFFIX}
        _make_default_colours_available_to_template(data)

        return render(request, 'assetcloud/pages/account/customise.html', data)


def render_tag_action(request):
    tag_name = request.GET.get('tag_name')
    force_user_tag = request.GET.get('force_user_tag')
    try:
        tag = ProxyTag.objects.get(name=tag_name)
    except ProxyTag.DoesNotExist:
        tag = {'name': tag_name,
               'is_user_tag': force_user_tag == '1'}
    return render(request, 'assetcloud/snippets/tag.html', {
            'tag': tag,
            'force_user_tag': force_user_tag == '1'
    })


def messages_action(request):
    return render(request, 'assetcloud/snippets/messages.html')


def tag_list(request):
    tags = request.user.get_profile().filter_tags_for_restrictions(
        request.account.tag_counts())

    return HttpResponse(json.dumps(sorted(tags)),
        mimetype='application/json; charset=UTF-8')


class BulkAction(View):
    """ Superclass for actions on multiple assets.

    It is quite easy to extend most bulk behaviour to individual assets though in certain cases (e.g. download as zip) it doesn't make much sense.

    The workflow for a bulk action is:
       initialise()
       check_arguments()
       process_ids()
       process_assets()
       finalise()
       return

    Initialise gives subclasses the opportunity to set up preconditions
    Check arguments allows subclasses to verify the arguments given to the view
    Process ids by default just transforms ids into the corresponding assets
    Process assets is not called explicitly but is called by process ids under default behaviour. It in turn calls process_asset
    Finalise gives subclasses an opportunity to do things just before the view returns

    To break out of processing early just raise PermissionDenied. If process_ids returns anything other than None that will be returned (after finalise). Otherwise, 200 will be returned after finalise()"""

    def post(self, request, *args, **kwargs):
        """
        Create and return a post response, and log the time it took to do so.
        """
        # The ONLY code in this method should be the timing and logging code
        # and a call to _post(). Everything to do with actually processing
        # the request and creating the response should be in _post().
        start_time = time.time()
        response = self._post(request, *args, **kwargs)
        end_time = time.time()
        logger.debug('%s took %0.3f seconds' % (self.__class__.__name__, end_time - start_time))
        return response

    def _post(self, request, *args, **kwargs):
        self.request = request
        try:
            self.initialise()
            self.check_arguments(*args, **kwargs)
            try:
                asset_ids = get_asset_ids_from_request(self.request)
                if asset_ids:
                    result = self.process_ids(asset_ids)
                    self.finalise()
                    if result:
                        return result
                    return HttpResponse(status=200)
            except InvalidAssetIdsError:
                pass
        except PermissionDenied:
            pass
        return HttpResponse(status=403)

    def initialise(self):
        pass

    def check_arguments(self, *args, **kwargs):
        pass

    def process_ids(self, ids):
        self.assets = Asset.objects(self.request.user).filter(pk__in=ids)
        return self.process_assets(self.assets)

    def process_assets(self, assets):
        for asset in assets:
            self.process_asset(asset)

    def finalise(self):
        pass


class FolderAction(BulkAction):
    action_text = None

    def initialise(self):
        self.processed_assets = 0

    def check_arguments(self, folder_id=None):
        folder = self.request.user.get_profile().folder
        if folder.pk == int(folder_id):
            self.folder = folder
        else:
            raise PermissionDenied()

    def finalise(self):
        if self.message_template:
            add_template_message(
                request=self.request, level=messages.SUCCESS,
                template='assetcloud/messages/' + self.message_template,
                context={
                    'num_assets': len(self.assets),
                    'folder': self.folder
                    },
                safe=True)


class AddToFolderAction(FolderAction):
    message_template = "added_to_folder.html"

    def process_asset(self, asset):
        if not self.folder.contains(asset):
            self.folder.assets.add(asset)


class RemoveFromFolderAction(FolderAction):
    message_template = "removed_from_folder.html"

    def process_asset(self, asset):
        if self.folder.contains(asset):
            self.folder.assets.remove(asset)


class PrepareZipAction(BulkAction):
    def process_assets(self, assets):
        _prepare_zip(self.request, assets)


def _prepare_zip(request, assets):
    """
    Create a zip with selected assets and store in session
    """
    temp = tempfile.NamedTemporaryFile(delete=False)
    with zipfile.ZipFile(temp.name, 'w') as zf:
        download_logs = []
        for asset in assets:
            download_logs.append(AssetDownloadLog.log_download(user=request.user, asset=asset, save=False))
            zf.writestr(asset.filename, asset.file.read())
        request.session['zip_file'] = temp.name
        AssetDownloadLog.objects.bulk_create(download_logs)


def download_zip_action(request):
    # Download the zip from the session
    if request.session.get('zip_file'):
        return assetcloud.download.DeleteAfterwardsFileResponse(
            path=request.session['zip_file'],
            filename="assets.zip")
    return HttpResponse(status=403)


class TagsAction(BulkAction):
    def check_arguments(self):
        form = forms.TagSetForm(self.request.POST)
        if form.is_valid():
            self.tags = form.cleaned_data['tags']
        else:
            return HttpResponse(status=400)

    def get_response(self, tag_names):
        response_html = [render_to_string(
                'assetcloud/snippets/tag.html',
                RequestContext(
                    self.request,
                    {'tag': ProxyTag.objects.get(name=t)}))
                         for t in tag_names]
        return HttpResponse(json.dumps(response_html),
                            mimetype='application/json; charset=UTF-8')


class CommonTagsAction(TagsAction):
    def initialise(self):
        super(CommonTagsAction, self).initialise()
        self.asset_tag_names = []

    def check_arguments(self):
        # Explicitly ignore super to avoid form check
        pass

    def process_assets(self, assets):
        super(TagsAction, self).process_assets(assets)
        if not self.asset_tag_names:
            self.asset_tag_names.append(set())
        tags = reduce(lambda x, y: x & y, self.asset_tag_names)
        return self.get_response(tags)

    def process_asset(self, asset):
        self.asset_tag_names.append(set(t.name for t in asset.tags.all()))


def _all_asset_tag_names(assets):
    """
    Returns the names of the tags that are associated with ALL the passed
    assets, i.e. if a tag is only associated with some of the assets don't
    include its name.
    """
    if not assets:
        return set()

    result = {tag.name for tag in assets[0].tags.all()}
    for asset in assets[1:]:
        result &= {tag.name for tag in asset.tags.all()}

    return result


class UpdateTagsAction(TagsAction):
    def process_assets(self, ids):
        # Record the existing tags (union if there are multiple assets)
        existing = _all_asset_tag_names(self.assets)

        super(TagsAction, self).process_assets(ids)

        # Return the tag diff
        new = _all_asset_tag_names(self.assets)
        response_tag_names = list(self.get_tag_name_difference(set(existing), set(new)))

        return self.get_response(response_tag_names)


class AddTagsAction(UpdateTagsAction):
    def process_asset(self, asset):
        asset.tags.add(*self.tags)

    def get_tag_name_difference(self, existing, new):
        return new - existing


class DeleteTagsAction(UpdateTagsAction):
    def process_asset(self, asset):
        asset.tags.remove(*self.tags)

    def get_tag_name_difference(self, existing, new):
        return existing - new


class DeleteAssetsAction(BulkAction):
    def process_asset(self, asset):
        asset.delete()

    def finalise(self):
        add_template_message(
            request=self.request, level=messages.SUCCESS,
            template='assetcloud/messages/assets_deleted.html',
            context={
                'num_assets': len(self.assets)
            },
            safe=True
        )


class SearchView(haystack.views.SearchView, View):
    template = 'assetcloud/pages/search.html'
    section = None

    def __init__(self):
        super(SearchView, self).__init__(
            form_class=forms.SearchForm,
            results_per_page=settings.ASSETS_PER_PAGE)

    def get(self, request, section=None):
        if section:
            self.section = section
        response = super(SearchView, self).__call__(request)
        nav = Navigation(request)
        nav.current_page_is_asset_list()
        return response

    def build_form(self):
        form_kwargs = {'user': self.request.user}

        # If haystack.views.SearchView is called with no parameters then it
        # passes data=None to the form, which causes form.is_bound to be False,
        # which causes form.is_valid() to be False, which causes no search
        # results to be shown. We want to show *all* the assets when we are
        # called with no parameters, so we tell assetcloud.forms.SearchForm
        # to use data={} instead of data=None in this case.
        if not len(self.request.GET):
            form_kwargs['data_override'] = {}

        return super(SearchView, self).build_form(form_kwargs)

    def get_results(self):
        if self.form.is_valid():
            return super(SearchView, self).get_results()
        else:
            return []

    def extra_context(self):
        result = {}
        result.update(super(SearchView, self).extra_context())
        if self.section:
            result['section'] = self.section
        return result


def home(request):

    max_asset_count = app_settings.HOMEPAGE_TAG_MAX_ASSET_COUNT

    recently_added = Asset.objects(request.user).order_by('-added')[:max_asset_count]

    all_results = OrderedDict()

    account = request.user.get_profile().account

    for tag in account.homepage_tags.order_by('name'):
        results = Asset.objects(request.user).order_by('-added').filter(tags=tag)[:max_asset_count]
        all_results['%s' % tag] = results

    all_results['Recently added'] = recently_added

    response = render(request, 'assetcloud/pages/home.html', {
        'all_results': all_results,
        'section': 'home',
    })
    Navigation(request).current_page_is_asset_list()
    return response


def share_asset(request, id):
    asset = get_asset_or_error(id, request.user)
    form = forms.ShareAssetsForm(initial={'asset_ids': id})
    return _render_share_asset(request, form, 1, asset)


def share_assets(request):
    asset_ids_str = request.GET['asset_ids']
    asset_ids_list = parse_asset_ids(asset_ids_str)
    form = forms.ShareAssetsForm(initial={'asset_ids': asset_ids_str})
    return _render_share_asset(request, form, len(asset_ids_list))


def share_assets_action(request):
    form = forms.ShareAssetsForm(request.POST)

    if form.is_valid():
        asset_ids = form.cleaned_data['asset_ids']
        assets = get_assets_or_error(asset_ids, request.user)
        recipient = form.cleaned_data['recipient']
        message = form.cleaned_data['message']
        sharing.share_assets(request.user, request=request, assets=assets,
                             recipient=recipient, message=message)
        return http.HttpResponse('OK')
    else:
        asset_ids_bound_field = form['asset_ids']
        asset_ids = asset_ids_bound_field.field.to_python(asset_ids_bound_field.value())
        num_assets = len(asset_ids)
        if num_assets == 1:
            asset = get_asset_or_error(asset_ids[0], request.user)
        else:
            asset = None
        return _render_share_asset(request, form, num_assets, asset)


def _render_share_asset(request, form, num_assets, asset=None):
    """
    asset: optional asset - if passed then its title will be shown in the heading on the page
    """
    return render(request, 'assetcloud/forms/share_assets_form.html', {
        'num_assets': num_assets,
        'asset': asset,
        'form': form,
        })


class FolderView(SearchView):
    template = 'assetcloud/pages/folder.html'
    section = 'folder'

    def get_results(self):
        results = super(FolderView, self).get_results()
        return results.filter(folders=self.request.user.get_profile().folder.pk)


class PrepareFolderZipView(FolderView):
    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def create_response(self):
        assets = assets_from_results(self.results)
        _prepare_zip(self.request, assets)
        return HttpResponse(status=200)


def server_error(request, *args, **kwargs):
    return url_history.views.server_error(
        request, data={
            'PROJECT_NAME': settings.PROJECT_NAME,
            'SUPPORT_EMAIL_ADDRESS': settings.SUPPORT_EMAIL_ADDRESS,
        },
        *args, **kwargs)


search = SearchView.as_view()
asset_list = search
favourites = FolderView.as_view()


add_to_folder_action = AddToFolderAction.as_view()
remove_from_folder_action = RemoveFromFolderAction.as_view()

prepare_zip_action = PrepareZipAction.as_view()
prepare_folder_zip_action = PrepareFolderZipView.as_view()
asset_add_tags_action = assetcloud_auth.require_can_edit_assets(
    AddTagsAction.as_view())
asset_delete_tags_action = assetcloud_auth.require_can_edit_assets(
    DeleteTagsAction.as_view())
delete_assets_action = assetcloud_auth.require_can_edit_assets(
    DeleteAssetsAction.as_view())
common_tags_action = CommonTagsAction.as_view()
