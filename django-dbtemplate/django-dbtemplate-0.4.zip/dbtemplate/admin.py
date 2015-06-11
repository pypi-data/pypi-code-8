import sys
import yaml
import cgitb
import mimetypes
from django import forms
from django.contrib import admin
from django.conf import settings
from django.conf.urls import patterns, url
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from dbtemplate.models import Template
from dbtemplate.tryrenderer import try_render_template

MAGIC_COOKIE = getattr(settings, 'DBTEMPLATE_MAGIC_COOKIE', 'i_know_what_i_do')


class TemplateAdminForm(forms.ModelForm):
    class Meta:
        model = Template
        fields = ("slug", "data", "specs")

    def clean_specs(self):
        try:
            data = yaml.load(self.cleaned_data['specs'])
        except Exception as e:
            raise forms.ValidationError(_(u"YAML parse error: %s") % e)

        if not isinstance(data, (dict,)):
            raise forms.ValidationError(_(u"Dictionary required."))

        if not data.get('description'):
            raise forms.ValidationError(_(u"Key 'description' required."))
        if not data.get('context'):
            raise forms.ValidationError(_(u"Key 'context' required."))

        return self.cleaned_data['specs']

    def clean(self):
        if self.errors:
            return
        try:
            specs = self.cleaned_data.get('specs') or self.instance.specs
            try_render_template(self.cleaned_data['data'], specs)
        except Exception as e:
            raise forms.ValidationError(_("Template rendering error: %s") % e)


class TemplateAdmin(admin.ModelAdmin):
    list_display = ("slug", "specs_description")
    search_fields = ("slug", "specs")
    actions = None
    form = TemplateAdminForm

    def render_change_form(self, request, context, obj, *args, **kwargs):
        if MAGIC_COOKIE not in request.COOKIES:
            context['context_specs'] = obj.get_context_specs()
        return super(TemplateAdmin, self).render_change_form(
            request, context, *args, **kwargs)

    def has_add_permission(self, request):
        return MAGIC_COOKIE in request.COOKIES

    def has_delete_permission(self, request, obj=None):
        return MAGIC_COOKIE in request.COOKIES

    def get_fields(self, request, obj=None):
        if MAGIC_COOKIE in request.COOKIES:
            return super(TemplateAdmin, self).get_fields(request, obj=obj)
        return ("slug", "data")

    def get_readonly_fields(self, request, obj=None):
        if MAGIC_COOKIE in request.COOKIES:
            return ()
        return ("slug",)

    def specs_description(self, obj):
        try:
            return yaml.load(obj.specs).get('description', '')
        except:
            return ""
    specs_description.short_description = _(u"description")

    def get_urls(self):
        urls = patterns(
            '',
            url(r'(\d+)/try/',
                self.admin_site.admin_view(self.try_render),
                name='database_template_try_render'),
        )
        return urls + super(TemplateAdmin, self).get_urls()

    def try_render(self, request, pk):
        dbtemplate = get_object_or_404(Template, pk=pk)
        if request.method in ("POST", "PUT"):
            data = request.POST["data"]
            dbtemplate.data = data
            if 'specs' in request.POST:
                dbtemplate.specs = request.POST['specs']

        try:
            result = try_render_template(dbtemplate.data, dbtemplate.specs)
            content_type = mimetypes.guess_type(dbtemplate.slug)[0]
            status_code = 200
        except:
            result = cgitb.html(sys.exc_info())
            content_type = "text/html"
            status_code = 500

        return HttpResponse(
            result,
            content_type=content_type,
            status=status_code,
        )

admin.site.register(Template, TemplateAdmin)
