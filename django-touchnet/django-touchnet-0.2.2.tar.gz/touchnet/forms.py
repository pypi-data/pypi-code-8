from django import forms
from django.conf import settings

from .models import PostbackLog
from .utils import make_external_transaction_id, make_validation_key

class PostbackForm(forms.Form):
    EXT_TRANS_ID = forms.CharField()
    UPAY_SITE_ID = forms.CharField()

    pmt_status = forms.ChoiceField(choices=PostbackLog.PAYMENT_STATUS_CHOICES)

    posting_key = forms.CharField()
    pmt_amt = forms.DecimalField(max_digits=19, decimal_places=2, required=False)

    def clean_UPAY_SITE_ID(self):
        site_id = self.cleaned_data['UPAY_SITE_ID']
        if site_id != settings.TOUCHNET['site_id']:
            raise forms.ValidationError('Incorrect Site Id', code='invalid')
        return site_id

    def clean_posting_key(self):
        posting_key = self.cleaned_data['posting_key']
        if posting_key != settings.TOUCHNET['posting_key']:
            raise forms.ValidationError('Incorrect Posting Key', code='invalid')
        return posting_key

class RedirectForm(forms.Form):
    EXT_TRANS_ID = forms.CharField(widget=forms.HiddenInput)
    UPAY_SITE_ID = forms.CharField(initial=settings.TOUCHNET['site_id'], widget=forms.HiddenInput)
    AMT = forms.DecimalField(max_digits=19, decimal_places=2, widget=forms.HiddenInput)
    VALIDATION_KEY = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, transaction_id, amount,
            fid=settings.TOUCHNET['accounting']['fid'],
            fau=settings.TOUCHNET['accounting']['fau'],
            *args, **kwargs):
        initial = kwargs.get('initial', {})
        external_transaction_id = make_external_transaction_id(transaction_id, fid, fau)
        initial['EXT_TRANS_ID'] = external_transaction_id
        initial['AMT'] = amount
        initial['VALIDATION_KEY'] = make_validation_key(external_transaction_id, amount)
        kwargs['initial'] = initial
        super(RedirectForm, self).__init__(*args, **kwargs)
