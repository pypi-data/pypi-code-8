#-*- coding:utf-8 -*-

from django.contrib import admin

from oauth2app.models import *

class AccessTokenAdmin(admin.ModelAdmin):
    list_display = ('client', 'user', 'token', 'refresh_token', 'get_expire_time',)
    list_display_links = ('client', 'user', 'token',)
    ordering = ('-id',)
    readonly_fields=  ('client', 'user', 'token', 'refresh_token', 'get_expire_time','scope','refreshable',)
    fields = ( 'client', 'expire','user', 'token', 'refresh_token', 'get_expire_time','scope','refreshable',)
    list_per_page = 30
    save_on_top = True    
    

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'description', 'key', 'secret','redirect_uri')
    list_display_links = ('name', 'key', 'secret',)
    ordering = ('-id',)
#    readonly_fields= ('name', 'user', 'description', 'key', 'secret','redirect_uri')
    fields =('name', 'user', 'description', 'key', 'secret','redirect_uri')
    list_per_page = 30
    save_on_top = True    
    
    
admin.site.register(Client,ClientAdmin)
admin.site.register(AccessRange)
admin.site.register(AccessToken,AccessTokenAdmin)
admin.site.register(Code)
admin.site.register(MACNonce)
