# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.conf import settings as conf
from django.contrib.auth.decorators import login_required
from rgallery.views import (Photos,
                            PhotosFolder,
                            PhotoDelete,
                            PhotoAdd,
                            PhotosTag,
                            PhotoAddTag,
                            PhotoGetVideo,
                            PhotoChangeStatus,
                            PhotoDownload,
                            PhotoMkThumb,
                            PhotoMediaSync)


########## PRIVACY SETTINGS
def private(myview):
    if conf.RGALLERY_PRIVATE:
        return login_required(myview)
    return myview
########## PRIVACY SETTINGS


########## URL SETTINGS
urlpatterns = patterns(
    '',

    url(r'^$',
        private(Photos.as_view()),
        name='index'),

    url(r'^page/(?P<page>\d+)/$',
        private(Photos.as_view()),
        name='page'),

    url(r'^photo/del/$',
        private(PhotoDelete.as_view()),
        name='photo_del'),

    url(r'^photo/add/$',
        private(PhotoAdd.as_view()),
        name='photo_add'),

    url(r'^photo/changestatus/$',
        private(PhotoChangeStatus.as_view()),
        name='photo_change_status'),

    url(r'^photo/download/$',
        private(PhotoDownload.as_view()),
        name='photo_download'),

    url(r'^photos/tag/(?P<slug>[-\w]+)/$',
        private(PhotosTag.as_view()),
        name='photos_tag'),

    url(r'^photos/tag/(?P<slug>[-\w]+)/(?P<page>\d+)/$',
        private(PhotosTag.as_view()),
        name='photos_tag_page'),

    url(r'^photo/add/tag/$',
        private(PhotoAddTag.as_view()),
        name='photo_add_tag'),

    url(r'^photo/get_video/$',
        private(PhotoGetVideo.as_view()),
        name='photo_get_video'),

    url(r'^(?P<folder>[-_A-Za-z0-9]+)/$',
        private(PhotosFolder.as_view()),
        name='folder'),

    url(r'^gallery/photos/mkthumb/$',
        private(PhotoMkThumb.as_view()),
        name='photo_mkthumb'),
    url(r'^gallery/photos/mediasync/$',
        private(PhotoMediaSync.as_view()),
        name='photo_mediasync'),
)
########## URL SETTINGS
