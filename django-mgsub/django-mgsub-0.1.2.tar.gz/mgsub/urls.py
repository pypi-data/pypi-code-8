from django.conf.urls import url
from mgsub.views import SignupView, ThanksView

urlpatterns = [
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^thanks/$', ThanksView.as_view(), name='thanks'),
]
