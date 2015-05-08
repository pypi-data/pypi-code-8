# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.conf.urls import patterns, url

urlpatterns = patterns('assetcloud.views',

    # Top level pages
    url(r'^$', 'home', name='home'),
    url(r'^upload$', 'asset_upload', name='asset-upload'),
    url(r'^search/', 'search', {'section': 'asset-list'}, name='search'),
    url(r'^assets$', 'asset_list', {'section': 'asset-list'},
        name='asset-list'),
    url(r'^account-users$', 'account_users', {'section': 'admin'},
        name='account-users'),
    url(r'^customise-account$', 'customise_account', {'section': 'admin'},
        name='customise-account'),

    # Other pages
    url(r'^asset/(?P<id>\d+)$', 'asset', {'section': 'asset-list'},
        name='asset'),

    # AJAX forms (these URLs return HTML that is loaded into a div)
    url(r'^asset/share/(?P<id>\d+)$', 'share_asset', name='share_asset'),
    url(r'^assets/share', 'share_assets', name='share_assets'),

    # Actions
    url(r'^actions/upload$', 'asset_upload_action',
        name='asset-upload-action'),
    url(r'^actions/upload/cancel$', 'cancel_upload_action',
        name='cancel_upload_action'),
    url(r'^actions/asset/update/(?P<id>\d+)$', 'asset_update_action',
        {'section': 'asset-list'},
        name='asset-update-action'),
    url(r'^actions/asset/delete/(?P<id>\d+)$', 'asset_delete_action',
        name='asset-delete-action'),
    url(r'^assets/download/(?P<id>\d+)$', 'asset_download_action',
        name='asset-download-action'),
    url(r'^assets/resize/(?P<id>\d+)/$',
        'asset_resize_download_action',
        name='asset-resize-base-download-action'),
    url(r'^assets/resize/(?P<id>\d+)/(?P<width>\d+)/$',
        'asset_resize_download_action',
        name='asset-resize-download-width-action'),
    url(r'^assets/resize/(?P<id>\d+)/(?P<width>\d+)/(?P<height>\d+)/$',
        'asset_resize_download_action',
        name='asset-resize-download-action'),
    url(r'^assets/tag/add/$', 'asset_add_tags_action',
        name='asset_add_tags_action'),
    url(r'^assets/tag/delete/$', 'asset_delete_tags_action',
        name='asset_delete_tags_action'),
    url(r'^assets/delete/$', 'delete_assets_action',
        name='delete_assets_action'),
    url(r'^actions/assets/share/$', 'share_assets_action',
        name='share_assets_action'),

    url(r'^tag/common$', 'common_tags_action', name='common_tags_action'),
    url(r'^tag/autocomplete$', 'tag_autocomplete_action',
        name='tag_autocomplete_action'),
    url(r'^tag/render/$', 'render_tag_action', name='render_tag_action'),
    url(r'^tags$', 'tag_list', name='tag-list'),
    url(r'^messages$', 'messages_action',
        name='messages-action'),

    url(r'^folders/add/(?P<folder_id>\d+)/$', 'add_to_folder_action',
        name='add_to_folder_action'),
    url(r'^folders/remove/(?P<folder_id>\d+)/$', 'remove_from_folder_action',
        name='remove_from_folder_action'),

    url(r'^folders/favourites$', 'favourites',
        name='favourites'),

    url(r'^download/zip/prepare$', 'prepare_zip_action', name='prepare_zip_action'),
    url(r'^download/zip/$', 'download_zip_action', name='download_zip_action'),

    url(r'^folders/favourites/download/zip/prepare$', 'prepare_folder_zip_action',
        name='prepare_folder_zip_action'),
    url(r'^download/zip/$', 'download_zip_action',
        name='download_folder_zip_action'),
)

urlpatterns += patterns('assetcloud.api',
    url(r'^api/asset/(?P<id>\d+)/title$', 'asset_title_action',
        name='asset-title-action')
)
