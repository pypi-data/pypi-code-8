__author__ = 'Sinisa'

import json
import inject
import requests
from sbg_cli.config import Config
from sbg_cli.command import Command
from sbg_cli.sbg_docker.docker_client.utils import get_session, login_as_user
from sbg_cli.sbg_docker.docker_client.client import Docker

class Appget(Command):

    cmd = 'app-get'
    args = '<url>'
    order = 6

    def __init__(self):
        self.docker = inject.instance(Docker)
        self.cfg = inject.instance(Config)

    def __call__(self, *args, **kwargs):
        url = kwargs.get('<url>')
        session_id = get_session(self.cfg.docker_registry)
        app_url = self.parse_url(url)
        app = self.get_app(app_url, session_id)
        if app:
            with open(self.app_name(url), 'w') as f:
                json.dump(app, f)
            print('App written in %s' % self.app_name(url))

    def parse_url(self, url):
        if 'sbgenomics.com' in url:
            proj = url.split('/u/')[-1]
            app_url = self.cfg.app_registry + '/' + proj
            app_url = app_url.replace('apps/#', '')
            if '?' in app_url:
                app_url = app_url.replace('?' + app_url.split('?')[-1], '')
            return app_url
        else:
            return url

    def get_app(self, url, session):
        headers = {'session-id': session, 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['message']
        else:
            print('App not found')
            return None

    def app_name(self, url):
        if 'sbgenomics.com' in url:
            slug = url.split('/u/')[-1].replace('apps/#', '')
            if '?' in slug:
                slug = slug.replace('?' + slug.split('?')[-1], '')
            slug = slug.split('/')
            if slug[-1] != '':
                name = slug[-1]
            else:
                name = slug[-2]
            return '%s.json' % name
        else:
            return '%s.json' % url.split('/')[-1]
