from jobvite import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^positions/$', views.positions,
        name='jobvite-positions'),
    url(r'^positions/(?P<job_id>[\w]+)/$', views.positions,
        name='jobvite-positions-by-id'),
    url(r'^categories/$', views.categories,
        name='jobvite-categories'),
    url(r'^categories/(?P<category_id>[\w-]+)/$',
        views.categories,
        name='jobvite-categories-by-id'),
)
