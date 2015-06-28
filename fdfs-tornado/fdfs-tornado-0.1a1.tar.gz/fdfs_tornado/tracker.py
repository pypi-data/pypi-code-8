import struct

from tornado import gen

from .constants import *


class TrackerClient(object):
    """Client to Tracker Server.
    """

    HEADER_STRUCT = struct.Struct('!QBB')

    def __init__(self, stream):
        self.stream = stream

    @gen.coroutine
    def get_storage_server(self, group_name=None):
        if group_name is None:
            pkg_len, cmd = 0, QUERY_WITHOUT_GROUP
        else:
            cmd = TRACKER_PROTO_CMD_SERVICE_QUERY_STORE_WITH_GROUP_ONE
            pkg_len = FDFS_GROUP_NAME_MAX_LEN
        status = 0
        header = self.HEADER_STRUCT.pack(pkg_len, cmd, status)
        yield self.stream.write(header)
        header = yield self.stream.read_bytes(self.HEADER_STRUCT.size)
        pkg_len, cmd, status = self.HEADER_STRUCT.unpack(header)
        print("pkg_len: %s, cmd: %s, status: %s" % (pkg_len, cmd, status))

        data = yield self.stream.read_bytes(pkg_len)
        s = struct.Struct('!%ds %ds Q B' % (FDFS_GROUP_NAME_MAX_LEN, IP_ADDRESS_SIZE-1))
        group_name, ip_addr, port, path_index = s.unpack(data)
        group_name = group_name.strip(b'\x00')
        ip_addr = ip_addr.strip(b'\x00')
        print("group_name:", group_name, ", ip_addr:", ip_addr,
              ", port:", port, ", path_index:", path_index)

        raise gen.Return((group_name, ip_addr, port, path_index))

