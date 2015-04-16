# -*- coding: utf-8 -*-
""".. _action-forms:

.. image:: ../images/actions.png


Extra Action Form
==================

Admin Actions_ in daily usage often require one or more
arguments. This extension provides an easy way to display a form to
fill in what needs to be passed to the actions. Namely:

#. Create a form that holds all the fields needed for any action and
   set ``action_form`` on your JumboModelAdmin pointing to that
   form. 

   .. caution:: Set any additional field as ``required = False``
      otherwise all actions that don't define that will will not let
      the form validate and you'll get "No action selected". See below
      the syntax to declare a required field just for one action

#. Configure which fields are needed for any action
   (``action_form_fields`` dict) and set attribute
   ``action_form_fields`` on your JumboModelAdmin

#. Modify ``change_list.html`` template to add 

    + templatetag to render ``admin/actions.html`` (inluded in
      ``{jmb.admin}result_list``) 

    + javascript to toggle visibility of the fields

   this step is already done in *jmb.admin* provided template


JumboModelAdmin.action_form
--------------------------------

When ModelAdmin has actions enabled, Django creates a form and attaches it to 
attribute ``action_form``, thought is not officially documented.
This action will hold 

* the selected action

* the selected ids or ``select_across`` boolean to say all records
  where selected.

Entending and modifying that form we make available any fields defined
in it.  The selected row will be available as a queryset, as usual.

You can use :meth:`JumboModelAdmin.get_action_form_instance` to
get an already validated form instance

This is used to specify a different form to add extra action fields.
To use this you need override class JumboActionForm. It's good idea
define these forms in admin_forms.py or in admin/forms.py::

    from jmb.admin.options import JumboActionForm

    class NewsletterActionForm(JumboActionForm):
        mailing_list = forms.ModelChoiceField(
            queryset=MailingList.objects.filter(status=1),
            label=_('Mailing list'),
            required=False,
            # This is automatically added if not specified. Used from JS to toggle extra action fields
            widget=forms.Select(attrs={'id': 'mailing_list', 'class': 'extra_action_field'})
        )

.. _action-form-fields:

JumboModelAdmin.action_form_fields
---------------------------------------

A dictionary to specify action and its extra fields to complete operation::

    from jmb.admin.options import JumboModelForm, JumboActionForm

    class NewsletterAdmin(JumboModelAdmin):

       def send_newsletter(self, request, queryset):
           form = self.get_form_action_instance(request)
           ...

       action_form = NewsletterActionForm
       action_form_fields = {
           'clone': [],
           'send_newsletter': ['mailing_list'],
           'resend_newsletter': ['mailing_list:required'],
        }

key is the action and value can be [] if there is not any extra fields
or a list of extra fields.  ``required`` it's used to specify that
that field is required. Example: ``send_newsletter``:
``['mailing_list:required']``.  When user select ``send newsletter``
action is required specify ``mailing_list`` to whom to send newsletter.

JumboModelAdmin.get_action_form_fields
--------------------------------------------

It's a method of JumboModelAdmin and it used to redefine action
extra fields dictionary To use these methods we rewrote
changelist_view in JumboModelAdmin adding get_action_form_fields
to extra_context and we overrode change_list.html template. 

API
===

.. autoclass:: JumboModelAdmin
   :members:

.. _Actions: https://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/#admin-actions

"""

from functools import update_wrapper
from django import forms, VERSION
from django import template
from django.core.urlresolvers import reverse
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as ugt
try:
    from django.contrib.admin.utils import unquote, flatten_fieldsets
except:
    from django.contrib.admin.util import unquote, flatten_fieldsets
from django.utils.encoding import force_unicode
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.utils.decorators import method_decorator
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.conf.urls import patterns, url
from ajax_inlines import AjaxParentModelAdmin
from django.contrib.admin import helpers

csrf_protect_m = method_decorator(csrf_protect)
try:
    atomic = transaction.atomic
except AttributeError: # django >= 1.6
    atomic = transaction.commit_on_success

# GET parameter for the URL to return to after change/add views. This lets the
# admin save the state of the changelist page through the change/add page.
#RETURN_GET_PARAM = '_return_to'

