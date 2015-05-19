from django.conf.urls import include, url
from django.contrib import admin

from commonwealth.apps.discussions.views import DiscussionListView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^summernote/', include('django_summernote.urls')),

    url(r'^$', DiscussionListView.as_view(), name='index'),

    url(r'^', include('commonwealth.apps.authentication.urls', namespace='authentication')),
    url(r'^discussions/', include('commonwealth.apps.discussions.urls', namespace='discussions'))
]
