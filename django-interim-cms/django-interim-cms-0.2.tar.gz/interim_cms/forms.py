from django import forms


class ExampleForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
