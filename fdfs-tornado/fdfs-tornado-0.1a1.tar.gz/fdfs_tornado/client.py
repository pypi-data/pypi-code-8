from tornado import gen

from .pool import Pool
from .tracker import TrackerClient
from .storage import StorageClient


class makeclient(object):
    def __init__(self, ip, port):
        self.tracker_ip = ip
        self.tracker_port = port

    def __call__(self):
        return _AsyncFDFSClient(self.tracker_ip, self.tracker_port)


class _AsyncFDFSClient(object):
    """Asynchronous FDFS Client for tornado.

    Its methods should be compatible with ``fdfs_client-py`` , which is based on.
    """

    def __init__(self, ip, port):
        """
        :param str ip: ip address of a tracker server.
        :param int port: tcp port of the tracker server.
        """
        self.tracker_pool = Pool(ip, port)
        self.storage_pools = {}

    @gen.coroutine
    def upload(self, file_io, file_size, file_ext='', group_name=None, metadata=None):
        """Upload a file to storage server.

        :param BytesIO file_io: read data from it.
        :param int file_size: number of bytes.
        :param str file_ext: file extension.
        :param dict metadata: a dictionary if provided, describe the file.
            for example as below::

                'ext_name'  : 'jpg',
                'file_size' : '10240B',
                'width'     : '160px',
                'hight'     : '80px'
        :return: a dictionary as following:
            'Group name'      : group_name,
            'Remote file_id'  : remote_file_id,
            'Status'          : 'Upload successed.',
            'Local file name' : '',
            'Uploaded size'   : upload_size,
            'Storage IP'      : storage_ip
        """
        stream = yield self.tracker_pool.get_stream()
        try:
            tracker_client = TrackerClient(stream)
            group_name, server_ip, server_port, path_index = (
                yield tracker_client.get_storage_server(group_name))
        finally:
            self.tracker_pool.release_stream(stream)

        try:
            pool = self.storage_pools[(server_ip, server_port)]
        except KeyError:
            self.storage_pools[(server_ip, server_port)] = pool = Pool(server_ip, server_port)
        stream = yield pool.get_stream()
        try:
            storage_client = StorageClient(stream, group_name, path_index)
            ret = yield storage_client.upload(file_io, file_size, file_ext)
            raise gen.Return(ret)
        finally:
            pool.release_stream(stream)


if __name__ == '__main__':
    import os
    import sys
    from tornado.ioloop import IOLoop
    ioloop = IOLoop.instance()

    def handle_success(future):
        ret = future.result()
        print("ret:", ret)
        ioloop.stop()

    tracker_ip, tracker_port = sys.argv[1], 22122
    AsyncFDFSClient = makeclient(tracker_ip, tracker_port)
    client = AsyncFDFSClient()

    for filename in sys.argv[2:]:
        if not os.path.exists(filename):
            raise Exception("File not found:", filename)
        file_size = os.stat(filename).st_size
        file_ext = os.path.splitext(os.path.split(filename)[1])[1]
        with open(filename, 'rb') as f:
            future = client.upload(f, file_size, file_ext)
            future.add_done_callback(lambda _: ioloop.stop())
            ioloop.start()

            ret = future.result()
            print("result:", ret, '\n')
