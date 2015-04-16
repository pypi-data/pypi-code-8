from __future__ import absolute_import
from __future__ import unicode_literals

import re
from copy import deepcopy
from collections import OrderedDict

from django import forms
from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.utils import six
from django.utils.datastructures import SortedDict
from django.utils.text import capfirst
from django.db.models.sql.constants import QUERY_TERMS
from django.utils.translation import ugettext as _

from .fields import LookupTypeField

try:
    from django.db.models.related import RelatedObject as ForeignObjectRel
except ImportError: # pragma: nocover
    # Django >= 1.8 replaces RelatedObject with ForeignObjectRel
    from django.db.models.fields.related import ForeignObjectRel


try:
    from django.db.models.constants import LOOKUP_SEP
except ImportError:  # pragma: nocover
    # Django < 1.5 fallback
    from django.db.models.sql.constants import LOOKUP_SEP  # noqa

from .filters import (Filter, CharFilter, BooleanFilter,
    ChoiceFilter, DateFilter, DateTimeFilter, TimeFilter, ModelChoiceFilter,
    ModelMultipleChoiceFilter, NumberFilter,
    MultipleChoiceFilter, DateRangeFilter, LOOKUP_MAP)

ORDER_BY_FIELD = 'o'


def get_declared_filters(bases, attrs, with_base_filters=True, model=None):
    """Return a OrderedDict of all filters declared in the class
    as opposed to the fields automatically built from the fields declared in Meta.
    
    Add reasonable defaults to (Multiple)ChoiceField and set the name if not present
    """
    filters = []
    for filter_name, obj in list(attrs.items()):
        if isinstance(obj, Filter):
            obj = attrs.pop(filter_name)
            if getattr(obj, 'name', None) is None:
                obj.name = filter_name
            add_suitable_choice_defaults(obj, model, filter_name)
            filters.append((filter_name, obj))
    filters.sort(key=lambda x: x[1].creation_counter)

    if with_base_filters:
        for base in bases[::-1]:
            if hasattr(base, 'base_filters'):
                filters = list(base.base_filters.items()) + filters
    else:
        for base in bases[::-1]:
            if hasattr(base, 'declared_filters'):
                filters = list(base.declared_filters.items()) + filters

    return OrderedDict(filters)

def add_suitable_choice_defaults(filter, model, filter_name):
    """Add choices from the model if field has no choices"""

    if isinstance(filter, (ChoiceFilter, MultipleChoiceFilter)):
        # (Multiple)ModelChoiceField already read from model
        if isinstance(filter.field, LookupTypeField):
            # LookupTypeField is a combo with real fields and select for lookup_types
            field = filter.field.fields[0]
        else:
            field = filter.field
        if not field.choices:
            model_field = get_model_field(model, filter_name)
            filter.field.choices = model_field.choices


def get_model_field(model, field_name):
    """Return the field of the model corresponing to field_name
    field name is a name found in Meta.fields, can be any of::
     
      date_sent
      date_sent__range
      user__groups__icontains
    
    :param model: the model that will be introspected
    :param field_name: the field_name, possibly with an operator and relations. 
    """
    parts = field_name.split(LOOKUP_SEP)
    if parts[-1] in QUERY_TERMS: # strip __in, __range and the like
        parts = parts[:-1]
    
    opts = model._meta
    for name in parts[:-1]:
        try:
            rel = opts.get_field_by_name(name)[0]
        except FieldDoesNotExist:
            return None
        if isinstance(rel, ForeignObjectRel):
            if hasattr(rel, "related_model"):
                # django >= 1.8 (ForeignObjectRel)
                opts = rel.related_model._meta
            else:
                # django < 1.8 (RelatedObject)
                opts = rel.opts
        else:
            model = rel.rel.to
            opts = model._meta
    try:
        rel, model, direct, m2m = opts.get_field_by_name(parts[-1])
    except FieldDoesNotExist:
        return None
    return rel


def filters_for_model(model, field_names=None, exclude=None, filter_for_field=None,
                      filter_for_reverse_field=None):
    """Return a field suitable to filter 'field_name'
    field name is a name found in Meta.fields, can be any of::
     
      date_sent
      date_sent__range
      user__groups__icontains
    
    :param model: the model that will be passed to get_model_field
    :param field_names: the list of field names found in Meta.fields
    """
    field_dict = OrderedDict()
    opts = model._meta
    if field_names is None:

        fields = [f.name for f in sorted(opts.fields + opts.many_to_many)]
    for fname in field_names:
        key = label = fname   
        if ':' in key:  # e.g.: organization__name__icontains:organization
            key, label = key.split(':')
        if '__' in label:
            label = _(label.split('__')[0])
        if exclude is not None and key in exclude:
            continue
        field = get_model_field(model, key)
        if field is None:
            field_dict[key] = None
            continue

        if isinstance(field, ForeignObjectRel):
            filter_ = filter_for_reverse_field(field, key, label)
        else:
            filter_ = filter_for_field(field, key, model, label)
        if filter_:
            field_dict[key] = filter_

    return field_dict


