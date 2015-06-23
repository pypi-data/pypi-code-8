# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from mapshop.models import Category, Product, Client
from django.forms import ModelForm




class ClientForm(ModelForm):
    class Meta:
        model = Client




__author__ = '1'
from django import forms


class ProductFilterForm(forms.Form):
    ASC = '1'
    DSC = '-1'
    ORDER_RATE = '1'
    ORDER_PRICE = '2'
    CHOICES = ((ASC, mark_safe('&#8593;')), (DSC, mark_safe('&#8595;')))
    ORDER_CHOICES = ((ORDER_RATE, u'По рейтингу'), (ORDER_PRICE, u'По цене'))
    category = forms.ModelChoiceField(Category.objects.all(), label=u'Категория', required=False)
    rate = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label=u'Рейтинг', required=False)
    price = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, label=u'Цена', required=False)
    order = forms.ChoiceField(widget=forms.RadioSelect, choices=ORDER_CHOICES, label=u'Порядок сортировки', required=False)

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop('initial', {})
        initial.setdefault('rate', self.ASC)
        initial.setdefault('price', self.ASC)
        initial.setdefault('order', self.ORDER_RATE)
        super(ProductFilterForm, self).__init__(initial=initial, *args, **kwargs)

    def _get_rate_ordering(self):
        return 'rate' if self.cleaned_data.get('rate') == self.ASC else '-rate'

    def _get_price_ordering(self):
        return 'price' if self.cleaned_data.get('price') == self.ASC else '-price'

    def clean_rate(self):
        return self.cleaned_data.get('rate', self.ASC)

    def clean_price(self):
        return self.cleaned_data.get('price', self.ASC)

    def clean_order(self):
        return self.cleaned_data.get('order', self.ORDER_RATE)

    def get_products(self):
        self.full_clean()
        products = Product.objects.all()
        if self.is_bound:
            cleaned_data = self.cleaned_data
            if cleaned_data.get('category'):
                products = products.filter(category=cleaned_data.get('category'))
            _ordering =[]
            _order = cleaned_data.get('order')
            if _order == self.ORDER_RATE:
                _ordering.append(self._get_rate_ordering())
                _ordering.append(self._get_price_ordering())
            else:
                _ordering.append(self._get_price_ordering())
                _ordering.append(self._get_rate_ordering())
            products = products.order_by(*_ordering)
        return products

