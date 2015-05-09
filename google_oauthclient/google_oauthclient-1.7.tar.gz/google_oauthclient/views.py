from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from auth_helpers import *
from django.conf import settings

# Required views for Google+ authentication   
def revoke(request):
    r = revoke_token(request)
    return JsonResponse({'success':'token revoked'})

def oauth2_callback(request):
    result = handle_callback(request)
    return redirect(settings.REDIRECT_URI)

def login(request):
    if check_auth(request):
        # User has been authenticated, form response here.
        return JsonResponse(me(request))
    else:
        # Required redirect
        return redirect(handle_redirect())



    
    
    