class FilterSetOptions(object):
    def __init__(self, options=None):
        self.model = getattr(options, 'model', None)
        self.fields = getattr(options, 'fields', None)
        self.exclude = getattr(options, 'exclude', None)

        self.order_by = getattr(options, 'order_by', False)

        self.form = getattr(options, 'form', forms.Form)


class FilterSetMetaclass(type):
    def __new__(cls, name, bases, attrs):
        try:
            parents = [b for b in bases if issubclass(b, FilterSet)]
        except NameError:
            # We are defining FilterSet itself here
            parents = None
        new_class = super(
            FilterSetMetaclass, cls).__new__(cls, name, bases, attrs)
        opts = new_class._meta = FilterSetOptions(
            getattr(new_class, 'Meta', None))
        declared_filters = get_declared_filters(bases, attrs, model=opts.model)

        if not parents:
            return new_class

        # fields is a list of possibly 1-level nested fields
        field_names = []
        for item in opts.fields:
             field_names += [item] if isinstance(item, basestring) else item
        if opts.model:
            filters = filters_for_model(opts.model, field_names, opts.exclude,
                                        new_class.filter_for_field,
                                        new_class.filter_for_reverse_field)
            filters.update(declared_filters)
        else:
            filters = declared_filters

        if None in filters.values():
            raise TypeError("Meta.fields contains a field that isn't defined "
                "on this FilterSet %s" % [key for key, val in filters.iteritems() if not val])

        new_class.declared_filters = declared_filters
        new_class.base_filters = filters
        return new_class


FILTER_FOR_DBFIELD_DEFAULTS = {
    models.AutoField: {
        'filter_class': NumberFilter
    },
    models.CharField: {
        'filter_class': CharFilter
    },
    models.TextField: {
        'filter_class': CharFilter
    },
    models.BooleanField: {
        'filter_class': BooleanFilter
    },
    models.DateField: {
        'filter_class': DateFilter
    },
    'DateRange': {
        'filter_class': DateRangeFilter
    },
    models.DateTimeField: {
        'filter_class': DateTimeFilter
    },
    models.TimeField: {
        'filter_class': TimeFilter
    },
    models.OneToOneField: {
        'filter_class': ModelChoiceFilter,
        'extra': lambda f: {
            'queryset': f.rel.to._default_manager.complex_filter(
                f.rel.limit_choices_to),
            'to_field_name': f.rel.field_name,
        }
    },
    models.ForeignKey: {
        'filter_class': ModelChoiceFilter,
        'extra': lambda f: {
            'queryset': f.rel.to._default_manager.complex_filter(
                f.rel.limit_choices_to),
            'to_field_name': f.rel.field_name
        }
    },
    models.ManyToManyField: {
        'filter_class': ModelMultipleChoiceFilter,
        'extra': lambda f: {
            'queryset': f.rel.to._default_manager.complex_filter(
                f.rel.limit_choices_to),
        }
    },
    models.DecimalField: {
        'filter_class': NumberFilter,
    },
    models.SmallIntegerField: {
        'filter_class': NumberFilter,
    },
    models.IntegerField: {
        'filter_class': NumberFilter,
    },
    models.PositiveIntegerField: {
        'filter_class': NumberFilter,
    },
    models.PositiveSmallIntegerField: {
        'filter_class': NumberFilter,
    },
    models.FloatField: {
        'filter_class': NumberFilter,
    },
    models.NullBooleanField: {
        'filter_class': BooleanFilter,
    },
    models.SlugField: {
        'filter_class': CharFilter,
    },
    models.EmailField: {
        'filter_class': CharFilter,
    },
    models.FilePathField: {
        'filter_class': CharFilter,
    },
    models.URLField: {
        'filter_class': CharFilter,
    },
    models.IPAddressField: {
        'filter_class': CharFilter,
    },
    models.CommaSeparatedIntegerField: {
        'filter_class': CharFilter,
    },
}


