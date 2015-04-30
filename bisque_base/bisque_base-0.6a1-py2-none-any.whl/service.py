###############################################################################
##  Bisquik                                                                  ##
##  Center for Bio-Image Informatics                                         ##
##  University of California at Santa Barbara                                ##
## ------------------------------------------------------------------------- ##
##                                                                           ##
##     Copyright (c) 2007,2008                                               ##
##      by the Regents of the University of California                       ##
##                            All rights reserved                            ##
##                                                                           ##
## Redistribution and use in source and binary forms, with or without        ##
## modification, are permitted provided that the following conditions are    ##
## met:                                                                      ##
##                                                                           ##
##     1. Redistributions of source code must retain the above copyright     ##
##        notice, this list of conditions, and the following disclaimer.     ##
##                                                                           ##
##     2. Redistributions in binary form must reproduce the above copyright  ##
##        notice, this list of conditions, and the following disclaimer in   ##
##        the documentation and/or other materials provided with the         ##
##        distribution.                                                      ##
##                                                                           ##
##     3. All advertising materials mentioning features or use of this       ##
##        software must display the following acknowledgement: This product  ##
##        includes software developed by the Center for Bio-Image Informatics##
##        University of California at Santa Barbara, and its contributors.   ##
##                                                                           ##
##     4. Neither the name of the University nor the names of its            ##
##        contributors may be used to endorse or promote products derived    ##
##        from this software without specific prior written permission.      ##
##                                                                           ##
## THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS "AS IS" AND ANY ##
## EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED ##
## WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, ARE   ##
## DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR  ##
## ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL    ##
## DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS   ##
## OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)     ##
## HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,       ##
## STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN  ##
## ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE           ##
## POSSIBILITY OF SUCH DAMAGE.                                               ##
##                                                                           ##
###############################################################################
"""
SYNOPSIS
========


DESCRIPTION
===========

"""

import os
import inspect
import logging
import posixpath
import pkg_resources

try:
    from lxml import etree as ET
    from lxml.etree import _Element as ETElement
except ImportError:
    import xml.etree.ElementTree as ET
    from xml.etree.ElementTree import Element  as ETElement

from urllib import urlencode
import urlparse
#from tg import config, expose, request
#from bq.core.lib.base import BaseController
from bq.auth import config_auth


log = logging.getLogger ("bq.service")

__all__=["ServiceController", "find_service", "load_services", "get_all_services" ]


bisque_config = None

class ServiceDirectory(object):
    """Specialized dict of service_type -> to bq.service"""

    class Entry(object): #pylint: disable=R0903
        """SeviceDirectory.Entry  maintains information on eash service_type"""
        def __init__ (self):
            self.module = None
            self.name  = None
            self.controller = None
            self.instances = []

    def __init__(self):
        # Services is a hash of service_type : Entry
        self.services = {}
        self.config = None

    def __iter__(self):
        for e in self.services:
            for i in e.instances:
                yield i
    def _get_entry (self, service_type):
        return self.services.setdefault (service_type, ServiceDirectory.Entry())

    def register_service (self, name, service, service_type = None):
        """Register a new service (type)"""
        if service_type is None:
            service_type = name
        e = self._get_entry (service_type)
        e.name = name
        e.module = service
        #e.controller = service.__controller__

    def register_instance (self, service):
        """Register a running instance of a service"""
        e = self._get_entry (service.service_type)
        e.instances.append(service)

    def find_class (self, service_type):
        """Find the service class by service type"""
        e = self._get_entry (service_type)
        return  e.controller

    def has_service(self, service_type = None):
        """Check the existance of a service type and/or service url"""
        return service_type in self.services

    def find_service (self, service_type, request = None):
        """Return the service instance of service type"""
        entry = self.services.get (service_type, None)
        if request is None:
            #from pyramid.request import Request
            from pyramid.threadlocal import get_current_registry, get_current_request
            from pyramid.request import Request

            request = Request.blank('/%s'%service_type)
            oldrequest = get_current_request()
            if oldrequest:
                request.session = oldrequest.session

            #request.registry =  get_current_registry()
            request.registry = self.config.registry #bisque_config.registry
            log.info ("REGIUS %s", request.registry)

        if entry is None:
            log.error ('ENTRY NOT FOUND %s' , self.services)

        service = entry.module.initialize(request)
        return service


    def get_services (self, service_type=None):
        """Return all services"""
        if service_type is None:
            return self.services
        return self.services.get (service_type, ServiceDirectory.Entry())


