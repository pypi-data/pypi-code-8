# coding: utf8
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from bangoo.content.models import Content


class EditContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['authors', 'allow_comments', 'template_name', 'registration_required', 'is_page']
    
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)

        self.base_fields['authors'].help_text = ''
        self.base_fields['authors'].widget.attrs['style'] = 'width: 100%'

        super(EditContentForm, self).__init__(*args, **kwargs)

        self.languages = []
        for lang_code, lang in settings.LANGUAGES:
            required = True if lang_code == settings.LANGUAGE_CODE.split('-')[-1] else False
            self.fields['title_%s' % lang_code] = forms.CharField(max_length=200, label='Title (%s)' % lang,
                                                                  required=required)
            self.fields['text_%s' % lang_code] = forms.CharField(required=required, label='Content (%s)' % lang,
                                                                 widget=forms.Textarea)
            if self.instance.pk:
                try:
                    trans = self.instance.translations.get(language_code=lang_code)
                    self.fields['title_%s' % lang_code].initial = trans.title
                    self.fields['text_%s' % lang_code].initial = trans.text
                except (Content.DoesNotExist, KeyError):
                    pass

            self.languages.append({
                'fields': {
                    'title': self['title_{0}'.format(lang_code)],
                    'text': self['text_{0}'.format(lang_code)]},
                'heading': _('Text in {0}'.format(lang.lower()))
            })

        self.experience_fields = []

        Author = get_user_model()
        if self.author:
            if self.author.experience == Author.EXPERT:
                self.experience_fields = [self[s] for s in ('authors', 'allow_comments', 'template_name',
                                                            'registration_required', 'is_page')]

    def clean(self, *args, **kwargs):
        data = super(EditContentForm, self).clean()
        if not self.errors:
            data['page_texts'] = []
            for lang_code, lang in settings.LANGUAGES:
                text = data['text_%s' % lang_code]
                p = {'language_code': lang_code, 'text': text}
                data['page_texts'].append(p)
            return data

    def save(self, *args, **kwargs):
        obj = super(EditContentForm, self).save(*args, **kwargs)
        for pt in self.cleaned_data['page_texts']:
            tr = Content.objects.language(pt['language_code']).get(pk=obj.pk)
            tr.text = pt['text']
            tr.save()
        return obj
