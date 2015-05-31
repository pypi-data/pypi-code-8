import json
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from websocket_channel.publisher import RedisPublisher


@csrf_exempt
def test1(request):
    RedisPublisher(request.POST['channel']).publish_message(request.POST['content'])
    return HttpResponse()


def websocket_request(request, recvmsg, subscriber):
    RedisPublisher("1111111111").publish_message("1111111111")