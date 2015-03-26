from zope.interface import implements
from plone.i18n.interfaces import ILanguageUtility, INegotiateLanguage
from zope.component import queryUtility
from plone.i18n.locales.interfaces import ICountryAvailability
from plone.i18n.locales.interfaces import IContentLanguageAvailability
from plone.i18n.locales.interfaces import ICcTLDInformation
from Products.SiteAccess.VirtualHostMonster import VirtualHostMonster
from ZODB.POSException import ConflictError
from AccessControl import ClassSecurityInfo
from zope.component.hooks import getSite
from zope.component import getMultiAdapter
from zope.component import getUtility
from Products.CMFCore.interfaces import IDublinCore
from zope.component.hooks import getSite

from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import ILanguageSchema


class LanguageBinding:
    """Helper which holding language infos in request."""
    security = ClassSecurityInfo()
    __allow_access_to_unprotected_subobjects__ = 1

    DEFAULT_LANGUAGE = None
    LANGUAGE = None
    LANGUAGE_LIST = []

    security.declarePublic('getLanguageBindings')

    def getLanguageBindings(self):
        """Returns the bound languages.

        (language, default_language, languages_list)
        """
        return (self.LANGUAGE, self.DEFAULT_LANGUAGE, self.LANGUAGE_LIST)


def setLanguageBinding(request):
    binding = request.get('LANGUAGE_TOOL', None)
    settings = getMultiAdapter((getSite(), request), INegotiateLanguage)

    if not isinstance(binding, LanguageBinding):
        # Create new binding instance
        binding = LanguageBinding()
        # Set bindings instance to request here to avoid infinite recursion
        request['LANGUAGE_TOOL'] = binding
    # Bind languages
    binding.LANGUAGE = lang = settings.language
    binding.DEFAULT_LANGUAGE = settings.default_language
    binding.LANGUAGE_LIST = list(settings.language_list)
    # Set LANGUAGE to request
    request['LANGUAGE'] = lang
    return lang


def onRequest(object, event):
    """Set Language headers in the request.
    """
    request = event.request

    return setLanguageBinding(request)


