# -*- coding: utf-8 -*-
"""
    storage_area.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""

from trytond.model import ModelSQL, ModelView, fields

__all__ = ['StorageArea']


class StorageArea(ModelSQL, ModelView):
    "Storage Area"
    __name__ = 'storage.area'

    name = fields.Char('Name', required=True, select=True)
    sequence = fields.Integer('Sequence', required=True, select=True)
    description = fields.Text('Description', select=True)

    @classmethod
    def __setup__(cls):
        super(StorageArea, cls).__setup__()
        cls._order.insert(0, ('sequence', 'ASC'))
        cls._order.insert(1, ('name', 'ASC'))

    @staticmethod
    def default_sequence():
        return 10
