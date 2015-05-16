# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import json, current_app, url_for, _app_ctx_stack


class BowerCDN(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('BOWERCDN_BOWER_JSON', 'bower.json')
        with app.app_context():
            with open(app.config['BOWERCDN_BOWER_JSON'], 'r') as fp:
                d = json.load(fp)
            ctx = _app_ctx_stack.top
            ctx.bowercdn_components = d['dependencies']
            app.logger.debug('bowercdn: loaded %s bower components' % (len(d['dependencies'],)))
        app.jinja_env.globals['bower_or_cdn'] = bower_or_cdn


def bower_or_cdn(local, urlpattern):
    if current_app.debug or current_app.testing:
        return url_for('bower.static', filename=local)
    else:
        component = local.split('/')[0]
        ctx = _app_ctx_stack.top
        components = getattr(ctx, 'bowercdn_components', None)
        version = components[component]
        return urlpattern.format(**{'version': version})
