import os
import struct

from tornado import gen

from .constants import *


class StorageClient(object):
    """Client for Storage server.
    """

    HEADER_STRUCT = struct.Struct('!QBB')

    def __init__(self, stream, group_name, path_index=0):
        self.stream = stream
        self.group_name = group_name
        self.path_index = path_index

    @gen.coroutine
    def upload(self, file_io, size, ext=''):
        """Upload file to storage server.

        :param bytes file_data: data content of the file, it should be iterable.
        """

        non_slave_fmt = "!B Q %ds" % FDFS_FILE_EXT_NAME_MAX_LEN
        pkg_len = struct.calcsize(non_slave_fmt) + size
        cmd = STORAGE_PROTO_CMD_UPLOAD_FILE
        status = 0
        header = self.HEADER_STRUCT.pack(pkg_len, cmd, status)
        yield self.stream.write(header)
        payload = struct.pack(non_slave_fmt, 0, size, ext.encode())
        yield self.stream.write(payload)
        while True:
            send_buffer = file_io.read(1024)
            if not send_buffer:  # EOF
                break
            yield self.stream.write(send_buffer)

        header = yield self.stream.read_bytes(self.HEADER_STRUCT.size)
        pkg_len, cmd, status = self.HEADER_STRUCT.unpack(header)
        print("pkg_len: %s, cmd: %s, status: %s" % (pkg_len, cmd, status))
        data = yield self.stream.read_bytes(pkg_len)

        s = struct.Struct('!%ds %ds' % (16, pkg_len-16))
        group_name, remote_name = s.unpack(data)
        raise gen.Return((group_name.strip(b'\x00'), remote_name.strip(b'\x00')))

