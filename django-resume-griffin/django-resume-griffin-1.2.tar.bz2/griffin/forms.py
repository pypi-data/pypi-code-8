from django.forms import ModelForm
from griffin.models import *

from django import forms
from django.utils.translation import ugettext_lazy as _
from griffin.fields import FuzzyDateInput
from griffin.models.attendance import Attendance
from griffin.models.entity import Project

class AttendanceForm(forms.ModelForm):
    date_begin = FuzzyDateInput()
    date_end = FuzzyDateInput(required=False,
            help_text=_("Leave blank if you still work here."))
    
    fields=('date_begin', 'date_end')

    class Meta:
        model=Attendance

class ProjectAdminForm(ModelForm):
    
    exclude=('',)
    
    class Meta:
        model=Project