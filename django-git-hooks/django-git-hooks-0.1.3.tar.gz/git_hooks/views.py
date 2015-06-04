# coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from git_hooks.gitpull import GitPuller


def git_pull(request):
    out = {}
    q = GitPuller(settings.BASE_DIR)
    # Запускаем процесс...
    q.run()
    try:
        return render(request, 'git_pull.html', out)
    except:
        return HttpResponse('OK')