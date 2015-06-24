from django.conf.urls import patterns, url
from bangoo.navigation.menu import views

urlpatterns = patterns('',
    url(r'^$', views.menu, name='admin-menu'),
    url(r'reorder/$', views.ReorderMenuView.as_view(), name='admin-reorder-menu'),
    url(r'(?P<menu_id>\d+)/rename/$', views.RenameMenuView.as_view(), name='admin-rename-menu')
)