service_registry  = ServiceDirectory()


def load_services ( wanted = None):
    for x in pkg_resources.iter_entry_points ("bisque.services"):
        #log.debug ('found service: ' + str(x))
        try:
            log.debug ('loading %s' % str(x))
            service = x.load()
            log.debug ('found %s' % (service.__file__))
            service_registry.register_service (x.name, service)

        except Exception:
            log.exception ("Failed to load bisque service: %s skipping" % x.name)
        #except Exception, e:
        #    log.exception ("Couldn't load %s -- skipping" % (x.name))



def mount_services (config):
    settings =config.get_settings()
    enabled = settings.get ('bisque.services_enabled')
    disabled = settings.get ('bisque.services_disabled')
    service_registry.config = config
    for x in pkg_resources.iter_entry_points ("bisque.services"):
        try:
            ty = x.name
            if (not enabled or  ty in enabled) and ty not in disabled:
                log.debug ('loading %s' % str(x))
                service = x.load()
                service_registry.register_service (x.name, service)
                config.include (service, route_prefix = x.name)

                #  Make a static route for each service that needs it (maybe move to internal config)
                if settings.get('bisque.static_files') and hasattr(service, 'get_static_dirs'):
                    dirlist = service.get_static_dirs()
                    for pk, drt in dirlist:
                        log.info ("Adding static %s -> %s", x.name, drt)
                        config.add_static_view("%s" %x.name, drt, cache_max_age=3600)
            else:
                log.debug ("Skipping %s", ty)

        except Exception:
            log.exception ("Failed to load bisque service: %s skipping" % x.name)
            print "PROB"



def urljoin(base,url, **kw):
    join = urlparse.urljoin(base,url)
    url = urlparse.urlparse(join)
    path = posixpath.normpath(url[2])
    #query = urlparse.parse_qs(url[4])
    if url[4]:
        query = dict ([ q.split('=')  for q in url[4].split('&')])
    else:
        query = {}
    query.update ( urlencode(kw) )
    return urlparse.urlunparse(
        (url.scheme,url.netloc,path,url.params,query,url.fragment)
        )

class ServiceMixin(object):

    def __init__(self, uri):
        """Initialize the Bisque Controller class

        @param url: The base url for this controller
        """
        self.service_type = self.__class__.service_type
        if uri[-1] != '/':
            uri += '/'
        self.fulluri = uri
        #self.baseuri = uri
        self.baseuri = urlparse.urlparse(uri).path
        log.debug ("creating %s at %s" % (self.service_type, self.baseuri))
        urituple = urlparse.urlparse(uri)
        self.host, self.path = urituple.netloc , urituple.path

    def start (self):
        """start the controller.. Used for common operations
        such as background threads and other assorted operations
        before the first request is delivered
        """
        pass


    def get_uri(self):
        try:
            if hasattr(self, 'request'):
                host_url = self.request.host_url
            #log.debug ("REQUEST %s" , host_url)
        except TypeError:
            #log.warn ("TYPEERROR on request")
            host_url = ''
        return urlparse.urljoin (host_url, self.baseuri)

    uri = property (get_uri)
    url = property (get_uri)


    def makeurl (self, path = "", **kw):
        """Construct a url with a local path and arguments passed
        as named parameters
        i.e.
        self.makeurl ("/view", option='deep', resource="http://aa.com" )
        http://baseuri/view?option=deep&resource=http%2f%fc%fcaa.com
        """

        return self.request.current_route_url(path, **kw)
        #return urljoin (self.baseuri, path, **kw)
    def __str__(self):
        return self.localuri

    def get_localurl(self):
        return self.path
    localuri = property(get_localurl)

    def get_static (self):
        pass
    staticuri = property (get_static)


    def servicelist(self):
        entries = []
        for name, m in inspect.getmembers (self.__class__, inspect.ismethod):
            if  hasattr(m, 'decoration'):
                args, varargs, kw, df = inspect.getargspec(m)
                tagsargs = [ dict(name='argument', value=arg) for arg in args if arg!='self']
                entries.append ( { 'name' : name,
                                   'type'  : 'service_entry',
                                   'tag' : tagsargs,
                                  })
        return { 'resource' : { 'tag' : entries, 'type': 'service' }}


class ServiceController(ServiceMixin):
    def __init__(self, uri):
        ServiceMixin.__init__(self, uri)


