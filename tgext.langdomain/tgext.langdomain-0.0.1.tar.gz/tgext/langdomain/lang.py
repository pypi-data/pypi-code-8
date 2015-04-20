try:
    from tg.i18n import set_request_lang
except ImportError:
    from tg.i18n import set_temporary_lang as set_request_lang

import logging
log = logging.getLogger('tgext.langdomain')


class LanguageDetector(object):
    def __init__(self, tldmap, subdomainmap, param, session_key):
        self._tldmap = tldmap
        self._subdomainmap = subdomainmap
        self._param = param
        self._session_key = session_key

        if self._param is True:
            self._param = 'lang'

    def process(self, req, session, continue_request):
        domain = req.domain
        if not domain:
            return continue_request()

        if session is not None:
            if self._session_key in session:
                # User has a forced language, skip...
                return continue_request()

        try:
            domain_name, tld = domain.rsplit('.', 1)
        except ValueError:
            # does not have a tld or subdomain...
            return continue_request()

        try:
            subdomain, domain_name = domain_name.split('.', 1)
        except ValueError:
            subdomain = None

        if self._tldmap:
            lang = self._tldmap.get(tld)
            if lang is not None:
                log.debug('TLD Forcing language %s', lang)
                set_request_lang(lang)

        if self._subdomainmap:
            lang = self._subdomainmap.get(subdomain)
            if lang is not None:
                log.debug('SubDomain Forcing language %s', lang)
                set_request_lang(lang)

        if self._param:
            lang = req.params.get(self._param)
            if lang is not None:
                log.debug('Param Forcing language %s', lang)
                set_request_lang(lang)

        return continue_request()


