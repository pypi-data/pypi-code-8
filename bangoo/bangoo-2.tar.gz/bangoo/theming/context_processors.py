from django.conf import settings

def act_theme(request):
    return {'ACT_THEME': getattr(request, 'ACT_THEME', settings.THEME)}