# -*- coding: utf-8 -*-
import re
from copy import copy

import django 
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from jmb.filters import FilterSet

class AdvancedSearchModelAdmin(admin.ModelAdmin):

    def get_filterset_class(self, request):
        """Return a filterset_class suitable for advanced search
        first look if attribute ``advanced_search_fields``
        """
        fields = self.get_advanced_search_fields(request) 
        
        if fields:
            meta = type('Meta', (object,), {'fields': fields, 'model' : self.model})
            AdminFilterset = type('Admin%sFilterset' % self.model.__name__, 
                                  (FilterSet,),
                                  { 'Meta' : meta, 'fields' : fields})
            return AdminFilterset
        # elif hasattr(self, 'get_filterset_class'):
        #     return self.get_filterset()
        return None


    def get_advanced_search_fields(self, request):
        """
        Return the list of fields that should be used in advanced search

        :arg request: the request
        """
        return getattr(self, 'advanced_search_fields', None)

    def lookup_allowed(self, lookup, value):
        if hasattr(self, '_lookup_search'):
            if lookup in self._lookup_names:
                return True
        return super(AdvancedSearchModelAdmin, self).lookup_allowed(lookup, value)

    def get_changelist(self, request):
        return AdvancedSearchChangeList

    def get_queryset(self, request):

        search_filterset_class = self.get_filterset_class(request)

        if search_filterset_class:
            self.search_filterset = search_filterset_class(request.GET)
            self.search_form = self.search_filterset.form
            self.search_form.is_valid()

            self._lookup_names = re.findall('name="(?P<name>[^\"]*)"', str(self.search_form))

            qs = self.search_filterset.qs
            # ordering is the only remainig action taken in ModelAdmin.queryset...
            ordering = self.get_ordering(request)
            if ordering:
                qs = qs.order_by(*ordering)
            return qs
        try:
            return admin.ModelAdmin.get_queryset(self, request)
        except:
            return admin.ModelAdmin.queryset(self, request)

    if django.VERSION[:2] < (1,6):
        queryset = get_queryset
        del get_queryset
            
class AdvancedSearchChangeList(ChangeList):
    """
    A ChangeList that can hadle any filter condition
    added by the search_filterset's form.

    Django uses ModelAdmin's queryset method to initialize 
    ChangeList's root_queryset::

       self.root_queryset = model_admin.get_queryset(request)

    and at the end of the :meth:`__init__` it handles all filtering
    due according to filters and the like::

       self.queryset = self.get_queryset(request)

   that uses it as base for the root_queryset::

       qs = self.root_queryset

    Beside handling all parameters contained in the filterset
    we use and pop ``_list_per_page`` attribute
    """
    def get_queryset(self, request):
        # save a copy of the GET parameters 
        saved_params = copy(self.params)
        self.params.pop("_popup", None)
        self.params.pop("_json", None)
        ## ModelAdmin.get_queryset has already filtered the qs
        #  we now just need to hide the paramenters that belong to
        #  the filterset_class.form. Standard ChangeList would not
        #  know how to handle them
        if hasattr(self.model_admin, 'search_form'):
            search_form = self.model_admin.search_form

            if search_form.is_valid():
                for name in self.model_admin._lookup_names:
                    self.params.pop(name, None)

            # 1. query_str  2. list_per_page  3. settings.LIST_PER_PAGE
            self.list_per_page = int(self.params.pop(
                '_list_per_page', self.model_admin.get_list_per_page()))

        if django.VERSION[:2] >= (1,6):
            qs_result = ChangeList.get_queryset(self, request)
        else:
            qs_result = ChangeList.get_query_set(self, request)

        # restore the self.params list so that templatetag 'result_list'
        # can compose it correctly. In particular ordering and filters
        # need to know all parameters
        self.params = saved_params

        return qs_result

    if django.VERSION[:2] < (1,6):
        get_query_set = get_queryset
