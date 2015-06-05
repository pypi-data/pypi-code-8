# -*- coding: utf-8 -*-
"""
    product.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""

from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta

__all__ = ['Product', 'ProductStorageArea']
__metaclass__ = PoolMeta


class ProductStorageArea(ModelSQL, ModelView):
    "Product Storage Area"
    __name__ = 'product.storage.area'

    product = fields.Many2One(
        'product.product', 'Product', required=True, select=True
    )
    sequence = fields.Integer('Sequence', required=True, select=True)
    location = fields.Many2One(
        'stock.location', 'Location', required=True, select=True
    )

    @classmethod
    def __setup__(cls):
        super(ProductStorageArea, cls).__setup__()
        cls._order.insert(0, ('sequence', 'ASC'))

    @staticmethod
    def default_sequence():
        return 10


class Product:
    __name__ = 'product.product'

    storage_areas = fields.One2Many(
        'product.storage.area', 'product', 'Storage Areas'
    )
