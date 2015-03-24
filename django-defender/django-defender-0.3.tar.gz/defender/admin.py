from django.contrib import admin
from .models import AccessAttempt


class AccessAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'attempt_time',
        'ip_address',
        'user_agent',
        'username',
        'path_info',
        'login_valid',
    )

    list_filter = [
        'username',
    ]

    search_fields = [
        'ip_address',
        'username',
    ]

    date_hierarchy = 'attempt_time'

    fieldsets = (
        (None, {
            'fields': ('path_info', 'login_valid')
        }),
        ('Meta Data', {
            'fields': ('user_agent', 'ip_address')
        })
    )


admin.site.register(AccessAttempt, AccessAttemptAdmin)
