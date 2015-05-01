import base64
import binascii
import bson
import re

__REGEX_AID = re.compile('^([A-Za-z0-9\-_]{16})$')


def cast(id, id_type=None):
    sid = str(id)

    if bson.objectid.ObjectId.is_valid(sid):
        bin = binascii.a2b_hex(sid)
        aid = base64.urlsafe_b64encode(bin)
    else:
        aid = sid
        aid_parts = aid.split('!')

        if not __REGEX_AID.match(aid_parts[-1]):
            raise ValueError('provided id must be an AgileId or ObjectId')
        elif id_type and aid_parts[0] == id_type:
            id_type = None

    if id_type:
        id_type = str(id_type)

        if '!' in id_type:
            raise ValueError('id_type cannot contain "!"')

        return '%s!%s' % (id_type, aid)

    return aid


def create(id_type=None):
    oid = bson.objectid.ObjectId()
    bin = binascii.a2b_hex(str(oid))
    aid = base64.urlsafe_b64encode(bin)

    if id_type:
        id_type = str(id_type)

        if '!' in id_type:
            raise ValueError('id_type cannot contain "!"')

        return '%s!%s' % (id_type, aid)

    return aid


def is_valid(id):
    sid = str(id)
    sid_parts = sid.split('!')

    is_scoped = all([len(p) > 0 for p in sid_parts])
    is_aid = __REGEX_AID.match(sid_parts[-1])

    return bool(is_scoped and is_aid)


def to_hexstring(id):
    sid = str(id)
    sid_parts = sid.split('!')

    if bson.objectid.ObjectId.is_valid(sid):
        return sid

    aid = sid_parts[-1]

    if not __REGEX_AID.match(aid):
        raise ValueError('provided id must be an AgileId or ObjectId')

    bin = base64.urlsafe_b64decode(aid)
    sid = binascii.b2a_hex(bin)

    return sid


def to_objectid(id):
    sid = to_hexstring(id)

    return bson.objectid.ObjectId(sid)
