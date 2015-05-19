from django.contrib import admin

from . import models

class PostbackLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'processed', 'payment_status', 'payment_amount', 'transaction_id', 'result', 'remote_ip', 'user_agent', 'post')
admin.site.register(models.PostbackLog, PostbackLogAdmin)