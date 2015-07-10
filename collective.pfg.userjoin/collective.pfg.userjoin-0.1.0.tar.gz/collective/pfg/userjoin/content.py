# -*- coding: utf-8 -*-

import time
from AccessControl import ClassSecurityInfo
from BTrees.LOBTree import LOBTree
from Products.CMFCore.utils import getToolByName
from BTrees.Length import Length
from Products.ATContentTypes.content.base import registerATCT
from Products.Archetypes import atapi
from Products.PloneFormGen.content.actionAdapter import FormActionAdapter
from Products.PloneFormGen.content.actionAdapter import FormAdapterSchema
from Products.CMFPlone.utils import base_hasattr
from collective.pfg.userjoin import _
from collective.pfg.userjoin import config
from collective.pfg.userjoin.interfaces import IUserJoinAdapter
from types import StringTypes
from zope.interface import implementer
from Products.DataGridField.SelectColumn import SelectColumn
from Products.DataGridField.DataGridField import DataGridField
from Products.DataGridField.DataGridWidget import DataGridWidget
from DateTime import DateTime
from plone import api


UserJoinAdapterSchema = atapi.Schema((
    atapi.StringField('useridField',
        required=True,
        searchable=False,
        vocabulary="pfgFieldVocabulary",
        default="userid",
        write_permission=config.EditAwkwardFieldsPermission,
        widget=atapi.SelectionWidget(
            label=_(u"Userid form field"),
            description=_('userid_field_help',
                          default=u"Select the form field that hosts the userid.\n"
                                  u"This form field must be required."),
        ),
    ),

    atapi.StringField('fullnameField',
        required=False,
        searchable=False,
        vocabulary="pfgFieldVocabulary",
        default="fullname",
        write_permission=config.EditAwkwardFieldsPermission,
        widget=atapi.SelectionWidget(
            label=_(u"Fullname form field"),
            description=_('fullname_field_help',
                          default=u"Select the form field that hosts the user's fullname"),
        ),
    ),

    atapi.StringField('emailField',
        required=True,
        searchable=False,
        vocabulary="pfgFieldVocabulary",
        default="email",
        write_permission=config.EditAwkwardFieldsPermission,
        widget=atapi.SelectionWidget(
            label=_(u"Email form field"),
            description=_('email_field_help',
                          default=u"Select the form field that hosts the user's email.\n"
                                  u"This form field must be required."),
        ),
    ),

    DataGridField('additionalUserInfo',
        required=False,
        searchable=False,
        columns=("formfield", "userfield"),
        write_permission=config.EditAwkwardFieldsPermission,
        widget=DataGridWidget(
            label=_(u"Map additional user's data"),
            description=_('help_additionalUserInfo',
                          default=u"Additional form field to be mapped to user information available.\n"
                                  u"For every form field you can register additional user information that "
                                  u"will be populated on user creation."),
            columns={
                 'formfield' : SelectColumn(_(u"Form field"),
                                            vocabulary="pfgFieldVocabulary",
                                            col_description=_('formfield_coldescription',
                                                              default=u"Select a field present in the form"),
                                            required=True),
                 'userfield' : SelectColumn(_(u"User field"),
                                            vocabulary="userFieldVocabulary",
                                            col_description=_('userfield_coldescription',
                                                              default=u"Select a user information to apply "
                                                                      u"the form field to"),
                                            required=True),
            },
        ),
    ),

    atapi.LinesField('groupsToBeAdded',
        required=False,
        searchable=False,
        write_permission=config.EditAwkwardFieldsPermission,
        vocabulary_factory="plone.app.vocabularies.Groups",
        widget=atapi.MultiSelectionWidget(
            label=_(u"Automatic groups membership"),
            description=_('groupsToBeAdded_help',
                          default=u"Generated users will be automatically added to those groups"),
            format="checkbox",
        ),
    ),

))


@implementer(IUserJoinAdapter)
class UserJoinAdapter(FormActionAdapter):
    """A form action adapter that will save form input data and
       keep them until Manager use this data to create new site's members"""

    meta_type      = 'UserJoinAdapter'
    portal_type    = 'UserJoinAdapter'
    security       = ClassSecurityInfo()

    schema = FormAdapterSchema.copy() + UserJoinAdapterSchema.copy()

    security.declarePrivate('pfgFieldVocabulary')
    def pfgFieldVocabulary(self):
        return atapi.DisplayList(
            [['', '']] +  [[field.getName(), field.widget.label] for field in self.fgFields()])

    security.declarePrivate('userFieldVocabulary')
    def userFieldVocabulary(self):
        portal_memberdata = getToolByName(self, 'portal_memberdata')
        return atapi.DisplayList(
            [['', '']] + [[x,x] for x in portal_memberdata.propertyIds() if x not in config.RESERVED_PROPS])

    def _initStorage(self, clear=False):
        inited = base_hasattr(self, '_inputStorage') and \
                 base_hasattr(self, '_inputItems') and \
                 base_hasattr(self, '_length')

        if not inited or clear:
            self._inputStorage = LOBTree()
            self._inputItems = 0
            self._length = Length()

    def _addDataRow(self, value):
        # Stolen from saveDataDapter
        self._initStorage()
        id = int(time.time() * 1000)
        self._inputStorage[id] = value
        self._length.change(1)
        return id

    def onSuccess(self, fields, REQUEST=None):
        """Store data in the inner registry"""
        data = {}
        userid_provided = REQUEST.form.get(self.getUseridField())
        if userid_provided:
            rtool = getToolByName(self, 'portal_registration')
            if api.user.get(username=userid_provided) is not None:
                return {self.getUseridField(): _('username_already_taken_error',
                                                 default=u'The username is already in use')}
            if userid_provided=='Anonymous User' or \
                    not rtool._ALLOWED_MEMBER_ID_PATTERN.match(userid_provided):
                return {self.getUseridField(): _('username_invalid_error',
                                                 default=u'The username is invalid')}            
            # userid already stored in the registry
            for v in self._inputStorage.values():
                if userid_provided==v.get(self.getUseridField()):
                    return {self.getUseridField(): _('username_already_taken_error',
                                                     default=u'The username is already in use')}                    
        for field in fields:
            # we do not handle files for now
            if field.isFileField() or field.isLabel():
                continue
            val = REQUEST.form.get(field.fgField.getName(), '')
            if not type(val) in StringTypes:
                # Zope has marshalled the field into
                # something other than a string
                val = str(val)
            data[field.fgField.getName()] = val
            data['__timestamp__'] = DateTime()
        id = self._addDataRow(data)
        REQUEST['pfguserjoin_obj'] = self
        REQUEST['pfguserjoin_newid'] = id


registerATCT(UserJoinAdapter, config.PROJECTNAME)
