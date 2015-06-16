from zope.component import adapter, queryUtility
from zope.annotation.interfaces import IAnnotations

from plone.registry.interfaces import IRegistry

from plone.cachepurging.hooks import KEY
from plone.cachepurging.interfaces import ICachePurgingSettings
from plone.cachepurging.utils import getPathsToPurge

from z3c.caching.interfaces import IPurgeEvent
from zope.globalrequest import getRequest

from ZPublisher.interfaces import IPubSuccess

from wildcard.cloudflare.interfaces import (
    ICloudflareSettings,
    HTTP, HTTPS, BOTH)

from wildcard.cloudflare.purger import CloudflarePurger


def getUrlsToPurge(path, domains=(), scheme=BOTH):
    if scheme == BOTH:
        schemes = ('http', 'https')
    elif scheme == HTTP:
        schemes = ('http',)
    elif scheme == HTTPS:
        schemes = ('https',)

    # remove virtual hosting stuff
    if '/_vh_' in path:
        path = '/' + path.split('/_vh_')[-1].split('/', 1)[-1]
    if 'VirtualHostRoot' in path:
        path = path.split('VirtualHostRoot')[-1]

    urls = []
    for scheme in schemes:
        for domain in domains:
            urls.append('%s://%s/%s' % (scheme, domain, path.lstrip('/')))
    return urls


@adapter(IPurgeEvent)
def queuePurge(event, force=False):
    """ so this is a little wonky here...
    We need to also purge here because plone.cachepurging will only update
    paths if caching proxies are defined. The deal here is that with
    cloudflare, we do not want to define caching proxies or we may not be """

    request = getRequest()
    if request is None:
        return

    annotations = IAnnotations(request, None)
    if annotations is None:
        return

    registry = queryUtility(IRegistry)
    if registry is None:
        return

    settings = registry.forInterface(ICachePurgingSettings, check=False)
    if not settings.enabled:
        return

    # so we're enabled, BUT we also need to NOT have proxies defined
    # in order to register here
    if bool(settings.cachingProxies) and not force:
        return

    paths = annotations.setdefault(KEY, set())
    paths.update(getPathsToPurge(event.object, request))


@adapter(IPubSuccess)
def purge(event):
    """
    Asynchronously send PURGE requests.
    this is mostly copied from plone.cachingpurgin
    """
    request = event.request

    annotations = IAnnotations(request, None)
    if annotations is None:
        return

    paths = annotations.get(KEY, None)
    if paths is None:
        return

    registry = queryUtility(IRegistry)
    if registry is None:
        return

    settings = registry.forInterface(ICachePurgingSettings, check=False)
    if not settings.enabled:
        return

    settings = registry.forInterface(ICloudflareSettings, check=False)
    if not settings.apiKey or not settings.zone_id:
        return

    key = settings.apiKey
    domains = settings.domains
    scheme = settings.scheme
    email = settings.email
    zone_id = settings.zone_id

    if paths:
        urls = []
        for path in paths:
            urls.extend(getUrlsToPurge(path, domains=domains, scheme=scheme))

        CloudflarePurger.purgeAsync(urls, zone_id, key, email)
