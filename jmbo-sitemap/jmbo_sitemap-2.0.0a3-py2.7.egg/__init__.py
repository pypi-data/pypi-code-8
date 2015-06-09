import types

from django.contrib.sitemaps import Sitemap, FlatPageSitemap
from django.utils.module_loading import import_by_path

from django.conf import settings


class BaseLinkSitemap(Sitemap):

    def __init__(self, request):
        self.request = request
        super(BaseLinkSitemap, self).__init__()

    def get_containers(self):
        raise NotImplementedError

    def items(self):
        added = []
        links = []
        for obj in self.get_containers():
            linkposition_set = getattr(obj, obj.__class__.__name__.lower() \
                + 'linkposition_set')
            for o in linkposition_set.select_related().all().order_by('position'):
                if o.condition_expression_result(self.request) \
                    and (o.link.id not in added):
                    # Skip over external links
                    if not o.link.get_absolute_url().startswith('http'):
                        links.append(o.link)
                        added.append(o.link.id)
        return links


class MainNavbarLinkSitemap(BaseLinkSitemap):
    priority = 1.0

    def get_containers(self):
        # Prevent circular import
        from foundry.models import Navbar
        return Navbar.permitted.filter(slug='main')


class MainMenuLinkSitemap(BaseLinkSitemap):
    priority = 1.0

    def get_containers(self):
        # Prevent circular import
        from foundry.models import Menu
        return Menu.permitted.filter(slug='main')


class SubNavbarsLinkSitemap(BaseLinkSitemap):
    priority = 0.75

    def get_containers(self):
        # Prevent circular import
        from foundry.models import Navbar
        return Navbar.permitted.all().exclude(slug='main')


class SubMenusLinkSitemap(BaseLinkSitemap):
    priority = 0.75

    def get_containers(self):
        # Prevent circular import
        from foundry.models import Menu
        return Menu.permitted.all().exclude(slug='main')

# Sitemaps can be set via settings
sitemaps = {}
try:
    sitemaps = settings.JMBO_SITEMAP['sitemaps']
except (AttributeError, KeyError):
    pass

if not sitemaps:
    sitemaps = {
        'flatpages': FlatPageSitemap,
    }

    if 'foundry' in settings.INSTALLED_APPS:
        sitemaps.update({
            'main-navbar': MainNavbarLinkSitemap,
            'main-menu': MainMenuLinkSitemap,
            'sub-navbars': SubNavbarsLinkSitemap,
            'sub-menus': SubMenusLinkSitemap,
        })

try:
    extra = settings.JMBO_SITEMAP['extra-sitemaps']
except (AttributeError, KeyError):
    pass
else:
    sitemaps.update(extra)

# Load classes if required
for k, v in sitemaps.items():
    if isinstance(v, types.StringType):
        sitemaps[k] = import_by_path(v)
