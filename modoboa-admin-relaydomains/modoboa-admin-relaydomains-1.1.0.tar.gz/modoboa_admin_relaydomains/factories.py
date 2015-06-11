"""Factories."""

import factory

from modoboa.core.factories import PermissionFactory

from modoboa_admin.factories import DomainFactory

from . import models


class ServiceFactory(factory.DjangoModelFactory):

    """Factory to create Service instances."""

    class Meta:
        model = models.Service
        django_get_or_create = ('name', )

    name = 'dummy'


class RelayDomainFactory(PermissionFactory):

    """Factory to create RelayDomain instances."""

    class Meta:
        model = models.RelayDomain

    domain = factory.SubFactory(DomainFactory)
    target_host = 'external.host.tld'
    verify_recipients = True
    service = factory.SubFactory(ServiceFactory)