class JumboListPerPageForm(forms.Form):
    LIST_PER_PAGE_CHOICES = (
        (0, '---'),
        (10, 10), (25, 25),
        (50, 50), (100, 100),
    )
    choices = getattr(settings, 'LIST_PER_PAGE_CHOICES', LIST_PER_PAGE_CHOICES)
    list_per_page = forms.ChoiceField(label=_('List per page'), choices=choices)


class JumboActionForm(helpers.ActionForm):

    def __init__(self, *args, **kwargs):
        self.non_actions_fields = ['action','select_across']
        if 'action_form_fields' in kwargs:
            self.action_form_fields = kwargs.pop('action_form_fields')
        super(JumboActionForm, self).__init__(*args, **kwargs)
        for key, value in self.fields.iteritems():
            if key not in self.non_actions_fields:
                self.fields[key].widget.attrs['id'] = key
                try:
                    self.fields[key].widget.attrs['class'] = self.fields[key].widget.attrs['class'] + ' extra_action_field'
                except KeyError:
                    self.fields[key].widget.attrs['class'] = 'extra_action_field'
                
    def clean(self):
        cleaned_data = super(JumboActionForm, self).clean()
        if (
            hasattr(self, 'action_form_fields') and
            'action' in self.cleaned_data
        ):
            extra_action = self.cleaned_data['action']
            all_extra_actions_args_dict = self.action_form_fields
            if extra_action in all_extra_actions_args_dict:
                selected_action_extra_fields = all_extra_actions_args_dict[extra_action]
                error_flag = False
                for selected_action_arg in selected_action_extra_fields:
                    required_flag = False
                    field = selected_action_arg
                    if  ":" in selected_action_arg:
                        field, required = selected_action_arg.split(":")
                        if required and required == "required":
                            required_flag = True
                        if required_flag and not self.cleaned_data[field]:
                            self.fields[field].error_messages[field + "_error"] = \
                            _("No %s selected." % field.replace("_", " "))
                            error_flag = True
                if error_flag:
                    raise forms.ValidationError(_(""))
        return cleaned_data


