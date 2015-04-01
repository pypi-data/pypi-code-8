from django.conf.urls import include, url

from wagtail.wagtailcore import hooks

from wagtailsettings import urls


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^settings/', include(urls)),
    ]
