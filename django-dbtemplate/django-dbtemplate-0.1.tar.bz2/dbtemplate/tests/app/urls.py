from django.conf.urls import url
from django.shortcuts import render_to_response


def test_view(request):
    return render_to_response('test.html', {'username': 'test'})


urlpatterns = [
    url(r'^$', test_view),
]
