from django.conf.urls import url, patterns
from bambu.xmlrpc import autodiscover

autodiscover()
urlpatterns = patterns('bambu.xmlrpc.views',
    url(r'^$', 'dispatch', name = 'xmlrpc_server')
)