from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    url(r'^$', 'griffin.views.resume.all',
        name='all_resumes'),
    url(r'^(?P<resume_id>\d+)$',
        'resume', name="resume"),
    url(r'^(?P<resume_id>\d+)/(?P<extension>[\w\d\_\-]+)/$',
        'griffin.views.resume.download',
        name='resume_download'),
)
