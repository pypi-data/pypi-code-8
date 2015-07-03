from django.contrib import admin
from django.contrib.auth.models import User, Group
from django_yubikey_admin.models import YubiKey
from django_yubikey_admin.forms import AuthenticationForm
from django.conf import settings

class YubiKeyAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__first_name', 'user__email']
    list_display = ['user', 'otp']

# register the admin site, only if we're storing the YUBIKEY cache
if getattr(settings, 'DJANGO_ADMIN_YUBIKEY_CACHE', False):
    admin.site.register(YubiKey, YubiKeyAdmin)

# are we or are we not in grappelli land
try:
    import grappelli
    grappelli.VERSION  # purely to silence F401 in flake8
    admin.site.login_template = 'admin_grappelli_otplogin.html'
except ImportError:
    admin.site.login_template = 'adminotplogin.html'
admin.site.login_form = AuthenticationForm
