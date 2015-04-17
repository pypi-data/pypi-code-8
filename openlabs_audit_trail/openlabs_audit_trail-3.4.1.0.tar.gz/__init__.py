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
        party.party =
        party.address =
        party.contact_mechanism =
    """
    classes_to_register = [AuditTrail]

    if config.has_section('audit_trail'):
        for model_name in config.options('audit_trail'):
            classes_to_register.append(PoolMeta(
                "Audit", (object, ),
                {'__name__': model_name, '_history': True}
            ))

    Pool.register(
        *classes_to_register,
        module='audit_trail', type_='model'
    )
