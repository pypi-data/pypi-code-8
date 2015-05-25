# -*- encoding:utf-8 -*-
import memcache
from edo_client import OcClient, OrgClient
try:
    from ztq_core import set_key, get_key
    from ztq_core import get_redis
except ImportError:
    def set_key(key, value, system=''): pass
    def get_key(key, system=''): return None
    def get_redis(key): return None

OU_PREFIX = 'groups.tree.'
COMPANY_PREFIX = 'groups.company.'
JOB_PREFIX = 'groups.jobs.'
OLD_JOB_PREFIX = 'groups.job.'
USER_PREFIX = 'users.'
CLIENT_PREFIX = 'clients.'

def replace_prefix(users=[]):

    results = []
    for user in users:
        if user.startswith(OU_PREFIX):
            results.append('ou:%s' % user[len(OU_PREFIX):])
        elif user.startswith(COMPANY_PREFIX):
            results.append('company:%s' % user[len(COMPANY_PREFIX):])
        elif user.startswith(JOB_PREFIX):
            results.append('group:%s' % user[len(JOB_PREFIX):])
        elif user.startswith(OLD_JOB_PREFIX):
            results.append('group:%s' % user[len(OLD_JOB_PREFIX):])
        elif user.startswith(USER_PREFIX):
            results.append('person:%s' % user[len(USER_PREFIX):])
        elif user.startswith(CLIENT_PREFIX):
            results.append('person:%s' % user[len(CLIENT_PREFIX):])
        else:
            raise ValueError, 'zopen.cacheorg.cacheorg.replace_prefix:ValueError:%s' % user

    return results 

def remove_prefix(pid):
    if pid.startswith(OU_PREFIX):
        return pid[len(OU_PREFIX):]
    elif pid.startswith(COMPANY_PREFIX):
        return pid[len(COMPANY_PREFIX):]
    elif pid.startswith(JOB_PREFIX):
        return pid[len(JOB_PREFIX):]
    elif pid.startswith(USER_PREFIX):
        return pid[len(USER_PREFIX):]

    raise ValueError, 'zopen.cacheorg.cacheorg.remove_prefix:ValueError:%s' % pid
        
def add_prefix(object_type, user_name):
    if object_type == 'ou':
        return '%s%s' % (OU_PREFIX, user_name)
    elif object_type == 'group':
        return '%s%s' % (JOB_PREFIX, user_name)
    elif object_type == 'company':
        return '%s%s' % (COMPANY_PREFIX, user_name)
    elif object_type == 'person':
        return '%s%s' % (USER_PREFIX, user_name)


def DenyCacheKeysForMember(account, principal_id, parents='', children=''):
    # 个人的详细资料
    principalinfo_key = "pinfo:%s:%s.%s"
    # 用户所在的组的信息
    listusergroups_key = "gusers:%s:%s"
    # 组成员信息
    listgroupmembers_key = "gmembers:%s:%s"
    listouonelevelmembersdetail_key = "oudetail:%s:%s:%s"
    listorgstructure_key = "orgstr:%s:%s"

    # 删除自身
    keys = []
    if principal_id.startswith('users.'):
        object_type = 'person'
        uid = principal_id.split('.', 1)[-1]
    elif principal_id.startswith('groups.jobs.'):
        object_type = 'group'
        uid = principal_id.split('.', 2)[-1]
    elif principal_id.startswith('groups.tree.'):
        object_type = 'ou'
        uid = principal_id.split('.', 2)[-1]
    elif principal_id.startswith('groups.company.'):
        object_type = 'company'
        uid = principal_id.split('.', 2)[-1]
    else:
        raise ValueError("principal_id is not person、group、ou, %s" % principal_id)

    keys.append(principalinfo_key % (account, object_type, uid))
    keys.append(listorgstructure_key)
    # 部门添加
    if object_type != 'person':
        keys.append(listouonelevelmembersdetail_key % (account, principal_id.split('.', 2)[-1], 'True'))
        keys.append(listouonelevelmembersdetail_key % (account, principal_id.split('.', 2)[-1], 'False'))
        keys.append(listorgstructure_key % (account, principal_id.split('.', 2)[-1]))
    # 删除父节点
    if parents:
        parents = replace_prefix(parents)
        keys.append(listusergroups_key % (account, uid))
        for group_id in parents:
            keys.append(listgroupmembers_key % (account, group_id))
            keys.append(listouonelevelmembersdetail_key % (account, group_id.split(':')[-1], 'True'))
            keys.append(listouonelevelmembersdetail_key % (account, group_id.split(':')[-1], 'False'))
            keys.append(listorgstructure_key % (account, group_id.split(':')[-1]))

    # 删除子节点
    if children:
        keys.append(listgroupmembers_key % (account, replace_prefix([principal_id])[0]))
        for child in children:
            keys.append(principalinfo_key % (account, 'person', child.split('.', 1)[-1]))
            keys.append(listusergroups_key % (account,child.split('.', 1)[-1]))

    get_redis('cache').delete(*keys)

