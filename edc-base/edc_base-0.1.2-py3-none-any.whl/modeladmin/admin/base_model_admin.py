import logging
import re
import six

from datetime import datetime

from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


from ...modeladmin.exceptions import NextUrlError

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseModelAdmin (admin.ModelAdmin):

    list_per_page = 15

    instructions = ['Please complete the questions below.']
    required_instructions = (
        'Required questions are in bold. '
        'When all required data has been entered click SAVE to return to the dashboard '
        'or SAVE NEXT to go to the next form (if available). Additional questions may be '
        'required or may need to be corrected when you attempt to save.')

    def __init__(self, *args):
        if not isinstance(self.instructions, list):
            raise ImproperlyConfigured(
                'ModelAdmin {0} attribute \'instructions\' must be a list.'.format(self.__class__))
        if not isinstance(self.required_instructions, six.string_types):
            raise ImproperlyConfigured(
                'ModelAdmin {0} attribute \'required_instructions\' must be a list.'.format(self.__class__))
        super(BaseModelAdmin, self).__init__(*args)

    def save_model(self, request, obj, form, change):
        self.update_modified_stamp(request, obj, change)
        super(BaseModelAdmin, self).save_model(request, obj, form, change)

    def contribute_to_extra_context(self, extra_context, object_id=None):
        return extra_context

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or dict()
        extra_context = self.contribute_to_extra_context(extra_context)
        extra_context.update(instructions=self.instructions)
        extra_context.update(required_instructions=self.required_instructions)
        extra_context.update(form_language_code=request.GET.get('form_language_code', ''))
        if request.GET.get('group_title'):
            extra_context.update(
                title=('{group_title}: Add {title}').format(
                    group_title=request.GET.get('group_title'),
                    title=self.model._meta.verbose_name
                )
            )
        extra_context.update(self.get_dashboard_context(request))
        return super(BaseModelAdmin, self).add_view(request, form_url=form_url, extra_context=extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or dict()
        extra_context = self.contribute_to_extra_context(extra_context, object_id)
        extra_context.update(instructions=self.instructions)
        extra_context.update(required_instructions=self.required_instructions)
        extra_context.update(form_language_code=request.GET.get('form_language_code', ''))
        if request.GET.get('group_title'):
            extra_context.update(
                title=('{group_title}: Add {title}').format(
                    group_title=request.GET.get('group_title'),
                    title=self.model._meta.verbose_name))
        extra_context.update(self.get_dashboard_context(request))
        result = super(BaseModelAdmin, self).change_view(
            request, object_id, form_url=form_url, extra_context=extra_context)
        # Look at the referrer for a query string '^.*\?.*$'
        ref = request.META.get('HTTP_REFERER', '')
        if ref.find('?') != -1:
            # We've got a query string, set the session value
            request.session['filtered'] = ref
        return result

    def response_add(self, request, obj, post_url_continue=None):
        """Redirects as default unless keyword 'next' is in the GET and is a
        valid url_name (e.g. can be reversed using other GET values)."""
        http_response_redirect = super(BaseModelAdmin, self).response_add(request, obj, post_url_continue)
        custom_http_response_redirect = None
        if '_addanother' not in request.POST and '_continue' not in request.POST:
            if request.GET.get('next'):
                custom_http_response_redirect = self.response_add_redirect_on_next_url(
                    request.GET.get('next'),
                    request,
                    obj,
                    post_url_continue,
                    post_save=request.POST.get('_save'),
                    post_save_next=request.POST.get('_savenext'),
                    post_cancel=request.POST.get('_cancel'))
        return custom_http_response_redirect or http_response_redirect

    def response_change(self, request, obj, post_url_continue=None):
        """Redirects as default unless keyword 'next' is in the GET and is a
        valid url_name (e.g. can be reversed using other GET values)."""
        http_response_redirect = super(BaseModelAdmin, self).response_add(request, obj, post_url_continue)
        custom_http_response_redirect = None
        if '_addanother' not in request.POST and '_continue' not in request.POST:
            # look for session variable "filtered" set in change_view
            if request.session.get('filtered', None):
                if 'next=' not in request.session.get('filtered'):
                    # return to the changelist using the same changelist filter, e.g. ?q=Erik
                    custom_http_response_redirect = HttpResponseRedirect(request.session['filtered'])
                    request.session['filtered'] = None
            if request.GET.get('next'):
                # go back to the dashboard or something custom
                custom_http_response_redirect = self.reponse_change_redirect_on_next_url(
                    request.GET.get('next'),
                    request,
                    obj,
                    post_url_continue,
                    post_save=request.POST.get('_save'),
                    post_save_next=request.POST.get('_savenext'),
                    post_cancel=request.POST.get('_cancel'))
        return custom_http_response_redirect or http_response_redirect

    def response_add_redirect_on_next_url(
            self, next_url_name, request, obj, post_url_continue, post_save=None,
            post_save_next=None, post_cancel=None):
        """Returns a http_response_redirect when called using the next_url_name.

        Users may override to to add special handling for a named url next_url_name."""
        custom_http_response_redirect = None
        if not next_url_name:
            raise NextUrlError(
                'Attribute \'next_url_name\' may not be none. Check the GET parameter \'next\' in your url.')
        else:
            url = None
            if next_url_name in ['changelist', 'add']:
                # reverse to a default admin url
                # next_url_name is "mode" and is being used to get to the default admin add or changelist
                mode = next_url_name
                app_label = request.GET.get('app_label')
                module_name = request.GET.get('module_name')
                if module_name:
                    module_name = module_name.lower()
                if not app_label or not module_name:
                    raise NextUrlError(
                        'next_url_name shortcut \'{0}\' (next={0}) requires GET attributes '
                        '\'app_label\' and \'module_name\'. Got app_label={1}, module_name={2}.'.format(
                            next_url_name, app_label, module_name))
                url = reverse(
                    'admin:{app_label}_{module_name}_{mode}'.format(
                        app_label=app_label, module_name=module_name, mode=mode))
            else:
                try:
                    # try to reverse using the next_url_name and the all values in the GET string
                    # less ['next', 'dashboard_id', 'dashboard_model', 'dashboard_type', 'show'].
                    # dashbord_xx values are excluded because we do not want to intercept a dashboard url here
                    kwargs = dict()
                    for key, value in list(request.GET.items()):
                        if key not in ['next', 'dashboard_id', 'dashboard_model', 'dashboard_type', 'show']:
                            kwargs.update({key: value})
                    if kwargs:
                        url = reverse(next_url_name, kwargs=kwargs)
                except NoReverseMatch:
                    # ok, failed to reverse with exactly what was given
                    dashboard_id = request.GET.get('dashboard_id')
                    dashboard_model = request.GET.get('dashboard_model')
                    dashboard_type = request.GET.get('dashboard_type')
                    entry_order = request.GET.get('entry_order')
                    visit_attr = request.GET.get('visit_attr')
                    help_link = request.GET.get('help_link')  # help link added to custom change form
                    show = request.GET.get('show', 'any')

            # at this point we may have a url
            #   1. an admin url (default)
            #   2. a reversed url using next= and all other non-dashboard GET values
            # if we do not have a url, then we have set the dashboard values
            # and will treat the next url as a dashboard url

            if not url:
                if post_save:
                    # will default to a url that takes us back to the subject dashoard below
                    pass
                elif post_save_next:
                    # post_save_next is only available to subject forms
                    # try to reverse using method next_url_in_scheduled_entry_meta_data()
                    # which jumps to the next form on the subject dashboard instead of going
                    # back to the subject dashboard
                    try:
                        next_url, visit_model_instance, entry_order = self.next_url_in_scheduled_entry_meta_data(obj, visit_attr, entry_order)
                        if next_url:
                            url = ('{next_url}?next={next}&dashboard_type={dashboard_type}&dashboard_id={dashboard_id}'
                                   '&dashboard_model={dashboard_model}&show={show}{visit_attr}{visit_model_instance}{entry_order}{help_link}'
                                   ).format(next_url=next_url,
                                            next=next_url_name,
                                            dashboard_type=dashboard_type,
                                            dashboard_id=dashboard_id,
                                            dashboard_model=dashboard_model,
                                            show=show,
                                            visit_attr='&visit_attr={0}'.format(visit_attr),
                                            visit_model_instance='&{0}={1}'.format(visit_attr, visit_model_instance.pk),
                                            entry_order='&entry_order={0}'.format(entry_order),
                                            help_link='&help_link={0}'.format(help_link))
                    except NoReverseMatch:
                        pass
                elif post_cancel:
                    # cancel goes back to the dashboard
                    # FIXME: i think the URL for the cancel button/link is calculated for by the dashboard
                    #        for the template or reversed on the template, so this might
                    #        be code that cannot be reached
                    url = reverse(
                        'subject_dashboard_url', kwargs={  # TODO: this defaults to the value subject_dashboard_url, not the variable!!!
                            'dashboard_type': dashboard_type,
                            'dashboard_id': dashboard_id,
                            'dashboard_model': dashboard_model,
                            'show': show})
                else:
                    pass
            if not url:
                # default back to the dashboard
                url = self.reverse_next_to_dashboard(next_url_name, request, obj)
            custom_http_response_redirect = HttpResponseRedirect(url)
        return custom_http_response_redirect

    def reponse_change_redirect_on_next_url(
            self, next_url_name, request, obj, post_url_continue,
            post_save, post_save_next, post_cancel):
        """Returns an http_response_redirect if next_url_name can be reversed otherwise None.

        Users may override to to add special handling for a named url next_url_name.

        .. note:: currently this assumes the next_url_name is reversible using dashboard
        criteria or returns nothing."""
        custom_http_response_redirect = None
        if 'dashboard' in next_url_name:   # FIXME: find a better way to intercept dashboard urls and ignore others
            url = self.reverse_next_to_dashboard(next_url_name, request, obj)
            custom_http_response_redirect = HttpResponseRedirect(url)
            request.session['filtered'] = None
        else:
            change_list_q = ''
            kwargs = {}
            [kwargs.update({key: value}) for key, value in list(request.GET.items()) if key != 'next']
            try:
                if '_add' in next_url_name:
                    url = reverse(next_url_name)
                elif '_changelist' in next_url_name:
                    url = reverse(next_url_name)
                    if kwargs.get('q', None) and kwargs.get('q') != 'None':
                        change_list_q = '?q={}'.format(kwargs.get('q'))
                else:
                    url = reverse(next_url_name, kwargs=kwargs)
            except NoReverseMatch:
                try:
                    # try reversing to the url from just section_name
                    url = reverse(next_url_name, kwargs={'section_name': kwargs.get('section_name')})
                except NoReverseMatch:
                    raise NoReverseMatch(
                        'response_change failed to reverse url \'{0}\' with kwargs {1}. Is this a '
                        'dashboard url?'.format(next_url_name, kwargs))
            custom_http_response_redirect = HttpResponseRedirect('{}{}'.format(url, change_list_q))
            request.session['filtered'] = None
        return custom_http_response_redirect

    def get_form_prep(self, request, obj=None, **kwargs):
        pass

    def get_form_post(self, form, request, obj=None, **kwargs):
        return form

    def get_form(self, request, obj=None, **kwargs):
        """Overrides to check if supplemental fields have been defined in the admin class.

            * get_form is called once to render and again to save, e.g. on GET and then on POST.
            * Need to be sure that the same supplemental choice is given on GET and POST for both
              add and change.
        """
        self.get_form_prep(request, obj, **kwargs)
        form = super(BaseModelAdmin, self).get_form(request, obj, **kwargs)
        form = self.get_form_post(form, request, obj, **kwargs)
        form = self.auto_number(form)
        return form

    def update_modified_stamp(self, request, obj, change):
        """Forces username to be saved on add/change and other stuff, called from save_model"""
        if not change:
            obj.user_created = request.user.username
        if change:
            obj.user_modified = request.user.username
            obj.modified = datetime.today()

    def insert_translation_help_text(self, form):
        WIDGET = 1
        for fld in list(form.base_fields.items()):
            fld[WIDGET].translation_help_text = str('translation')
        return form

    def auto_number(self, form):
        WIDGET = 1
        auto_number = True
        if 'auto_number' in dir(form._meta):
            auto_number = form._meta.auto_number
        if auto_number:
            for index, fld in enumerate(form.base_fields.items()):
                if not re.match(r'^\d+\.', str(fld[WIDGET].label)):
                    fld[WIDGET].label = '{0}. {1}'.format(str(index + 1), str(fld[WIDGET].label))
        return form

    def get_dashboard_context(self, request):
        return {'subject_dashboard_url': request.GET.get('next', ''),
                'dashboard_type': request.GET.get('dashboard_type', ''),
                'dashboard_model': request.GET.get('dashboard_model', ''),
                'dashboard_id': request.GET.get('dashboard_id', ''),
                'show': request.GET.get('show', 'any')}

    def reverse_next_to_dashboard(self, next_url_name, request, obj, **kwargs):
        url = ''
        if next_url_name and request.GET.get('dashboard_id') and request.GET.get('dashboard_model') and request.GET.get('dashboard_type'):
            kwargs = {'dashboard_id': request.GET.get('dashboard_id'),
                      'dashboard_model': request.GET.get('dashboard_model'),
                      'dashboard_type': request.GET.get('dashboard_type')}
            # a subject dashboard url will also have "show"
            if request.GET.get('show'):  # this may fail if a subject template does not set show
                kwargs.update({'show': request.GET.get('show', 'any')})
            url = reverse(next_url_name, kwargs=kwargs)
        elif next_url_name in ['changelist', 'add']:
            app_label = request.GET.get('app_label')
            module_name = request.GET.get('module_name').lower()
            mode = next_url_name
            url = reverse('admin:{app_label}_{module_name}_{mode}'.format(app_label=app_label, module_name=module_name, mode=mode))
        else:
            # normally you should not be here.
            try:
                kwargs = self.convert_get_to_kwargs(request, obj)
                url = reverse(next_url_name, kwargs=kwargs)
            except NoReverseMatch:
                try:
                    # try reversing to the url from just section_name
                    url = reverse(next_url_name, kwargs={'section_name': kwargs.get('section_name')})
                except NoReverseMatch:
                    raise NoReverseMatch('response_add failed to reverse url \'{0}\' with kwargs {1}. Is this a dashboard url?'.format(next_url_name, kwargs))
            except:
                raise
        return url

    def convert_get_to_kwargs(self, request, obj):
        kwargs = dict()
        for k, v in list(request.GET.items()):
            kwargs.update({str(k): ''.join(str(i) for i in request.GET.get(k))})
            if not v:
                if k in dir(obj):
                    try:
                        kwargs.update({str(k): getattr(obj, k)})
                    except AttributeError:
                        pass
        if 'next' in kwargs:
            del kwargs['next']
        if 'csrfmiddlewaretoken' in kwargs:
            del kwargs['csrfmiddlewaretoken']
        return kwargs

    def next_url_in_scheduled_entry_meta_data(self, obj, visit_attr, entry_order):
        """Returns a tuple with the reverse of the admin url for the next
        model listed in scheduled_entry_meta_data.

        If there is not a "next" model, returns an empty tuple (None, None, None).

        Called from response_add and response_change."""
        from edc_entry.helpers import ScheduledEntryMetaDataHelper
        from edc_rule_groups.classes import site_rule_groups
        next_url_tuple = (None, None, None)
        if visit_attr and entry_order:
            visit_instance = getattr(obj, visit_attr)
            site_rule_groups.update_rules_for_source_model(obj, visit_instance)
            next_entry = ScheduledEntryMetaDataHelper(
                visit_instance.get_appointment(),
                visit_instance.__class__, visit_attr
            ).get_next_entry_for(entry_order)
            if next_entry:
                next_url_tuple = (
                    reverse('admin:{0}_{1}_add'.format(
                        next_entry.entry.content_type_map.app_label,
                        next_entry.entry.content_type_map.module_name)),
                    visit_instance,
                    next_entry.entry.entry_order
                )
        return next_url_tuple
