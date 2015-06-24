from django.conf.urls import url, patterns, include
from bangoo.media import views

urlpatterns = patterns('',
    url(r'^admin/', include('bangoo.admin.urls', namespace='admin')),
    url('images/$', views.images_home, name='images-list'),
)

