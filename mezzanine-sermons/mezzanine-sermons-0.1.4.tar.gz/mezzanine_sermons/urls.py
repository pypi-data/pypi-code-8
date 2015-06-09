from django.conf.urls import patterns, include, url

from mezzanine_sermons import views

#####################################
#       Urls for church app         #
#####################################

urlpatterns = patterns('',
                       url(r'^$', views.sermons, name="home"),
                       url(r'^series//?(?P<series_id>\d+)?/?$', views.single_sermon_series, name='series'),
                       url(r'^allseries', views.sermon_series_list, name='serieslist'),
                       )
