#coding=utf-8

from django.conf.urls import patterns,  url

urlpatterns = patterns('base.views',
    # url(r'^myview/$', 'myview', name=u'我的视图'),
)

# 引用相同app下的不同views模块
# 
# urlpatterns += patterns('some_views.views',
#    url(r'^other_view/$', 'other_view', name=u'另一个视图'),
# )