from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html
from cmsplugin_latest.utils import *
from django.apps import apps as django_apps
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from itertools import chain

from cmsplugin_latest.models import OrderBy

import logging
logger = logging.getLogger('cmsplugin_latest')

class ModelSelectionWidget(forms.Select):
    def __init__(self):
        super(ModelSelectionWidget, self).__init__(
            choices=list(get_model_choices()))
        
    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<p><a href="#" class="model-selection" ' +
                            'id="{0}"{1}>{2}</a></p>',
                           option_value,
                           selected_html,
                           force_text(option_label))
    
    def render(self, name, value, attrs=None, choices=[]):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<div{0}>', flatatt(final_attrs))]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append('</div>')
        return mark_safe('\n'.join(output))

class ModelSelectionInput(forms.Field):
    
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'widget' : ModelSelectionWidget(),
            'label' : "Model",
            'help_text' : _("Select a model"),
        })
        super(ModelSelectionInput, self).__init__(*args, **kwargs)
        
class DivWrapRadioSelect(forms.RadioSelect):
    
    def __init__(self, model, *args, **kwargs):
        self.model = model
        super(DivWrapRadioSelect, self).__init__(*args, **kwargs)
        
    def render_option(self, selected_choices, option_value, option_label):
        return None
    
    def render(self, name, value, attrs=None):
        rendered = super(DivWrapRadioSelect, self).render(
            name, value, attrs)
        model_name = self.model._meta.__dict__['model_name']
        model_title = self.model._meta.verbose_name_raw.title()
        return mark_safe('<div id="%s" '%model_name +
            'class="model-fields-selection" ' +
            flatatt(attrs) +
            ' >\n<h3 class="model-name">%s</h3>'%model_title +
            '\n%s\n'%rendered +
            '\n</div>')
        
class ModelFieldChoiceWidget(forms.MultiWidget):
    
    def __init__(self):
        self.models = get_models()
        
        _widgets = []
        
        for m in self.models:
            choices = get_model_field_choices(m)
            _widgets.append(DivWrapRadioSelect(model=m, choices=choices))
            
        super(ModelFieldChoiceWidget, self).__init__(
            widgets=_widgets)
            
    def render(self, *args, **kwargs):
        rendered = super(ModelFieldChoiceWidget, self).render(*args, **kwargs)
        return mark_safe(
            '<div id="model-selection-right">' +
            rendered + 
            '</div>'
        )
            
    def decompress(self, value):
        if not value:
            return [None]*len(self.models)
        return value.split(',')
        
class ModelFieldChoiceInput(forms.MultiValueField):

    def __init__(self):
        self.models = get_models()
        
        _fields = []
        
        for m in self.models:
            logger.debug("Getting field choices for %s"%m)
            choices = get_model_field_choices(m)
            for c in choices:
                logger.debug(">\t%s"%(c,))
            _fields.append(forms.ChoiceField(choices=choices))
            
        super(ModelFieldChoiceInput, self).__init__(
            fields=_fields, widget=ModelFieldChoiceWidget())
            
    def compress(self, data_list):
        return ','.join(data_list)

class ModelRenderForm(forms.ModelForm):
    
    model = ModelSelectionInput()
    field = ModelFieldChoiceInput()
    
    class Meta:
        model = OrderBy
