from django.conf.urls import url
from warmama import views

urlpatterns = [
    url(r'^slogin$', views.ServerLogin.as_view(), name='slogin'),
    url(r'^slogout$', views.ServerLogout.as_view(), name='slogout'),
    url(r'^scc$', views.ServerClientConnect.as_view(), name='scc'),
    url(r'^scd$', views.ServerClientDisconnect.as_view(), name='scd'),
    url(r'^smr$', views.ServerMatchReport.as_view(), name='smr'),
    url(r'^shb$', views.ServerHeartbeat.as_view(), name='shb'),
    url(r'^smuuid$', views.ServerMatchUUID.as_view(), name='smuuid'),
    url(r'^clogin$', views.ClientLogin.as_view(), name='clogin'),
    url(r'^clogout$', views.ClientLogout.as_view(), name='clogout'),
    url(r'^ccc$', views.ClientConnect.as_view(), name='ccc'),
    url(r'^chb$', views.ClientHeartbeat.as_view(), name='chb'),
    url(r'^auth$', views.ClientAuthenticate.as_view(), name='auth'),
]
