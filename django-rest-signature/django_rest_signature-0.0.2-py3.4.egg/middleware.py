from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import Signature
import jwt
from jwt.api import DecodeError
from django import http

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class SignatureMiddleware(object):
    def process_request(self, request):
        sb = 'http://learning-tech.com/'
        calladmin = '找管理员'
        response = http.HttpResponse(sb)
        response_admin= http.HttpResponse(calladmin)

        if request.method in ('POST','DELETE','PATCH',):
            print('Post')
        elif request.method == 'GET':
            print('get')

        encoded = request.META.get('HTTP_SIGNATURE',False)
        signature_id = request.GET.get('sid',False)
        unix_time = request.GET.get('t',False)

        if not(encoded or signature_id or unix_time):
            return response

        try:
            signature = get_object_or_404(Signature,pk=signature_id)

            try:
                decoded = jwt.decode(encoded, signature.key, algorithms=['HS256'])
            except DecodeError:
                return response

            except:
                return response_admin

            if str(decoded['sid']) == signature_id and str(decoded['t']) == unix_time:
                request.site = signature.site
            else:
                return response
        except Signature.DoesNotExist and http.Http404:
            return response
        except :
            return response_admin