class LanguageUtility(object):
    implements(ILanguageUtility)

    # resources that must not use language specific URLs
    exclude_paths = frozenset((
        'portal_css',
        'portal_javascripts',
        'portal_kss',
        'portal_factory'
    ))

    exclude_exts = frozenset((
        'css',
        'js',
        'kss',
        'xml',
        'gif',
        'jpg',
        'png',
        'jpeg'
    ))

    @property
    def settings(self):
        registry = getUtility(IRegistry)
        return registry.forInterface(
            ILanguageSchema,
            prefix='plone',
        )

    # BBB propouses
    @property
    def use_combined_language_codes(self):
        return self.settings.use_combined_language_codes

    @property
    def supported_langs(self):
        return self.settings.available_languages

    @property
    def showFlags(self):
        return self.settings.display_flags

    def getSupportedLanguages(self):
        """Returns a list of supported language codes."""
        return self.settings.available_languages

    def listSupportedLanguages(self):
        """Returns a list of supported language names."""
        r = []
        available = self.getAvailableLanguages()
        for i in self.supported_langs:
            if available.get(i):
                r.append((i, available[i][u'name']))
        return r

    def getAvailableLanguages(self):
        """Returns the dictionary of available languages.
        """
        util = queryUtility(IContentLanguageAvailability)
        if self.settings.use_combined_language_codes:
            languages = util.getLanguages(combined=True)
        else:
            languages = util.getLanguages()
        return languages

    def getCcTLDInformation(self):
        util = queryUtility(ICcTLDInformation)
        return util.getTLDs()

    def listAvailableLanguages(self):
        """Returns sorted list of available languages (code, name)."""
        util = queryUtility(IContentLanguageAvailability)
        if self.use_combined_language_codes:
            languages = util.getLanguageListing(combined=True)
        else:
            languages = util.getLanguageListing()
        languages.sort(lambda x, y: cmp(x[1], y[1]))
        return languages

    def listAvailableLanguageInformation(self):
        """Returns list of available languages."""
        langs = self.getAvailableLanguageInformation()
        new_langs = []
        for lang in langs:
            # add language-code to dict
            langs[lang][u'code'] = lang
            # flatten outer dict to list to make it sortable
            new_langs.append(langs[lang])
        new_langs.sort(lambda x, y: cmp(x.get(u'native', x.get(u'name')), y.get(u'native', y.get(u'name'))))
        return new_langs

    def getAvailableLanguageInformation(self):
        """Returns the dictionary of available languages."""
        util = queryUtility(IContentLanguageAvailability)
        if self.use_combined_language_codes:
            languages = util.getLanguages(combined=True)
        else:
            languages = util.getLanguages()

        for lang in languages:
            languages[lang]['code'] = lang
            if lang in self.supported_langs:
                languages[lang]['selected'] = True
            else:
                languages[lang]['selected'] = False
        return languages

    def getDefaultLanguage(self):
        """Returns the default language. D"""
        return self.settings.default_language

    def setDefaultLanguage(self, langCode):
        """Sets the default language. D"""
        if langCode not in self.settings.available_languages:
            # If its not in supported langs
            if len(self.settings.available_languages) > 0:
                self.settings.default_language = self.settings.available_languages[0]
            return
        self.settings.default_language = langCode

    def getNameForLanguageCode(self, langCode):
        """Returns the name for a language code."""
        info = self.getAvailableLanguageInformation().get(langCode, None)
        if info is not None:
            return info.get(u'name', None)
        return None

    def getFlagForLanguageCode(self, langCode):
        """Returns the name of the flag for a language code."""
        info = self.getAvailableLanguageInformation().get(langCode, None)
        if info is not None:
            return info.get(u'flag', None)
        return None

    def addSupportedLanguage(self, langCode):
        """Registers a language code as supported."""
        alist = self.settings.available_languages[:]
        if (langCode in self.getAvailableLanguages().keys()) and not langCode in alist:
            alist.append(langCode)
            self.settings.available_languages = alist

    def removeSupportedLanguages(self, langCodes):
        """Unregisters language codes from supported."""
        alist = self.settings.available_languages[:]
        for i in langCodes:
            alist.remove(i)
        self.settings.available_languages = alist

    def setLanguageCookie(self, lang=None, request=None, noredir=None):
        """Sets a cookie for overriding language negotiation."""
        res = None
        if lang and lang in self.getSupportedLanguages():
            if lang != self.getLanguageCookie(request):
                request.RESPONSE.setCookie('I18N_LANGUAGE', lang, path='/')
            res = lang
        return res

    def getLanguageCookie(self, request):
        """Gets the preferred cookie language."""
        if not request:
            return None
        langCookie = request.cookies.get('I18N_LANGUAGE')
        if langCookie in self.getSupportedLanguages():
            return langCookie
        return None

    def getPreferredLanguage(self, request):
        """Gets the preferred site language."""
        l = self.getLanguageBindings(request)
        if l[0]:
            if not self.settings.use_combined_language_codes:
                return l[0].split('-')[0]
            else:
                return l[0]
            return l[0]
        # this is the default language
        return l[1]

    def getPathLanguage(self, request):
        """Checks if a language is part of the current path."""
        if not request:
            return []
        items = request.get('TraversalRequestNameStack')
        # XXX Why this try/except?
        try:
            for item in items:
                if item in self.getSupportedLanguages():
                    return item
        except (ConflictError, KeyboardInterrupt):
            raise
        except:
            pass
        return None

    def getContentLanguage(self, request):
        """Checks the language of the current content if not folderish."""
        if not request:
            return []
        try: # This will actually work nicely with browserdefault as we get attribute error...
            contentpath = request.path[:]

            # Now check if we need to exclude from using language specific path
            # See https://dev.plone.org/ticket/11263
            if (bool([1 for p in self.exclude_paths if p in contentpath]) or
                bool([1 for p in self.exclude_exts if contentpath[0].endswith(p)])
                ):
                return None

            obj = getSite()
            traversed = []
            while contentpath:
                name = contentpath.pop()
                if name[0] in '@+':
                    break
                next = obj.unrestrictedTraverse(name, None)
                if next is None:
                    break
                if isinstance(next, VirtualHostMonster):
                    # next element is the VH subpath
                    contentpath.pop()
                    continue
                obj = next
                traversed.append(obj)
            for obj in reversed(traversed):
                if IDublinCore.providedBy(obj):
                    lang = obj.Language()
                    if not lang:
                        continue
                    if lang in self.getSupportedLanguages():
                        return lang
                    else:
                        return None
        except ConflictError:
            raise
        except:
            pass
        return None

    def getCcTLDLanguages(self, request):
        if not request:
            return None
        if "HTTP_HOST" not in request:
            return None
        host = request["HTTP_HOST"].split(":")[0].lower()
        tld = host.split(".")[-1]
        wanted = self.getCcTLDInformation().get(tld, [])
        allowed = self.getSupportedLanguages()
        return [lang for lang in wanted if lang in allowed]

    def getSubdomainLanguages(self, request):
        if not request:
            return None
        if "HTTP_HOST" not in request:
            return None
        host = request["HTTP_HOST"].split(":")[0].lower()
        tld = host.split(".")[0]
        wanted = self.getCcTLDInformation().get(tld, [])
        allowed = self.getSupportedLanguages()
        return [lang for lang in wanted if lang in allowed]

    def getRequestLanguages(self, request):
        """Parses the request and return language list."""

        if not request:
            return None

        # Get browser accept languages
        browser_pref_langs = request.get('HTTP_ACCEPT_LANGUAGE', '')
        browser_pref_langs = browser_pref_langs.split(',')

        i = 0
        langs = []
        length = len(browser_pref_langs)

        # Parse quality strings and build a tuple like
        # ((float(quality), lang), (float(quality), lang))
        # which is sorted afterwards
        # If no quality string is given then the list order
        # is used as quality indicator
        for lang in browser_pref_langs:
            lang = lang.strip().lower().replace('_', '-')
            if lang:
                l = lang.split(';', 2)
                quality = []

                if len(l) == 2:
                    try:
                        q = l[1]
                        if q.startswith('q='):
                            q = q.split('=', 2)[1]
                            quality = float(q)
                    except:
                        pass

                if quality == []:
                    quality = float(length-i)

                language = l[0]
                if (self.use_combined_language_codes and
                        language in self.getSupportedLanguages()):
                    # If allowed add the language
                    langs.append((quality, language))
                else:
                    # if we only use simply language codes, we should recognize
                    # combined codes as their base code. So 'de-de' is treated
                    # as 'de'.
                    baselanguage = language.split('-')[0]
                    if baselanguage in self.getSupportedLanguages():
                        langs.append((quality, baselanguage))
                i = i + 1

        # Sort and reverse it
        langs.sort()
        langs.reverse()

        # Filter quality string
        langs = map(lambda x: x[1], langs)

        return langs

    def getLanguageBindings(self, request):
        """Returns the bound languages.

        (language, default_language, languages_list)
        """
        if not request:
            # Can't do anything
            return (None, self.getDefaultLanguage(), [])
        binding = request.get('LANGUAGE_TOOL', None)
        if not isinstance(binding, LanguageBinding):
            # Not bound -> bind
            setLanguageBinding(request)
            binding = request.get('LANGUAGE_TOOL')
        return binding.getLanguageBindings()

    def getAvailableCountries(self):
        """Returns the dictionary of available countries."""
        util = queryUtility(ICountryAvailability)
        return util.getCountries()

    def listAvailableCountries(self):
        """Returns the sorted list of available countries (code, name)."""
        util = queryUtility(ICountryAvailability)
        countries = util.getCountryListing()
        countries.sort(lambda x, y: cmp(x[1], y[1]))
        return countries

    def getNameForCountryCode(self, countryCode):
        """Returns the name for a country code."""
        return self.getAvailableCountries().get(countryCode, countryCode)

    def isAnonymousUser(self):
        from AccessControl import getSecurityManager
        user = getSecurityManager().getUser()
        return not user.has_role('Authenticated')

    def showSelector(self):
        """Returns True if the selector viewlet should be shown."""
        if self.settings.always_show_selector:
            return True
        if (self.settings.use_cookie_negotiation and
            not (self.settings.authenticated_users_only and self.isAnonymousUser())):
            return True
        return False

try:
    from Products.PlacelessTranslationService.Negotiator import registerLangPrefsMethod
    _hasPTS = 1
except ImportError:
    _hasPTS = 0


class PrefsForPTS:
    """A preference to hook into PTS."""
    def __init__(self, context):
        self._env = context
        self.languages = []
        binding = context.get('LANGUAGE_TOOL')
        if not isinstance(binding, LanguageBinding):
            return None
        self.pref = binding.getLanguageBindings()
        self.languages = [self.pref[0]] + self.pref[2] + [self.pref[1]]
        return None

    def getPreferredLanguages(self):
        """Returns the list of the bound languages."""
        return self.languages


if _hasPTS:
    registerLangPrefsMethod({'klass':PrefsForPTS, 'priority':100 })
