__author__ = 'Stephan Conrad <stephan@conrad.pics>'

import exon.utils.fileutils
import ctypes

_AD_SYNTAX = {
    '2.5.5.9': 'Flags'
}

class ADLdapAttribute(object):

    def __init__(self, attribute):
        self.isSingleValued = False
        self.attributeSyntax = None
        self.attributeSyntaxText = None
        parse = False
        for line in exon.utils.fileutils.readfileAsArray('/usr/share/samba/setup/ad-schema/MS-AD_Schema_2K8_R2_Attributes.txt'):
            line = line.strip()
            if ': ' in line:
                (key, value) = line.split(": ", 1)
                if 'ldapDisplayName' == key:
                    if attribute == value:
                        parse = True
                    else:
                        parse = False
                if parse:
                    if 'isSingleValued' == key:
                        self.isSingleValued = value.strip().lower() == 'true'
                    elif 'attributeSyntax' == key:
                        self.attributeSyntax = value
                        if value in _AD_SYNTAX:
                            self.attributeSyntaxText = _AD_SYNTAX[value]

class _ParseAdFlag(object):
    _FLAGS = {}

    @classmethod
    def getFlags(cls, flag):
        flag = int(ctypes.c_uint32(flag).value)
        ret = {}
        for key in cls._FLAGS:
            ret[key] = bool(cls._FLAGS[key] & flag)
        return  ret

    @classmethod
    def setFlag(cls, flag, key, state = True):
        flag = int(ctypes.c_uint32(flag).value)
        old_val = cls.getFlags(flag)
        if key in cls._FLAGS and key in old_val:
            if state:
                if not old_val[key]:
                    flag |= cls._FLAGS[key]
            else:
                if old_val[key]:
                    flag &= ~cls._FLAGS[key]
        return flag

class ParseAdSamAccountType(_ParseAdFlag):
    _FLAGS = {
        'SAM_DOMAIN_OBJECT': 0x0,
        'SAM_GROUP_OBJECT': 0x10000000,
        'SAM_NON_SECURITY_GROUP_OBJECT': 0x10000001,
        'SAM_ALIAS_OBJECT': 0x20000000,
        'SAM_NON_SECURITY_ALIAS_OBJECT': 0x20000001,
        'SAM_USER_OBJECT': 0x30000000,
        'SAM_NORMAL_USER_ACCOUNT': 0x30000000,
        'SAM_MACHINE_ACCOUNT': 0x30000001,
        'SAM_TRUST_ACCOUNT': 0x30000002,
        'SAM_APP_BASIC_GROUP': 0x40000000,
        'SAM_APP_QUERY_GROUP': 0x40000001,
        'SAM_ACCOUNT_TYPE_MAX': 0x7fffffff
    }


class ParseAdGroupType(_ParseAdFlag):
    _FLAGS = {
        'CREATED_BY_SYSTEM': 0x00000001,
        'GLOBAL_SCOPE': 0x00000002,
        'LOCAL_SCOPE': 0x00000004,
        'UNIVERSAL_SCOPE': 0x00000008,
        'APP_BASIC': 0x00000010,
        'APP_QUERY': 0x00000020,
        'SECURITY_GROUP': 0x80000000,
    }


if __name__ == "__main__":
    print(ParseAdSamAccountType.getFlags(268435456))
    print(ParseAdGroupType.getFlags(-2147483646))
    print(ParseAdGroupType.getFlags(ParseAdGroupType.setFlag(-2147483646, 'GLOBAL_SCOPE', False)))
    print(ParseAdGroupType.getFlags(ParseAdGroupType.setFlag(-2147483646, 'APP_QUERY', True)))