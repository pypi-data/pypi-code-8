# coding: utf-8

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from bangoo.core import bangoo_plugins
from bangoo.navigation.models import Menu
from .utils import create_path


class MenuOrderForm(forms.Form):
    METHOD_CHOCES = (
        ('insert', 'Insert'),
        ('move', 'Move')
    )

    method = forms.ChoiceField(choices=METHOD_CHOCES)
    source = forms.IntegerField()
    target = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        # TODO: Add unique check
        super(MenuOrderForm, self).__init__(*args, **kwargs)

        self.default_locale = settings.LANGUAGE_CODE.split('-')[0]

    def clean_target(self):
        try:
            target_id = self.cleaned_data['target']
            target_menu = Menu.handler.language(self.default_locale).get(id=target_id)

            return target_menu
        except Menu.DoesNotExist:
            raise ValidationError(_('Menu does not exist'))

    def clean_source(self):
        try:
            which_id = self.cleaned_data['source']
            which_menu = Menu.handler.language(self.default_locale).get(id=which_id)

            return which_menu
        except Menu.DoesNotExist:
            raise ValidationError(_('Menu does not exist'))


class MenuRenameForm(forms.Form):
    title = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        self.menu = kwargs.pop('menu')
        super(MenuRenameForm, self).__init__(*args, **kwargs)

        self.default_locale = settings.LANGUAGE_CODE.split('-')[0]

    def clean_title(self):
        old_title = self.menu.title
        self.menu.title = self.cleaned_data['title']

        path = create_path(self.menu)

        if Menu.handler.language(self.default_locale).filter(path=path).count() > 0:
            self.menu.title = old_title
            raise ValidationError(_('Menu with same path already exists'))

        return self.cleaned_data['title']


class MenuCreateForm(forms.Form):
    PLUGIN_CHOICES = [(key, key) for key in bangoo_plugins.apps if key != 'bangoo.media']

    plugin = forms.ChoiceField(choices=PLUGIN_CHOICES, label=_('Plugin'), initial=PLUGIN_CHOICES[0][0])
    parent = forms.ModelChoiceField(queryset=Menu.objects.language(settings.LANGUAGES[0][0]).all(), label=_('Parent'),
                                    required=False)

    def __init__(self, *args, **kwargs):
        super(MenuCreateForm, self).__init__(*args, **kwargs)
        self.fields['plugin'].choices = [(key, key) for key in bangoo_plugins.apps if key != 'bangoo.media']
        self.language_fields = {}

        for code, lang in settings.LANGUAGES:
            field_key = 'title_{0}'.format(code)
            self.fields[field_key] = forms.CharField(max_length=100, label=_('Title ({0})'.format(lang)), required=True)
            self.language_fields[field_key] = code

    def clean(self):
        data = super(MenuCreateForm, self).clean()
        code_dict = dict(settings.LANGUAGES)

        if not self.errors:
            for field_key, field_value in data.items():
                if field_key in self.language_fields:
                    code = self.language_fields[field_key]
                    path = '/{0}/'.format(slugify(field_value))

                    if 'parent' in data and data['parent']:
                        path = data['parent'].path + path[1:]

                    if Menu.objects.language(code).filter(path=path).exists():
                        raise ValidationError(_(
                            "Menu item '{0}' with the selected parent already exists in {1} language".format(
                                field_value, code_dict[code])
                        ))
        return data
