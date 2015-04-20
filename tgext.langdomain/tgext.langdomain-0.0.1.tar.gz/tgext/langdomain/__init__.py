import tg

try:
    from tg.i18n import set_request_lang
    old_tg = False
except ImportError:
    old_tg = True

from .lang import LanguageDetector

import logging
log = logging.getLogger('tgext.langdomain')


def plugme(configurator, options=None):
    if options is None:
        options = {}

    log.info('Setting up tgext.langdomain extension...')
    conf = {
        'param': options.get('param', False),
        'tldmap': options.get('tld', {}),
        'subdomainmap': options.get('subdomain', {}),
    }

    if not conf['param'] and not conf['tldmap'] and not conf['subdomainmap']:
        # All options are empty
        log.error("You didn't provide any behaviour for tgext.langdomain, check documentation...")

    configurator['tgext.langdomain'] = conf

    if old_tg:
        configurator.register_hook('controller_wrapper', LangDomainControllerWrapper)
    else:
        configurator.register_wrapper(LangDomainApplicationWrapper)

    # This is required to be compatible with the
    # tgext.pluggable interface
    return dict(appid='tgext.langdomain')


class LangDomainApplicationWrapper(object):
    def __init__(self, handler, config):
        self.next_handler = handler

        conf = config['tgext.langdomain']
        self._detector = LanguageDetector(conf['tldmap'], conf['subdomainmap'], conf['param'],
                                          config.get('lang_session_key', 'tg_lang'))

    def __call__(self, controller, environ, context):
        req = context.request
        session = context.session

        def continue_callback():
            return self.next_handler(controller, environ, context)

        return self._detector.process(req, session, continue_callback)


class LangDomainControllerWrapper(object):
    def __init__(self, next_handler):
        self.next_handler = next_handler

        from tg import config as tg_config
        conf = tg_config['tgext.langdomain']
        self._detector = LanguageDetector(conf['tldmap'], conf['subdomainmap'], conf['param'],
                                          tg_config.get('lang_session_key', 'tg_lang'))

    def __call__(self, *args, **kw):
        req = tg.request._current_obj()
        session = tg.session._current_obj()

        def continue_callback():
            return self.next_handler(*args, **kw)

        return self._detector.process(req, session, continue_callback)
