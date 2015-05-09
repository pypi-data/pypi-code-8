from django.contrib.auth.models import User
from django.conf import settings
from oauth2client.client import OAuth2WebServerFlow
import urllib
import json

def me(request):
    if 'token' in request.session:
        uri = 'https://www.googleapis.com/plus/v1/people/me?access_token=' + request.session['token']
        r = urllib.urlopen(uri)
        u = json.loads(r.read())
        return u
    else:
        return {'message':'Not authenticated'}

def check_auth(request):
    if 'token' in request.session:
        try:
            gmail = get_gmail(request.session['token'])
            if not gmail:
                return False
            else:
                user = User.objects.get(email=gmail) 
                return True
        except User.DoesNotExist:
            pass
    return False

def get_gmail(token):
    uri = 'https://www.googleapis.com/plus/v1/people/me?access_token=' + token
    r = urllib.urlopen(uri)
    try:
        gmail = json.loads(r.read())['emails'][0]['value']
        return gmail
    except KeyError:
        return False

def handle_redirect():
    flow = OAuth2WebServerFlow(client_id=settings.CLIENT_ID,client_secret=settings.CLIENT_SECRET, scope=settings.SCOPES,redirect_uri=settings.CALLBACK_URI)
    return flow.step1_get_authorize_url()

def handle_callback(request):
    code = request.GET.get('code', '')
    flow = OAuth2WebServerFlow(client_id=settings.CLIENT_ID,client_secret=settings.CLIENT_SECRET, scope=settings.SCOPES,redirect_uri=settings.CALLBACK_URI)
    credentials = flow.step2_exchange(code)
    gmail = get_gmail(credentials.access_token)
    try:
        user = User.objects.get(email=gmail)
    except User.DoesNotExist:
        user = User.objects.create_user(gmail, gmail, 'blank')
        user.save()
    request.session['token'] = credentials.access_token
    return gmail
        
def revoke_token(request):
    if 'token' in request.session:
        access_token = request.session['token']
        uri = 'https://accounts.google.com/o/oauth2/revoke?token=' + access_token
        urllib.urlopen(uri)
        request.session.flush()
        return None
    else:
        request.session.flush()
        return None