class BaseFilterSet(object):
    filter_overrides = {}
    order_by_field = ORDER_BY_FIELD

    def __init__(self, data=None, queryset=None, prefix=None):
        self.is_bound = data is not None
        self.data = data or {}
        if queryset is None:
            queryset = self._meta.model._default_manager.all()
        self.queryset = queryset
        self.form_prefix = prefix

        self.filters = deepcopy(self.base_filters)
        # propagate the model being used through the filters
        for filter_ in self.filters.values():
            filter_.model = self._meta.model

        for name, field in self.filters.iteritems():
            if isinstance(field, ChoiceFilter):
                # Add "Any" entry to choice fields.
                field.extra['choices'] = tuple([("", "-------"), ] + list(field.extra['choices']))

    def __iter__(self):
        for obj in self.qs:
            yield obj

    def __len__(self):
        return len(self.qs)

    def __getitem__(self, key):
        return self.qs[key]

    @property
    def qs(self):
        if not hasattr(self, '_qs'):
            qs = self.queryset.all()
            for name, filter_ in six.iteritems(self.filters):
                try:
                    if self.is_bound:
                        data = self.form[name].data
                    else:
                        data = self.form.initial.get(
                            name, self.form[name].field.initial)
                    val = self.form.fields[name].clean(data)
                    qs = filter_.filter(qs, val)
                except forms.ValidationError:
                    pass
            if self._meta.order_by:
                try:
                    order_field = self.form.fields[self.order_by_field]
                    data = self.form[self.order_by_field].data
                    value = order_field.clean(data)
                    if value:
                        qs = qs.order_by(value)
                except forms.ValidationError:
                    pass
            self._qs = qs
        return self._qs

    def count(self):
        return self.qs.count()

    @property
    def form(self):
        if not hasattr(self, '_form'):
            fields = OrderedDict([
                (name, filter_.field)
                for name, filter_ in six.iteritems(self.filters)])
            fields[self.order_by_field] = self.ordering_field
            Form = type(str('%sForm' % self.__class__.__name__),
                        (self._meta.form,), fields)
            if self.is_bound:
                self._form = Form(self.data, prefix=self.form_prefix)
            else:
                self._form = Form(prefix=self.form_prefix)
        return self._form

    def get_ordering_field(self):
        if self._meta.order_by:
            if isinstance(self._meta.order_by, (list, tuple)):
                if isinstance(self._meta.order_by[0], (list, tuple)):
                    # e.g. (('field', 'Display name'), ...)
                    choices = [(f[0], f[1]) for f in self._meta.order_by]
                else:
                    choices = [(f, capfirst(f)) for f in self._meta.order_by]
            else:
                # use the filter's label if provided
                choices = [(fltr.name or f, fltr.label or capfirst(f))
                           for f, fltr in self.filters.items()]
            return forms.ChoiceField(label=_("Ordering"), required=False,
                                     choices=choices)

    @property
    def ordering_field(self):
        if not hasattr(self, '_ordering_field'):
            self._ordering_field = self.get_ordering_field()
        return self._ordering_field

    @classmethod
    def filter_for_field(cls, field, name, model, label):
        """Mapping of field_name to filter

        :arg field:
        :arg name: the name of the field (a key of queryset filter)
        :arg model: the model of the 
        :arg label: the label to be used
        """
        parts = name.split(LOOKUP_SEP)
        if parts[-1] in QUERY_TERMS or parts[-1] == 'year':
            name = LOOKUP_SEP.join(parts[:-1])
            lookup_type = parts[-1]
        else:
            lookup_type = 'exact'
            
        filter_for_field = dict(FILTER_FOR_DBFIELD_DEFAULTS)
        filter_for_field.update(cls.filter_overrides)

        label = capfirst(_(label or field.name)) + (
            '' if lookup_type in ('exact', 'in') else " (%s)" % LOOKUP_MAP.get(lookup_type, ''))
        default = {
            'name': name,
            'label': label,
            'lookup_type' : lookup_type,
        }
        if field.choices:
            default['choices'] = field.choices
            if lookup_type == 'in':
                default['lookup_type'] = ('in_any', 'not_in_any')
                return MultipleChoiceFilter(**default)
            else:
                return ChoiceFilter(**default)

        if lookup_type == 'range':
            data = filter_for_field.get('DateRange') # implements __range
        else:
            data = filter_for_field.get(field.__class__)
        if data is None:
            # could be a derived field, inspect parents
            for class_ in field.__class__.mro():
                # skip if class_ is models.Field or object
                # 1st item in mro() is original class
                if class_ in (field.__class__, models.Field, object):
                    continue
                data = filter_for_field.get(class_)
                if data:
                    break
            if data is None:
                return
        if lookup_type == 'in':
            # 'Non model' cases are already considered
            filter_class = ModelMultipleChoiceFilter
            if isinstance(field, models.ForeignKey):
                default['lookup_type'] = ('in_any', 'not_in_any')
            else:
                default['lookup_type'] = ('in_any', 'not_in_any', 'in_all', 'not_in_all')
        else:
            filter_class = data.get('filter_class')
        default.update(data.get('extra', lambda field: {})(field))
        if filter_class is not None:
            filter_ = filter_class(**default)
            add_suitable_choice_defaults(filter_, model, name)
            return filter_

    @classmethod
    def filter_for_reverse_field(cls, field, name, label):
        rel = field.field.rel
        # TODO in new version of django_filters they fixed with...
        # queryset = field.field.model._default_manager.all()
        queryset = field.model._default_manager.all()
        default = {
            'name': name,
            'label': capfirst(rel.related_name),
            'queryset': queryset,
        }
        if rel.multiple:
            return ModelMultipleChoiceFilter(**default)
        else:
            return ModelChoiceFilter(**default)


class FilterSet(six.with_metaclass(FilterSetMetaclass, BaseFilterSet)):
    pass


def filterset_factory(model):
    meta = type(str('Meta'), (object,), {'model': model})
    filterset = type(str('%sFilterSet' % model._meta.object_name),
                     (FilterSet,), {'Meta': meta})
    return filterset
