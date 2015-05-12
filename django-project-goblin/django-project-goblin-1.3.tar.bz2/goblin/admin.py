from django.contrib import admin
from django.db import models

# Register your models here.
from goblin.models import Project, Release, Change, PublishStatus, ProjectLink

class ProjectLinksInline(admin.TabularInline):
    model=ProjectLink
    exclude=('release',)
    
class ReleaseLinksInline(admin.TabularInline):
    model=ProjectLink
    exclude=('project',)
    
class ReleaseAdmin(admin.ModelAdmin):
    model=Project
    inlines = [
        ReleaseLinksInline
    ]
    
class ReleaseInline(admin.StackedInline):
    model=Release

class ProjectAdmin(admin.ModelAdmin):
    model=Project
    inlines = [
        ProjectLinksInline,
        ReleaseInline,
    ]

admin.site.register(ProjectLink)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Release, ReleaseAdmin)
admin.site.register(Change)
admin.site.register(PublishStatus)
