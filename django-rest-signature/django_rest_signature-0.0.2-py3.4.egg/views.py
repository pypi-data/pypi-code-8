from rest_framework.generics import *
from .serializers import *

class SiteList(ListCreateAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer


class SignatureList(ListCreateAPIView):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer
    response_serializer = SignatureResponseSerializer

    def get(self, request, *args, **kwargs):
        self.serializer_class = self.response_serializer
        return super(SignatureList, self).get(request,*args,**kwargs)

# jwt.encode({'sid': 1 , 't':123456}, '717e2534055268ab5a980009336c2ec6552df3e9', algorithm='HS256')
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0IjoxMjM0NTYsInNpZCI6MX0.7wTdQ5GZ_K2Vdg8YVR6XFitmN3VUISD_LbwToFvRAUo
# 717e2534055268ab5a980009336c2ec6552df3e9