# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from plone.protect import CheckAuthenticator
from zExceptions import NotFound, Unauthorized
from plone.memoize.view import memoize
from zope.security import checkPermission
from collective.pfg.userjoin import _
from collective.pfg.userjoin import logger
from Products.CMFCore.utils import getToolByName
from plone import api


class Base(object):

    @memoize
    def canEditAwkData(self):
        return checkPermission('collective.pfg.userjoin.permissions.editFields',
                               self.context)

    @memoize
    def canManageJoin(self):
        return checkPermission('collective.pfg.userjoin.permissions.manageJoin',
                               self.context)


class UserJoinAdapterView(BrowserView, Base):

    def __call__(self, *args, **kwargs):
        form = self.request.form
        if 'form.submitted' in form.keys():
            CheckAuthenticator(self.request)
            if not self.canManageJoin():
                raise Unauthorized()
            if 'delete' in form.keys():
                self.deleteEntries()
            elif 'confirm' in form.keys():
                self.createUsers()
        return self.index()

    def createUsers(self):
        uids = self.request.form.get('uids')
        context = self.context
        plone_utils = getToolByName(context, 'plone_utils')
        for uid in uids:
            data = context._inputStorage[uid]
            try:
                user = self._subscribe(data)
                del context._inputStorage[uid]
                context._inputItems -= 1
                context._length.change(-1)
                plone_utils.addPortalMessage(_('user_created_message',
                                               default=u"User $name added",
                                               mapping={'name': user.getId()}))
            except Exception as e:
                plone_utils.addPortalMessage(_('user_created_error_message',
                                               default=u"Error adding with data $data: $err",
                                               mapping={'data': data, 'err': str(e)}),
                                             type="error")
                logger.error(e)

    def _subscribe(self, data):
        context = self.context
        properties = {'fullname': data.get(context.getFullnameField())}
        for additional in context.getAdditionalUserInfo():
            formfield = additional['formfield']
            userfield = additional['userfield']
            properties[userfield] = data[formfield]
        user = api.user.create(username=data.get(context.getUseridField()),
                               email=data.get(context.getEmailField()),
                               properties=properties)        
        for g in context.getGroupsToBeAdded():
            api.group.add_user(groupname=g, username=user.getId())
        # Now reset user password
        rtool = getToolByName(context, 'portal_registration')
        try:
            rtool.mailPassword(user.getId(), self.request, immediate=True)
        except Exception as e:
            plone_utils = getToolByName(context, 'plone_utils')
            plone_utils.addPortalMessage(_('password_reset_issue_message',
                                           default=u"Unable to perform a password reset for $user: $message",
                                           mapping={'user': user.getId(), 'message': str(e)}),
                                         type="warning")
        return user

    def deleteEntries(self, uids=[]):
        uids = uids or self.request.form.get('uids')
        context = self.context
        plone_utils = getToolByName(context, 'plone_utils')
        for uid in uids:
            del context._inputStorage[uid]
            context._inputItems -= 1
            context._length.change(-1)
        plone_utils.addPortalMessage(_('entries_deleted_message',
                                       default=u"${count} elements deleted",
                                       mapping={'count': len(uids)}))

    def items(self):
        context = self.context
        self.context._initStorage()
        length = context._length.value
        if not length:
            return []
        return context._inputStorage.items()

    def keys(self):
        context = self.context
        keys = [context.getUseridField(), context.getFullnameField(), context.getEmailField()]
        additional = context.getAdditionalUserInfo()
        keys.extend([x['formfield'] for x in additional])
        return keys

    def hederKeys(self):
        context = self.context
        keys = self.keys()
        form_fields = context.fgFields()
        used_fields = [f for f in form_fields if f.getName() in keys]
        headers = []
        for k in keys: # BBB: computational disaster, to be refactored
            for f in used_fields:
                if k==f.getName():
                    headers.append(f.widget.label)
        return headers


class UserJoinDetailView(BrowserView, Base):
        
    def __init__(self, context, request):
        self.context = context
        self.request = request
        request.set('disable_border', True)

    def _loadStorage(self):
        uid = self.request.form.get('id')
        data = self.context._inputStorage.get(uid)
        if not data:
            raise NotFound("No data found for id %d" % uid)
        return data

    @property
    def username(self):
        context = self.context
        data = self._loadStorage()
        return data.get(context.getFullnameField() or context.useridField()) 

    @property
    @memoize
    def userdata(self):
        context = self.context
        data = self._loadStorage()
        form_fields = context.fgFields()
        results = []
        for f in form_fields:
            results.append({'name': f.widget.label,
                            'value': data.get(f.getName())})                
        return results
