from datetime import datetime
from django.contrib import admin


class BaseTabularInline (admin.TabularInline):

    """Forces username to be saved on add and change"""

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user_created = request.user.username
        if change:
            obj.user_modified = request.user.username
            obj.modified = datetime.today()
        super(BaseTabularInline, self).save_model(request, obj, form, change)