def service_service (request):
    from pyramid.response import Response
    resource = ET.Element ('resource')
    for ty, e in  service_registry.get_services().items():
        service = ET.SubElement (resource, 'tag',
                                    name='service',
                                    type=ty,
                                    value="/%s/" % e.name)
    return Response(ET.tostring (resource), content_type='text/xml')



from pyramid.config import Configurator
from pyramid.settings import asbool
from pyramid.compat import string_types, text_type
import pyramid.httpexceptions as exc


#####################################################################
#  XML renderer
#
def xml_renderer_factory (info):
    """ allows views to say renderer='xml' and return a
    an string or elementtree
    """
    def xml_render(value, system):
        request = system.get ('request')
        if request is not None:
            response = request.response
            ct = response.content_type
            if ct == response.default_content_type:
                response.content_type = 'text/xml'
        if isinstance (value, ETElement):
            value =  ET.tostring(value)
        elif not isinstance(value, string_types):
            value = str(value)
        return value
    return xml_render


class XmlRendererFactory(object):
    def __init__(self, info):
        self._info = info
    def __call__(self, value, system):
        xml =  XmlRenderer ()
        return xml (value, system)

##################################################

class ContentTypePredicate(object):
    def __init__(self, val, config):
        self.val = val

    def text(self):
        return 'content type = %s' % self.val
    phash = text

    def __call__(self, context, request):
        types =  request.content_type or  'text/html'
        log.debug ("predicate %s in %s", self.val, types)
        return self.val in types.split (',')



###################################################
# Pyramid main entry point
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    from pyramid.paster import setup_logging
    if os.path.exists ('config/site.cfg'):
        setup_logging('config/site.cfg')

    log.info ("BISQUE STARTUP")



    if asbool(settings.get ('bisque.has_database', True)):
        from sqlalchemy import engine_from_config
        from bq.core.model import DBSession, DeclarativeBase
        engine = engine_from_config(settings, 'sqlalchemy.')
        settings['bisque.sqlengine'] = engine
        DBSession.configure (bind=engine)
        DeclarativeBase.metadata.bind = engine

    enabled = settings.get('bisque.services_enabled', None)
    disabled = settings.get('bisque.services_disabled', None)
    enabled  = enabled and [ x.strip() for x in enabled.split(',') ] or []
    disabled = disabled and [ x.strip() for x in disabled.split(',') ] or []

    settings['bisque.services_enabled'] = enabled
    settings['bisque.services_disabled'] = disabled

    global bisque_config
    bisque_config = config = Configurator(settings=settings, root_factory = config_auth.BisqueRoot)
    log.info ("CONFIG REGISTRY %s", config.registry )

    # Private XML renderer
    config.add_renderer('xml', xml_renderer_factory)
    #config.add_view_predicate('content_type', ContentTypePredicate)

    # Authentication & Authorization
    config.include (config_auth.config_auth)

    if asbool(settings.get ('bisque.celery', False)):
        log.debug ("CELERY CONFIG")
        from bq.celery.app import config_celery
        config_celery (config)

    # Template engines
    config.include('pyramid_beaker')
    config.include('pyramid_genshi')
    #config.include('pyramid_chameleon')
    #config.include('pyramid_chameleon_genshi')

    # Bundle of static webassets
    if asbool(settings.get ('bisque.static_files')):
        from bq.setup.bundles import all_css, pre_js, all_js
        config.include ("pyramid_webassets")
        log.info ("ADDING Webassets")
        config.add_webasset ('all_css', all_css)
        config.add_webasset ('pre_js', pre_js)
        config.add_webasset ('all_js', all_js)

    # The ordering of routes is important
    # The top level "service listing" service
    config.add_route('service_service', '/services')
    config.add_view(service_service, route_name='service_service')
    # Now mount sub-controllers routes
    mount_services (config)
    # Finally add shortcut route if none other match

    if service_registry.has_service ('data_service'):
        config.add_route('resource_shortcut', '/{uniq:00-\w+}*path')

    if service_registry.has_service ('web'):
        config.add_route('web_shortcut', '/')
        config.add_static_view (name='', path=os.path.abspath('./public'))

    if service_registry.has_service('engine_service'):
        config.add_route ('engine_shortcut', '/')
        def redirector(request):
            return exc.HTTPMovedPermanently(request.route_url('engine_index',_query=request.GET,**request.matchdict))
        config.add_view(redirector, route_name='engine_shortcut')




    return config.make_wsgi_app()
