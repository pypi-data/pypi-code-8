# -*- coding: utf-8 -*-

from django import forms
from widgets import UbigeoWidget
from models import Ubigeo


class UbigeoField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        regions = Ubigeo.objects.filter(
            political_division=Ubigeo.POLITICAL_DIVISION_CHOICES.REGION
            )
        if kwargs.get('with_international') is None:
            regions = regions.exclude(reniec_code__startswith='9').order_by('name', 'id')

        self.fields = (
            forms.ModelChoiceField(
                queryset=regions,
                empty_label=u"",
                required=False),
            forms.ModelChoiceField(
                queryset=Ubigeo.objects.filter(
                    political_division=Ubigeo.POLITICAL_DIVISION_CHOICES.PROVINCE
                    ),
                empty_label=u"",
                required=False),
            forms.ModelChoiceField(
                queryset=Ubigeo.objects.filter(
                    political_division=Ubigeo.POLITICAL_DIVISION_CHOICES.DISTRICT
                    ),
                empty_label=u"",
                required=False,),
            )

        self.widget = UbigeoWidget(
            self.fields[0]._get_choices(),
            self.fields[1]._get_choices(),
            self.fields[2]._get_choices(),
            attrs_1=kwargs.get('attrs_1'),
            attrs_2=kwargs.get('attrs_2'),
            attrs_3=kwargs.get('attrs_3'),
            )
        super(UbigeoField, self).__init__(
            self.fields,
            self.widget,
            *args)

    def clean(self, value):
        """I know I shouldn't override this but, Fuck this shit.
        """
        if value is None:
            return None
        v1, v2, v3 = value
        if not v3 in (None, u''):
            return Ubigeo.objects.get(pk=v3)
        elif not v2 in (None, u''):
            return Ubigeo.objects.get(pk=v2)
        elif not v1 in (None, u''):
            return Ubigeo.objects.get(pk=v1)

    def compress(self, data_list):
        if data_list:
            if data_list[2]:
                return data_list[2]
            elif data_list[1]:
                return data_list[1]
            elif data_list[0]:
                return data_list[0]
        return None

    def prepare_value(self, value):
        if value is None:
            return None
        if type(value) is tuple or type(value) is list:
            r, p, d = value
        elif type(value) is int:
            u = Ubigeo.objects.get(pk=value)
            if u.political_division == Ubigeo.POLITICAL_DIVISION_CHOICES.DISTRICT:
                r, p, d = (u.parent.parent, u.parent, u)
            elif u.political_division == Ubigeo.POLITICAL_DIVISION_CHOICES.PROVINCE:
                r, p, d = (u.parent, u, 0)
            elif u.political_division == Ubigeo.POLITICAL_DIVISION_CHOICES.REGION:
                r, p, d = (u, 0, 0)
            else:
                r, p, d = (0, 0, 0)
        if r:
            self.fields[1].queryset = Ubigeo.objects.filter(parent=r)
        else:
            self.fields[1].queryset = None
        if p:
            self.fields[2].queryset = Ubigeo.objects.filter(parent=p)
        else:
            self.fields[2].queryset = None
        self.widget.provincias = self.fields[1]._get_choices()
        self.widget.distritos = self.fields[2]._get_choices()
        self.widget.decompress(d)
        return value
