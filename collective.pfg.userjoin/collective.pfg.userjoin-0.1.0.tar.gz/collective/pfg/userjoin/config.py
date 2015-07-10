# -*- coding: utf-8 -*-

PROJECTNAME = "collective.pfg.userjoin"
RESERVED_PROPS =  ('email', 'fullname', 'portal_skin', 'listed',
                   'login_time', 'last_login_time', 'error_log_update',
                   'language', 'ext_editor', 'wysiwyg_editor', 'visible_ids')

ADD_PERMISSIONS = {
    'UserJoinAdapter': PROJECTNAME + ': Add User Join Adapter',
}

EditAwkwardFieldsPermission = 'collective.pfg.userjoin: Edit Awkward Fields'