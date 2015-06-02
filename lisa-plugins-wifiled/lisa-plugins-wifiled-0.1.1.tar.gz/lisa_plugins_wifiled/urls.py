from views import ConfigurationViewSet
from rest_framework import routers
from django.conf.urls import include, url

router = routers.DefaultRouter()
router.register(r'configuration', ConfigurationViewSet)

urlpatterns = [
    url(r'^/', include(router.urls, namespace='wifiled')),
]