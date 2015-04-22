# -*- coding: utf-8 -*-
"""
    __init__.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool, PoolMeta
from trytond.config import config

from audit_trail import AuditTrail


def register():
    """This also registers history models defined in tryton configuration as:

        [audit_trail]
        party.party = module_name
        party.address = module_name
        party.contact_mechanism = module_name
    """
    Pool.register(
        AuditTrail,
        module='audit_trail', type_='model'
    )

    if not config.has_section('audit_trail'):
        return

    # Tryton will not be able to fetch the previous class for history models
    # until they are defined in tryton.cfg(must be a dependency!). Without
    # this history will not be registered.
    #
    # So we are registering models in corresponding modules only, eg: product
    # module can register product.product history but can't party.party's.
    history_classes = {}
    for model_name in config.options('audit_trail'):
        history_classes.setdefault(
            config.get('audit_trail', model_name), []).append(PoolMeta(
                "Audit", (object, ),
                {'__name__': model_name, '_history': True}
            ))

    for module, classes in history_classes.iteritems():
        Pool.register(
            *classes,
            module=module, type_='model'
        )
