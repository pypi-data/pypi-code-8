# -*- coding: utf-8 -*-
from zope.component import adapts

from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender, IBrowserLayerAwareExtender
from archetypes.schemaextender.field import ExtensionField


from Products.Archetypes.public import StringWidget, StringField

from collective.behavior.talcondition.interfaces import ITALConditionable
from collective.behavior.talcondition.interfaces import ICollectiveBehaviorTalconditionLayer


class TALConditionStringField(ExtensionField, StringField):
    """A string field that will contain an eventual TAL condition expression."""


class TALConditionExtender(object):
    """TALCondition class"""

    implements(ISchemaExtender, IBrowserLayerAwareExtender)

    # adapts elements that provide the IExternalIdentifierable marker interface
    adapts(ITALConditionable)

    layer = ICollectiveBehaviorTalconditionLayer

    fields = [
        TALConditionStringField(
            'tal_condition',
            required=False,
            default='',
            searchable=False,
            languageIndependent=True,
            widget=StringWidget(
                label=(u"TAL condition expression"),
                description=(u"Enter a TAL expression that will return True if "
                             u"element should be available."),))
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
