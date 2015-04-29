from nekbot.utils.modules import get_module

__author__ = 'nekmo'

from nekbot.conf import settings

def get_permissions_tree(tree):
    def get_permission(perm):
        perms = [perm]
        for subperm in tree[perm]:
            perms += get_permission(subperm)
        return perms
    new_tree = {}
    for perm in tree:
        new_tree[perm] = get_permission(perm)
    return new_tree

permissions_tree = get_permissions_tree(settings.PERMISSIONS_TREE)

def always_true(user, perm):
    """Only for debug!
    """
    return True

def perms_from_settings(user, wanted_perm):
    settings_property = '%s_PERMISSIONS' % user.protocol.name.upper()
    if not hasattr(settings, settings_property):
        return False
    perms = getattr(settings, settings_property)
    if not user.get_id() in perms: return False
    for perm in perms[user.id]:
        if wanted_perm in permissions_tree[perm]:
            return True
    return False

def has_perm(user, perm):
    for perm_method in settings.PERMS_METHODS:
        perm_method = get_module(perm_method)
        if perm_method(user, perm): return True
    return False