def DenyCacheKeysForInstance(account_name):
    get_redis('cache').delete('instanceinfo:%s'%(account_name))



class CachedOcClient(OcClient):

    def __init__(self, server_url, app_id, secret, account=None, instance=None, maxsize=10000, expire=24*3600):
        OcClient.__init__(self, server_url, app_id, secret, account=account, instance=instance)
        self.cache = memcache.lru_cache(maxsize=maxsize, expire=expire)

    def get_token_info(self):
        """ 得到用户的token_info """
        try:
            token_info = self.cache.get(self.token_code)
        except KeyError:
            token_info = self.oauth.get_token_info()
            self.cache.put(self.token_code, token_info)
        return token_info

    def get_user_roles(self, user, account=None):
        """ 得到用户的角色"""
        key = "roles:%s:%s"%(account, user)
        try:
            return self.cache.get(key)
        except KeyError:
            roles = self.account.get_user_roles(user=user, account=account)
            self.cache.put(key, roles)
            return roles

class CachedOrgClient(OrgClient, OcClient):
    """ 支持缓存的admin接口 """

    def __init__(self, server_url, app_id, secret, account=None, instance=None, maxsize=5000, expire=120):
        OrgClient.__init__(self, server_url, app_id, secret, account=account, instance=instance)
        self.cache = memcache.lru_cache(maxsize=maxsize, expire=expire)

    def _get_cache(self, cache_key, skip_memcached=False):
        # 从内存中取
        if not skip_memcached:
            try:
                return self.cache.get(cache_key)
            except:
                pass

        # 从redis上取
        result = get_key(cache_key, 'cache')
        if result is not None:
            self.cache.put(cache_key, result)
            return result

    def refresh_cache(self, keys):
        for info in keys:
            del_type = info.pop('type')
            if del_type == 'DeleteOrg':
                DenyCacheKeysForMember(**info)
            elif del_type == 'DeleteInstance':
                DenyCacheKeysForInstance(**info)


    def _getValueUseCache(self, cache_key, func, skip_cache=False, **params):
        """ 根据key从redis得到值，否则从rpc调用得到值并放入redis """

        # 从内存和redis上查找缓存 
        cache = self._get_cache(cache_key, skip_cache)
        if cache:
            return cache

        # 从服务器上取 
        result = func(**params)
        if result is None:
            return None

        # 放入redis
        set_key(cache_key, result, 'cache')
        self.cache.put(cache_key, result)

        return result

    def get_objects_info(self, account, pids, skip_cache=False):
        """ 批量得到人员和组的信息 """
        users = []
        values = []
        for pid in pids:
            object_type, name = pid.split(':')
            key = "pinfo:%s:%s.%s"%(account, object_type, name)

            # 从内存和redis上查找缓存 
            value = self._get_cache(key, skip_cache)
            if value is None:
                users.append(pid)
            else:
                values.append(value)

        if not users:
            return values

        infos = self.org.get_objects_info(account=account, objects=','.join(users))
        for info in infos:
            key = "pinfo:%s:%s.%s"%(account, info['object_type'], info['id'])
            self.cache.put(key, info)
            set_key(key, info, 'cache')
            values.append(info)
        return values

    def list_person_groups(self, account, user_id):
        key = "gusers:%s:%s"%(account, user_id)
        remote_groups = self._getValueUseCache(key, self.org.list_person_ougroups, person=user_id, account=account) or {}
        return remote_groups

    def get_ou_detail(self, account, ou_id, include_disabled=False, skip_cache=False):
        key = 'oudetail:%s:%s:%s' % (account, ou_id, str(include_disabled))
        return self._getValueUseCache(key, self.org.get_ou_detail, ou_id=ou_id, include_disabled=include_disabled, account=account, skip_cache=skip_cache)

    def list_groups_members(self, account, group_ids, skip_cache=False):
        """ 批量得到组的人员列表 """
        if isinstance(group_ids, basestring):
            group_ids = [group_ids]

        groups = []
        result = []
        for group_id in group_ids:
            key = "gmembers:%s:%s"%(account, group_id)

            value = self._get_cache(key) if not skip_cache else None
            if value is None:
                groups.append(group_id)
            else:
                result.extend([user_id for user_id in value])
        if not groups:
            return list(set(result))

        groups = self.org.list_groups_members(account=account, groups=','.join(groups))
        for group_key, group_value in groups.items():
            key = "gmembers:%s:%s"%(account, group_key)
            self.cache.put(key, group_value)
            set_key(key, group_value, 'cache')
            result.extend([user_id for user_id in group_value])

        return list(set(result))

    def list_org_structure(self, account, root='default', skip_cache=False):
        key = "orgstr:%s:%s" % (account, root)
        org_structure = self._getValueUseCache(key, self.org.list_org_structure, account=account, root=root, skip_cache=skip_cache) or {}
        
        return org_structure

    def list_instances(self, account, application, skip_cache=False):
        key = "instanceinfo:%s" % (account)
        value = self._getValueUseCache(key, self.account.list_instances, account=account, application=application, skip_cache=skip_cache)
        return value

