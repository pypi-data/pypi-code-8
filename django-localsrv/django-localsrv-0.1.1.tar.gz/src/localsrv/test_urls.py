from django.conf.urls import include, url
from django.contrib import admin
from . import urls

urlpatterns = [
    # Examples:
    # url(r'^$', 'localsrv.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^serve/', include(urls, namespace='serve')),
]
