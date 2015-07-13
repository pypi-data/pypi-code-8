from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, resolve

from djangocms_contact.forms import ContactForm


def contact(request):
    """
    Shows a contact page with a form or redirects to success page if the form
    has been sent.
    """

    # Required for apphooks because Django does not allow an other way of doing
    # this. See <http://docs.django-cms.org/en/3.1.2/how_to/apphooks.html>.
    current_app = resolve(request.path_info).namespace

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('djangocms_contact:success',
                                                current_app=current_app))
    else:
        form = ContactForm()

    context = RequestContext(request, {'contact_form': form},
                             current_app=current_app)
    return render_to_response('djangocms_contact/contact.html',
                              context_instance=context)
