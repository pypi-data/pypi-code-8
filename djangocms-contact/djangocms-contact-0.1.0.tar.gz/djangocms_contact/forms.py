from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from djangocms_contact.models import ContactMessage


class ContactForm(ModelForm):
    """
    A contact form based on ContactMessage model for allow the user to send a
    message.
    """

    name = forms.CharField(min_length=2, error_messages={
        'required': _('You must enter your name.'),
        'min_length': _('The name must be at least %(limit_value)s characters.')
    })
    email = forms.EmailField(error_messages={
        'required': _('You must enter your email.'),
        'invalid': _('The email is not valid.')
    })
    message = forms.CharField(min_length=5, widget=forms.Textarea, error_messages={
        'required': _('You must enter a message.'),
        'min_length': _('The message must be at least %(limit_value)s characters.')
    })

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
