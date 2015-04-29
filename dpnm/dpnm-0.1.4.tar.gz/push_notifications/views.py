# -*- coding: utf-8 -*-

# Third party
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Local
from .forms import PushDeviceForm
from .models import PushDevice


class UnRegisterDeviceView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        form = PushDeviceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            PushDevice.unregister_push_device(request.user,
                                              form.cleaned_data['token'])
            return Response({'unregistered': True})

        # Return back errors
        data = {
            'unregistered': False
        }
        data.update(form.errors)

        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class RegisterDeviceView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        form = PushDeviceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            PushDevice.register_push_device(request.user,
                                            form.cleaned_data['token'])
            return Response({'registered': True})

        # Return back errors
        data = {
            'registered': False
        }
        data.update(form.errors)

        return Response(data, status=status.HTTP_400_BAD_REQUEST)
