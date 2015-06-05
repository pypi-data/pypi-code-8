# -*- coding: utf-8 -*-
"""
    __init__.py

    :copyright: (c) 2014 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool
from storage_area import StorageArea
from product import ProductStorageArea, Product


def register():
    Pool.register(
        StorageArea,
        ProductStorageArea,
        Product,
        module='product_storage_area', type_='model'
    )
