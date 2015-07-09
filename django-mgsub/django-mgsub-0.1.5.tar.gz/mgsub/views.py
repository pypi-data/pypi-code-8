from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy

from mgsub.forms import SignupForm


class SignupView(FormView):
    template_name = 'mgsub/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('mgsub:thanks')


class ThanksView(TemplateView):
    template_name = 'mgsub/thanks.html'
