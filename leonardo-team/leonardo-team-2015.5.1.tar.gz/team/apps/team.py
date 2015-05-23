from django.conf.urls import *

urlpatterns = patterns('team.views',
                       (r'^$', 'person_list', {}, 'project_team_list'),
                       (r'^(?P<person_nick_name>\w+)/$',
                        'person_detail', {}, 'project_team_detail'),
                       )