class JumboModelAdmin(AjaxParentModelAdmin):
    class Media:

        js = ['jmb/js/collapsed_stacked_inlines.js']

    #: tabs: show tabs even if they're empty
    tabs_show_empty = True

    #: tabs: show tab lables sticky on top of the page
    tabs_sticky_on_top = False

    no_display_links = True
    list_per_page = 20
    save_on_top = True
    use_fancybox = False
    father_foreignkey_fancybox = None
    list_per_page_form = JumboListPerPageForm
    paginator_on_top = getattr(settings, 'PAGINATOR_ON_TOP', False)
    paginator_on_bottom = getattr(settings, 'PAGINATOR_ON_BUTTOM', True)

    def get_action_form_fields(self, request):
        """
        Return a :ref:`dictionary <action-form-fields>`
        to specify action and its extra fields to complete operation
        """
        try:
            return self.action_form_fields
        except:
            return None

    def get_action_form_instance(self, request):
        """
        Return an ``action_form``
        """
        ###########  Django's official code 1.7 -- begin ##############
        # There can be multiple action forms on the page (at the top
        # and bottom of the change list, for example). Get the action
        # whose button was pushed.
        try:
            action_index = int(request.POST.get('index', 0))
        except ValueError:
            action_index = 0

        # Construct the action form.
        data = request.POST.copy()
        data.pop(helpers.ACTION_CHECKBOX_NAME, None)
        data.pop("index", None)

        # Use the action whose button was pushed
        try:
            data.update({'action': data.getlist('action')[action_index]})
        except IndexError:
            # If we didn't get an action from the chosen form that's invalid
            # POST data, so by deleting action it'll fail the validation check
            # below. So no need to do anything here
            pass

        action_form = self.action_form(data, auto_id=None)
        ###########  DJango's official code 1.7 -- end ##############
        action_form.fields['action'].choices = self.get_action_choices(request)
        action_form.is_valid()
        return action_form

    def get_list_per_page_form(self, request):
        """
        Returns number of items appear on each paginated admin change list page
        """
        try:
            return self.list_per_page_form
        except:
            return None

    def get_list_display_links(self, request, list_display):
        return ('get_edit_icon',)

    def get_list_per_page(self):
        """
        Set how many items appear on each paginated admin change list page.
        This value is conditioned by settings.LIST_PER_PAGE.
        Example:
            LIST_PER_PAGE = {
                'content_content': 50,
                'content': 10,
                'all': 100,
            }
        """
        if hasattr(settings, 'LIST_PER_PAGE'):
            list_per_page = settings.LIST_PER_PAGE
            app_label = self.model._meta.app_label.lower()
            model_name = self.model._meta.verbose_name_raw.lower()

            key = app_label + '_' + model_name
            if key in list_per_page:
                return list_per_page[key]

            key = app_label
            if key in list_per_page:
                return list_per_page[key]

            key = 'all'
            if key in list_per_page:
                return list_per_page[key]

        return 50

    def get_readonly_fields(self, request, obj=None):
        readonly = ()
        fields = []
        fieldsets = self.get_fieldsets(request)
        if fieldsets:
            fields = flatten_fieldsets(fieldsets)

        if 'creator' in fields:
            readonly = readonly + ('creator',)
        if 'date_create' in fields:
            readonly = readonly + ('date_create',)
        if 'last_modifier' in fields:
            readonly = readonly + ('last_modifier',)
        if 'date_last_modify' in fields:
            readonly = readonly + ('date_last_modify',)
        return self.readonly_fields + readonly

    def get_changelist_instance(self, request):
        """Return a chagelist instance suitable to find out the real queryset represented bu result_list
        This function can be used in actions when the queryset is much faster then
        using the list of single ids
        """
        kw = dict(model=self.model, list_display=self.list_display,
            list_display_links=self.list_display_links, list_filter=self.list_filter,
            date_hierarchy=self.date_hierarchy, search_fields=self.search_fields, list_select_related=self.list_select_related,
            list_per_page=self.list_per_page, list_max_show_all=self.list_max_show_all,
            list_editable=self.list_editable, model_admin=self)
        return self.get_changelist(request)(request, **kw)

    def _getobj(self, request, object_id):
            opts = self.model._meta
            app_label = opts.app_label

            try:
                obj = self.queryset(request).get(pk=unquote(object_id))
            except self.model.DoesNotExist:
                obj = None

            if obj is None:
                raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})
            return obj

    def _wrap(self, view):
        def wrapper(*args, **kwargs):
            return self.admin_site.admin_view(view)(*args, **kwargs)
        return update_wrapper(wrapper, view)

    def _view_name(self, name):
        if VERSION[:2] < (1,6):
            info = self.model._meta.app_label, self.model._meta.module_name, name
        else:
            info = self.model._meta.app_label, self.model._meta.model_name, name
        return '%s_%s_%s' % info

    def has_change_permission(self, request, obj=None):
        has_change_permission = super(JumboModelAdmin, self).has_change_permission(request, obj)
        if VERSION[:2] < (1,6):
            model_name = self.model._meta.module_name
        else:
            model_name = self.model._meta.model_name

        if obj is None:
            if (
                has_change_permission or
                request.user.has_perm(self.model._meta.app_label + '.' + 'view_%s' % model_name) or
                request.user.has_perm(self.model._meta.app_label + '.' + 'list_%s' % model_name)
            ):
                return True
            return False
        else:
            if hasattr(obj, "can_be_modified"):
                if obj.can_be_modified():
                    return True
                else:
                    return False
            return has_change_permission

    def has_delete_permission(self, request, obj=None):
        has_delete_permission = super(JumboModelAdmin, self).has_delete_permission(request, obj)
        if hasattr(obj, "can_be_delete"):
            if obj.can_be_delete():
                return True
            else:
                return False

        return has_delete_permission

    def get_value_obj(self, obj, attribute):
        value = None
        try:
            value = getattr(obj, attribute)
        except:
            try:
                if hasattr(self, attribute):
                    value = getattr(self, attribute)(obj)
            except Exception, e:
                pass
        return value

    def detail_view(self, request, object_id, **kwargs):
        obj = self._getobj(request, object_id)
        opts = self.model._meta
        verbose_name = opts.verbose_name
        app_label = opts.app_label.lower()
        object_name = opts.object_name.lower()

        detail_fields = []
        d_values = {}
        #ricordarsi di aggiungere nel progetto
        #(r'^comments/', include('django.contrib.comments.urls')), 
        template_name = kwargs.get('template_name', 'detail.html')

        if hasattr(self, 'detail_display'):
            for f in self.detail_display:
                # Se e' una lista aggiunga tt i suoi campi ai detail_fields
                if type(f) == type([]) or type(f) == type(()):
                    detail_fields.append(f)
                    for subf in f:
                        d_values[subf] = self.get_value_obj(obj, subf)
                # Se la funzione e' presente nell'admin la chiamo e aggiungo il
                # valore ai detail fields
                elif hasattr(self, f):
                    detail_fields.append([f])
                    d_values[f] = getattr(self, f)(obj)
                # altrimenti cerco il valore dell'oggetto in maniera normale
                else:
                    detail_fields.append([f])
                    d_values[f] = self.get_value_obj(obj, f)

        context = {
            'title': _('Detail %s') % force_unicode(verbose_name),
            'object_id': object_id,
            'obj': obj,
            'is_popup': request.REQUEST.has_key('_popup'),
            'app_label': app_label,
            'opts': opts,
            'detail_fields': detail_fields,
            'd_values': d_values,
            'has_change_permission': self.has_change_permission(request, obj),
        }
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)

        return render_to_response([
            "admin/%s/%s/%s" % (app_label, object_name, template_name),
            "admin/%s/%s" % (app_label, template_name),
            "admin/%s" % template_name
        ], context, context_instance=context_instance)

    #nuovo nome, retrocompatibilità
    detail = detail_view

    @csrf_protect_m
    @atomic
    def import_data_view(self, request, form_url='', extra_context=None, **kwargs):
        "The 'import data' admin view for this model."
        from jmb.admin.forms import ImportDataForm
        from jmb.admin.import_data import ImportData
        from django.contrib import messages

        model = self.model
        opts = model._meta
        app_label = opts.app_label
        verbose_name = force_unicode(opts.verbose_name)

