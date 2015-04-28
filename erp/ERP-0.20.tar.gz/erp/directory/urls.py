__author__ = 'cltanuki'
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from . import api


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'persons', api.PersonsViewSet)
router.register(r'persons/(?P<person_pk>.+)/phones', api.PhonesViewSet)
router.register(r'persons/(?P<person_pk>.+)/emails', api.EMailsViewSet)
router.register(r'persons/(?P<person_pk>.+)/positions', api.PositionsViewSet)

#router.r

urlpatterns = router.urls