from views import ShoppingListViewSet
from rest_framework import routers
from django.conf.urls import include, url

router = routers.DefaultRouter()
router.register(r'shopping', ShoppingListViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]