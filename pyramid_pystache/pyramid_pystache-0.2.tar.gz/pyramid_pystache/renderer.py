import os
import re
import threading

import pkg_resources

from zope.interface import implementer

from pyramid.asset import asset_spec_from_abspath
from pyramid.path import (
    caller_package,
    package_path
    )

from pyramid_pystache.interfaces import (
    IMustacheLookup,
    ITemplateRenderer
    )


@implementer(IMustacheLookup)
class MustacheRendererLookup(object):
    spec_re = re.compile(
        r'(?P<asset>[\w_.:/-]+)'
        r'(\.(?P<ext>.*))'
        )

    def __init__(self, impl, registry):
        self.impl = impl
        self.registry = registry
        self.lock = threading.Lock()

    def get_spec(self, name, package):
        if not package:
            # if there's no package, we can't do any conversion
            return name

        spec = name
        isabspath = os.path.isabs(name)
        colon_in_name = ':' in name
        isabsspec = colon_in_name and (not isabspath)
        isrelspec = (not isabsspec) and (not isabspath)

        # if it's already an absolute spec, we don't need to do anything,
        # but if it's a relative spec or an absolute path, we need to try
        # to convert it to an absolute spec

        if isrelspec:
            # convert relative asset spec to absolute asset spec
            pp = package_path(package)
            spec = os.path.join(pp, spec)
            spec = asset_spec_from_abspath(spec, package)

        elif isabspath:
            # convert absolute path to absolute asset spec
            spec = asset_spec_from_abspath(spec, package)

        return spec

    def _crack_spec(self, spec):
        asset, ext = self.spec_re.match(spec).group(
            'asset', 'ext'
        )
        return asset, ext

    def __call__(self, info):
        spec = self.get_spec(info.name, info.package)
        registry = info.registry

        if os.path.isabs(spec):
            # 'spec' is an absolute filename
            if not os.path.exists(spec):
                raise ValueError('Missing template file: %s' % spec)
            renderer = registry.queryUtility(ITemplateRenderer, name=spec)
            if renderer is None:
                renderer = self.impl(spec, self)
                # cache the template
                with self.lock:
                    registry.registerUtility(renderer,
                                             ITemplateRenderer, name=spec)
        else:
            # spec is a package:relpath asset spec
            renderer = registry.queryUtility(ITemplateRenderer, name=spec)
            if renderer is None:
                asset, ext = self._crack_spec(spec)
                cracked_spec = '%s.%s' % (asset, ext)
                try:
                    package_name, filename = cracked_spec.split(':', 1)
                except ValueError: # pragma: no cover
                    # somehow we were passed a relative pathname; this
                    # should die
                    package_name = caller_package(4).__name__
                    filename = spec_without_macro
                abspath = pkg_resources.resource_filename(package_name,
                                                          filename)
                if not pkg_resources.resource_exists(package_name, filename):
                    raise ValueError(
                        'Missing template asset: %s (%s)' % (
                            cracked_spec, abspath)
                        )
                renderer = self.impl(abspath, self)
                settings = info.settings
                if not settings.get('reload_assets'):
                    # cache the template
                    with self.lock:
                        registry.registerUtility(renderer, ITemplateRenderer,
                                                 name=spec)

        return renderer

registry_lock = threading.Lock()

def template_renderer_factory(info, impl, lock=registry_lock):
    registry = info.registry
    lookup = registry.queryUtility(IMustacheLookup, name=info.type)
    if lookup is None:
        lookup = MustacheRendererLookup(impl, registry)
        with lock:
            registry.registerUtility(lookup, IMustacheLookup, name=info.type)
    return lookup(info)

