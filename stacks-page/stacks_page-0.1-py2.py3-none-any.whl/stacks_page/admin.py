from django.contrib import admin

from .admin_actions import stackspage_admin_actions
from .models import StacksPage, StacksPageSection


class StacksPageSectionInline(admin.StackedInline):
    model = StacksPageSection
    ordering = ['order']
    fieldsets = (
        (None, {
            'fields': (
                ('order', 'title_section'),
                ('title_menu', 'slug'),
                ('twitter_share_text',),
                ('content',)
            )
        }),
    )
    extra = 1
    prepopulated_fields = {"slug": ("title_menu",)}


class StacksPageAdmin(admin.ModelAdmin):
    actions = stackspage_admin_actions
    fieldsets = (
        ('Page Meta', {
            'fields': (
                ('title', 'slug'),
                ('description', 'twitter_share_text'),
                ('canonical_image',),
                ('publish',)
            )
        }),
    )
    superuser_fieldsets = fieldsets + ((
        'Superuser-only Fields', {
            'fields': (
                ('template_path', 'live_url'),
            )
        }
    ),)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [StacksPageSectionInline]
    list_display = ['title', 'live_url', 'publish']
    save_as = True

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return self.superuser_fieldsets
        return super(StacksPageAdmin, self).get_fieldsets(request, obj)

admin.site.register(StacksPage, StacksPageAdmin)
