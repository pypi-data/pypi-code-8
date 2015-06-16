from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView
from plone.app.registry.browser import controlpanel
from wildcard.cloudflare.interfaces import ICloudflareSettings
from zope.component import getMultiAdapter
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from wildcard.cloudflare import getUrlsToPurge, queuePurge
from wildcard.cloudflare.purger import CloudflarePurger
import requests


class CloudflareSettingsEditForm(controlpanel.RegistryEditForm):

    schema = ICloudflareSettings
    label = u"Cloudflare Settings"
    description = u"""You must also configure Plone's cache purging"""


class CloudflareSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    index = ViewPageTemplateFile('controlpanel_layout.pt')

    form = CloudflareSettingsEditForm


class FakeEvent(object):

    def __init__(self, object):
        self.object = object


class Purge(BrowserView):

    def purge(self, paths):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(ICloudflareSettings, check=False)
        key = settings.apiKey
        domains = settings.domains
        scheme = settings.scheme
        email = settings.email
        zone_id = settings.zone_id

        urls = []
        for path in paths:
            urls.extend(getUrlsToPurge(path, domains=domains, scheme=scheme))

        resp = CloudflarePurger.purgeSync(urls, zone_id, key, email)

        return urls, resp.json()['success']

    def __call__(self):
        self.success = False
        authenticator = getMultiAdapter((self.context, self.request),
                                        name=u"authenticator")
        if authenticator.verify():
            self.paths = self.request.get('paths', '').splitlines()
            if self.paths:
                self.purged, self.success = self.purge(self.paths)
            else:
                self.purged = []
        return self.index()


class PurgePage(BrowserView):

    def __call__(self):
        queuePurge(FakeEvent(self.context))
        self.request.response.redirect(self.context.absolute_url() + '/view')


class ListZones(BrowserView):
    def __call__(self):
        req = self.request
        return requests.get(
            'https://api.cloudflare.com/client/v4/zones',
            headers={
                'X-Auth-Email': req.get('email'),
                "X-Auth-Key": req.get('key')
            }
        ).content
