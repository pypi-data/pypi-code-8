from django.contrib import admin
from .models import SwiftContainer

# Register your models here.
class SwiftContainerAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        SwiftContainer.create_container(title=obj.title)

admin.site.register(SwiftContainer, SwiftContainerAdmin)
