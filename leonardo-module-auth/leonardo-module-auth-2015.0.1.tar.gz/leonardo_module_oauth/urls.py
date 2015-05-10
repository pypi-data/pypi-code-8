
from django.conf.urls import include, patterns

from leonardo.module.auth import views

from allauth.account.views import LoginView

views.LoginView = LoginView
#views.LoginView.template_name = 'leonardo/common/modal.html'

urlpatterns = patterns('',
                       (r'^accounts/', include('allauth.urls')),
                       )
