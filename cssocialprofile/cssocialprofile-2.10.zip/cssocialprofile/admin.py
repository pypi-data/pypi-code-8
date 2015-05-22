from django.contrib import admin
from django.db import models
from django.conf import settings

AUTH_USER_MODEL = getattr(settings,'AUTH_USER_MODEL', 'cssocialprofile.CSSocialProfile')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )
    search_fields = ['user__username',]

app_label, model_name = AUTH_USER_MODEL.split('.')
model = models.get_model(app_label, model_name)

#admin.site.register(model,UserProfileAdmin)
