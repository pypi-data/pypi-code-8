
from django.conf.urls import include, patterns

urlpatterns = patterns(
    '',

    (r'^saml2/', include('djangosaml2.urls')),

)
