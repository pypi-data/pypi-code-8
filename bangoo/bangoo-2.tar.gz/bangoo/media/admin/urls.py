from bangoo.media import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^images/$', views.images_home, name='media-images-home'),
    url(r'^images/upload/$', views.upload_image, name='media-image-upload'),
    url(r'^redactor/images/list/$', views.list_images, name='media-redactor-list-images'),
    url(r'^redactor/images/upload/$', views.upload_images, name='media-redactor-upload-images'),
)