#        if not self.has_change_permission(request, obj):
#            raise PermissionDenied

        template_name = kwargs.get('template_name', 'import_data.html')
        breadcrumbs = (
            (_('Home'), '/admin/'),
            (_(app_label), '/admin/%s/' % app_label),
            (_(verbose_name), '/admin/%s/%s/' % (app_label, verbose_name)),
        )

        if request.method == 'POST':
            form = ImportDataForm(request.POST, request.FILES)
            if form.is_valid():
                file_source = form.cleaned_data['import_file']
                import_data = ImportData(
                    file_contents=file_source.read(), auto=True, model=model
                )
                import_data.read()
                if import_data.messages['inserted'] > 0:
                    messages.success(request, "%s righe inserite correttamente" % import_data.messages['inserted'])
                if import_data.messages['modified'] > 0:
                    messages.warning(request, "%s righe modificate correttamente" % import_data.messages['modified'])
                if import_data.messages['errors']:
                    for error in import_data.messages['errors']:
                        messages.error(request, error)
            else:
                messages.error(request, "Correggi l'errore qui sotto")
        else:
            form = ImportDataForm()

        context = {
            'title': _('Import %s') % verbose_name,
            'is_popup': "_popup" in request.REQUEST,
            'app_label': opts.app_label,
            'breadcrumbs': breadcrumbs,
            'import_form': form
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(
            [
                "admin/%s/%s/%s" % (opts.app_label, opts.object_name.lower(), template_name),
                "admin/%s/%s" % (opts.app_label, template_name),
                "admin/%s" % template_name
            ],
            context,
            context_instance=context_instance
        )

    @csrf_protect_m
    @atomic
    def export_data_view(self, request, form_url='', extra_context=None, **kwargs):
        "The 'export data' admin view for this model."
        from django.contrib import messages
        from jmb.admin.forms import ExportDataForm
        from jmb.admin import tasks

        model = self.model
        opts = model._meta
        app_label = opts.app_label
        verbose_name = force_unicode(opts.verbose_name)

        #        if not self.has_change_permission(request, obj):
        #            raise PermissionDenied

        template_name = kwargs.get('template_name', 'export_data.html')
        breadcrumbs = (
            (_('Home'), '/admin/'),
            (_(app_label), '/admin/%s/' % app_label),
            (_(verbose_name), '/admin/%s/%s/' % (app_label, verbose_name)),
        )

        if request.method == 'POST':
            form = ExportDataForm(request.POST, request.FILES)
            if form.is_valid():
                return tasks.create_xls(model)
            else:
                messages.error(request, "Correggi l'errore qui sotto")
        else:
            form = ExportDataForm()

        context = {
            'title': _('Export %s') % verbose_name,
            'is_popup': "_popup" in request.REQUEST,
            'app_label': opts.app_label,
            'breadcrumbs': breadcrumbs,
            'export_form': form
        }
        context.update(extra_context or {})
        context_instance = template.RequestContext(request, current_app=self.admin_site.name)
        return render_to_response(
            [
                "admin/%s/%s/%s" % (opts.app_label, opts.object_name.lower(), template_name),
                "admin/%s/%s" % (opts.app_label, template_name),
                "admin/%s" % template_name
            ],
            context,
            context_instance=context_instance
        )
    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['is_popup'] = request.GET.get("_popup", False)
        extra_context['action_form_fields'] = self.get_action_form_fields(request)
#        extra_context['action_form'] = self.get_action_form(request)
        extra_context['list_per_page_form'] = self.get_list_per_page_form(request)
        extra_context['paginator_on_top'] = self.paginator_on_top
        extra_context['paginator_on_bottom'] = self.paginator_on_bottom

        self.list_per_page = self.get_list_per_page()
        return super(JumboModelAdmin, self).changelist_view(request, extra_context)

    def get_urls(self):
        urls = super(JumboModelAdmin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        if VERSION[:2] < (1,6):
            info = self.model._meta.app_label, self.model._meta.module_name
        else:
            info = self.model._meta.app_label, self.model._meta.model_name

        my_urls = patterns(
            '',
            url(
                r'^(.+)/detail/$',
                self._wrap(self.detail),
                name=self._view_name('detail')
            ),
            url(
                r'^import_data/$',
                self.admin_site.admin_view(self.import_data_view),
                name='%s_%s_import_data' % info
            ),
            url(
                r'export_data/$',
                self.admin_site.admin_view(self.export_data_view),
                name="%s_%s_export_data" % info
            ),
        )
        return my_urls + urls


    def response_action(self, request, queryset):
        """
        Handle an admin action. This is called if a request is POSTed to the
        changelist; it returns an HttpResponse if the action was handled, and
        None otherwise.
        """

        # There can be multiple action forms on the page (at the top
        # and bottom of the change list, for example). Get the action
        # whose button was pushed.
        try:
            action_index = int(request.POST.get('index', 0))
        except ValueError:
            action_index = 0

        # Construct the action form.
        data = request.POST.copy()
        data.pop(helpers.ACTION_CHECKBOX_NAME, None)
        data.pop("index", None)

        # Use the action whose button was pushed
        try:
            data.update({'action': data.getlist('action')[action_index]})
        except IndexError:
            # If we didn't get an action from the chosen form that's invalid
            # POST data, so by deleting action it'll fail the validation check
            # below. So no need to do anything here
            pass

        if hasattr(self, 'action_form_fields') and self.action_form_fields:
            action_form = self.action_form(data, auto_id=None, action_form_fields=self.action_form_fields)
        else:
            action_form = self.action_form(data, auto_id=None)

        action_form.fields['action'].choices = self.get_action_choices(request)

        # If the form's valid we can handle the action.
        if action_form.is_valid():
            action = action_form.cleaned_data['action']
            select_across = action_form.cleaned_data['select_across']
            func = self.get_actions(request)[action][0]

            # Get the list of selected PKs. If nothing's selected, we can't
            # perform an action on it, so bail. Except we want to perform
            # the action explicitly on all objects.
            selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)
            if not selected and not select_across:
                # Reminder that something needs to be selected or nothing will happen
                msg = _("Items must be selected in order to perform "
                        "actions on them. No items have been changed.")
                self.message_user(request, msg, messages.WARNING)
                return None

            if not select_across:
                # Perform the action only on the selected objects
                queryset = queryset.filter(pk__in=selected)

            response = func(self, request, queryset)

            # Actions may return an HttpResponse-like object, which will be
            # used as the response from the POST. If not, we'll be a good
            # little HTTP citizen and redirect back to the changelist page.
            if isinstance(response, HttpResponse):
                return response
            else:
                return HttpResponseRedirect(request.get_full_path())
        else:
            msg = ""
            if hasattr(self, 'action_form_fields') and self.action_form_fields:
                if 'action' in action_form.cleaned_data:
                    selected_action = action_form.cleaned_data['action']
                    if selected_action in self.action_form_fields:
                        selected_action_args =  self.action_form_fields[selected_action]
                        for selected_action_argument in selected_action_args:
                            if  ":" in selected_action_argument:
                                field, required = selected_action_argument.split(":")
                                msg = action_form.fields[field].error_messages[field+"_error"]
                                self.message_user(request, msg, messages.WARNING)
            if not msg:
                msg = _("No action selected.")
                self.message_user(request, msg, messages.WARNING)
            return None

    def message_user(self, request, message, level=messages.INFO, extra_tags='',
                     fail_silently=False):
        """
        Send a message to the user. The default implementation
        posts a message using the django.contrib.messages backend.

        Exposes almost the same API as messages.add_message(), but accepts the
        positional arguments in a different order to maintain backwards
        compatibility. For convenience, it accepts the `level` argument as
        a string rather than the usual level number.
        """

        if not isinstance(level, int):
            # attempt to get the level if passed a string
            try:
                level = getattr(messages.constants, level.upper())
            except AttributeError:
                levels = messages.constants.DEFAULT_TAGS.values()
                levels_repr = ', '.join('`%s`' % l for l in levels)
                raise ValueError('Bad message level string: `%s`. '
                        'Possible values are: %s' % (level, levels_repr))

        messages.add_message(request, level, message, extra_tags=extra_tags,
                fail_silently=fail_silently)

    def get_detail_icon(self, obj):
        opts = self.model._meta
        app_label = opts.app_label.lower()
        object_name = opts.object_name.lower()
        return """
            <a class='iframe' href=%(reverse_url)s?_popup=1&nobuttons=1>
                <img src='%(url)sjmb/images/search.png' alt='%(window_title)s' title='%(window_title)s'/>
            </a>""" % {
                'reverse_url':reverse('%s:%s_%s_detail' % (
                    self.admin_site.name, app_label, object_name), args=(obj.pk,)
                ),
                'url':settings.STATIC_URL,
                'window_title':ugt("Detail %s" % object_name)
            }
    get_detail_icon.allow_tags = True
    get_detail_icon.short_description = _("V")

    def get_status_icon(self, obj):
        return obj.status
    get_status_icon.short_description = _("ST")
    get_status_icon.boolean = True
    get_status_icon.admin_order_field = 'status'

    def get_changelist_queryset(self, request):
        """
        Return a queryset that was correctly filtered by any filter (q= and filterset_class)
        """
        # stolen from changelist_view in Django 1.5
        opts = self.model._meta
        app_label = opts.app_label
        if not self.has_change_permission(request, None):
            raise PermissionDenied

        list_display = self.get_list_display(request)
        list_display_links = self.get_list_display_links(request, list_display)
        list_filter = self.get_list_filter(request)

        ChangeList = self.get_changelist(request)
        cl = ChangeList(request, self.model, list_display,
                        list_display_links, list_filter, self.date_hierarchy,
                        self.search_fields, self.list_select_related,
                        self.list_per_page, self.list_max_show_all, self.list_editable,
                        self)
        try:
            return cl.queryset
        except AttributeError:  # pre Django 1.6
            return cl.query_set



