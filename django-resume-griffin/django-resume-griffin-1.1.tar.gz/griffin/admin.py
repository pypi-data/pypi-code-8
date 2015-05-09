from django.contrib import admin
from . models import *
from griffin.forms import AttendanceForm

import logging
logger = logging.getLogger('RenegadeEngineer')

GOBLIN_URL='https://pypi.python.org/pypi/django-project-goblin/'
try:
    import goblin
    goblin_available = True
except ImportError as ie:
    logger.debug("Project Goblin <%s>"%GOBLIN_URL +
        "Has not been installed, so the GoblinProject model will not be " +
        "available.")
    goblin_available = True

SKILLS_INLINE = admin.StackedInline

class SkillsInline(SKILLS_INLINE):
    model=attendance.Attendance.skills.through

if goblin_available:
    #from goblin.models import Project
    #class GProjectInline(SKILLS_INLINE):
        #model = Project
    class GPSkillsInline(SKILLS_INLINE):
        model=attendance.GoblinProject.skills.through
    
    class GProjectAdmin(admin.ModelAdmin):
        model=attendance.GoblinProject
        fields = (
            'resume',
            'project',
            'duties',
            ('date_begin', 'date_end'),
            'skills',
        )

class AttendanceAdmin(admin.ModelAdmin):
    inlines = [
        SkillsInline,
    ]
    #form = AttendanceForm

class PositionInline(admin.TabularInline):
    model = attendance.Position

class AttendanceInline(admin.StackedInline):
    model = attendance.Attendance
    inlines = [
        PositionInline,
    ]

class ResumeAdmin(admin.ModelAdmin):
    inlines = [
        PositionInline,
    ]

class PositionInline(admin.StackedInline):
    model=attendance.Position

class CompanyInline(admin.StackedInline):
    model=entity.Company
    
class PositionAdmin(admin.ModelAdmin):
    model=attendance.Position

CONTACT_INLINE=admin.StackedInline

class EmailFieldInline(CONTACT_INLINE):
    model=contactfield.EmailFieldModel

class PhoneFieldInline(CONTACT_INLINE):
    model=contactfield.PhoneFieldModel

class WebPageFieldInline(CONTACT_INLINE):
    model=contactfield.WebPageFieldModel

class OtherContactFieldInline(CONTACT_INLINE):
    model = contactfield.OtherContactFieldModel

class StreetFieldInline(CONTACT_INLINE):
    model = contactfield.StreetFieldModel
    
class DegreeInline(admin.StackedInline):
    model = attendance.Degree
    
class MajorInline(admin.StackedInline):
    model = attendance.Major
    
class UniversityStudentAdmin(admin.ModelAdmin):
    inlines = [
        DegreeInline,
        MajorInline,
    ]

class EntityAdmin(admin.ModelAdmin):
    inlines = [
        EmailFieldInline,
        PhoneFieldInline,
        WebPageFieldInline,
        OtherContactFieldInline,
        StreetFieldInline,
    ]
    
my_models = (
    (attendance.Position, PositionAdmin),
    #attendance.Position,
    #(attendance.Attendance, AttendanceAdmin),
    attendance.Student,
    attendance.CollegeStudent,
    attendance.Major,
    attendance.Degree,
    #(attendance.UniversityStudent, UniversityStudentAdmin),
    attendance.UniversityStudent,
    
    contactfield.State,
    contactfield.City,
    contactfield.StreetFieldModel,
    contactfield.EmailFieldModel,
    contactfield.PhoneFieldModel,
    contactfield.WebPageFieldModel,
    contactfield.OtherContactFieldModel,
    
    #(entity.CorporateEntity, EntityAdmin),
    (entity.Person, EntityAdmin),
    (entity.Applicant, EntityAdmin),
    (entity.Company, EntityAdmin),
    (entity.School, EntityAdmin),
    #(entity.Project, EntityAdmin),
    
    (resume.Resume, ResumeAdmin),
    
    skill.Skill,
)

if goblin_available:
    my_models = my_models + ((attendance.GoblinProject, GProjectAdmin),)

for m in my_models:
    #logger.info("Registering %s"%(m,))
    if isinstance(m, list) or isinstance(m, tuple):
        admin.site.register(*m)
    else:
        admin.site.register(m)
