from contextlib import contextmanager
import errno
import socket

from path import path
import paramiko


CLUSPRO_DATA_DIR = "/data/cluspro"


class ClusproClient(object):
    """Exposes various ways to get at files and directories on cluspro"""
    def __init__(self, config):
        self._config = config
        self._cache = path(config.get("cluspro", "local_cache"))

        self._username = config.get("cluspro", "username")
        self._hostname = config.get("cluspro", "hostname")
        self._port = config.getint("cluspro", "port")

        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((self._hostname, self._port))

        self._transport = paramiko.Transport(self._sock)
        try:
            self._transport.start_client()
        except paramiko.SSHException as e:
            print("SSHException:", e.message)
            raise e

        if config.has_option("cluspro", 'check_host_key'):
            pass  # TODO

        agent = paramiko.Agent()
        keys = agent.get_keys()
        for k in keys:
            try:
                self._transport.auth_publickey(self._username, k)
            except paramiko.SSHException:
                pass
            if self._transport.is_authenticated():
                break

        if not self._transport.is_authenticated():
            raise Exception("No public keys worked")

        self._sftp = paramiko.SFTPClient.from_transport(self._transport)

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()

    def close(self):
        self._sftp.close()
        self._transport.close()
        self._sock.close()

    @contextmanager
    def ftfile(self, cluspro_id, coeff_set, translation=0, mode="r"):
        ftfile_format = "ft.{0:03d}.{1:02d}"
        ftfile_filename = ftfile_format.format(coeff_set, translation)

        allfiles = self.listdir(cluspro_id)
        if ftfile_filename in allfiles:
            ftfile = ftfile_filename
            self._sftp.chdir(CLUSPRO_DATA_DIR + "/{0}".format(cluspro_id))
            with self._sftp.open(ftfile, mode) as ftfile:
                yield ftfile
        elif (ftfile_filename + ".gz") in allfiles:
            import gzip

            ftfile = ftfile_filename + ".gz"
            self._sftp.chdir(CLUSPRO_DATA_DIR + "/{0}".format(cluspro_id))
            with self._sftp.open(ftfile, mode) as ftfile:
                with gzip.GzipFile(fileobj=ftfile, mode="r") as gzfile:
                    yield gzfile
        else:
            raise IOError(errno.ENOENT,
                          "{0}/ft.{1:03d}.{2:02d}[.gz] not found".format(
                              cluspro_id, coeff_set, translation))

    def exists(self, path):
        try:
            self._sftp.stat(path)
        except IOError as e:
            if e.errno == errno.ENOENT:
                return False
            raise
        else:
            return True

    @contextmanager
    def recfile(self, cluspro_id, mode="r"):
        rec_file = CLUSPRO_DATA_DIR + "/{0}/rec.pdb".format(cluspro_id)

        if self.exists(rec_file):
            with self._sftp.open(rec_file, mode) as rec:
                yield rec
        elif self.exists(rec_file + ".gz"):
            import gzip

            self._sftp.chdir(CLUSPRO_DATA_DIR + "/{0}".format(cluspro_id))
            with self._sftp.open(rec_file + ".gz", mode) as rec:
                with gzip.GzipFile(fileobj=rec, mode=mode) as gzfile:
                    yield gzfile
        else:
            raise IOError(errno.ENOENT, "Receptor file not found")

    def listdir(self, cluspro_id):
        dirname = CLUSPRO_DATA_DIR + "/{0}".format(cluspro_id)
        return self._sftp.listdir(dirname)

    @contextmanager
    def open(self, cluspro_id, filepath, mode="r"):
        path_format = "/data/cluspro/{0}/{1}"
        remote_path = path_format.format(cluspro_id, filepath)

        with self._sftp.open(remote_path, mode) as f:
            yield f

    def local_cached_path(self, cluspro_id, filepath):
        return self._cache/"{0}/{1}".format(cluspro_id, filepath)

    def download_file(self, cluspro_id, filepath):
        local_path = self.local_cached_path(cluspro_id, filepath)

        if local_path.exists():
            return

        local_path.dirname().mkdir_p()
        with self.open(cluspro_id, filepath) as remote_file:
            with open(local_path, "w") as local_file:
                local_file.write(remote_file.read())
