from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

class ModalAdmin(SummernoteModelAdmin):
    fieldsets = [
        ('Настройки модального окна', {'fields': ['name', 'modal_id', 'type', 'text'], 'classes': ['collapse']}),
        ('Настройки для окна отправки писем', {'fields': ['email', 'mandrill_api_key', 'buttonText'], 'classes': ['collapse']}),
        ('Поле Email', {'fields': ['showEmail', 'requiredEmail'], 'classes': ['collapse']}),
        ('Поле Телефон', {'fields': ['showPhone', 'requiredPhone'], 'classes': ['collapse']}),
        ('Поле Сообщение', {'fields': ['showMessage', 'requiredMessage'], 'classes': ['collapse']}),
        ('Результирующее модальное окно', {'fields': ['resModal', 'resModalText'], 'classes': ['collapse']}),
    ]
    list_display = ('name', 'modal_id', 'email',)
    list_editable = ('modal_id', 'email',)

admin.site.register(Modal, ModalAdmin)