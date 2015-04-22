# -*- coding: utf-8 -*-
"""
    audit_trail.py

    :copyright: (c) 2015 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
from trytond.pool import Pool
from trytond.model import ModelSingleton, ModelSQL, ModelView, fields
from trytond.config import config


class AuditTrail(ModelSingleton, ModelSQL, ModelView):
    "Audit Trail for tryton models"
    __name__ = "audit_trail"

    models = fields.Function(
        fields.One2Many("ir.model", None, 'Audit Trail Enabled For:'),
        getter="get_models"
    )

    def get_models(self, name):
        Model = Pool().get('ir.model')

        if not config.has_section('audit_trail'):
            return []

        return map(int, Model.search([
            ('model', 'in', config.options('audit_trail'))]
        ))
