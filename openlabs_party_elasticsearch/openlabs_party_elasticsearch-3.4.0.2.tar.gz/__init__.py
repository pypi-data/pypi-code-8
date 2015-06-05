# -*- coding: utf-8 -*-
"""
    __init__.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool
from party import Party, Address


def register():
    Pool.register(
        Party,
        Address,
        module='party_elasticsearch', type_='model'
    )
