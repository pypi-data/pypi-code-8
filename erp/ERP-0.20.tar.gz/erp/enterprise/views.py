import json
import logging
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import View, FormView, TemplateView, DetailView
from django.http import HttpResponseBadRequest
from django.conf import settings
from . import models, forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login
from erp.extras.views import AjaxFormMixin
from django.core.urlresolvers import reverse
from erp.enterprise.models import CorpUser


class Index(TemplateView):

    template_name = 'enterprise/index.html'


class Login(FormView):

    template_name = settings.LOGIN_TEMPLATE
    form_class = forms.SignInForm


class AjaxLogin(AjaxFormMixin):

    form_class = forms.SignInForm

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponse('OK')


class Register(AjaxFormMixin):

    template_name = 'registration/register.html'
    form = forms.UserCreationForm

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('dir-add'))


class StructureMain(TemplateView):

    template_name = 'enterprise/structure.html'


class Profile(DetailView):

    template_name = 'enterprise/corpuser_detail.html'
    model = CorpUser

    # def get(self, request, *args, **kwargs):
    #     user = kwargs['username']
    #     return render(request, self.template_name, {'object': user})


class PasswordChange(AjaxFormMixin):

    form_class = PasswordChangeForm

    def get_form(self, form_class):
        return form_class(user=self.request.user, **self.get_form_kwargs())