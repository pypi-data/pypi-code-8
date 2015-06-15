"""
Exposes SFTP interface to ``domain.Company.mount``, which allows:

- ``domain.Settlement`` uploads
- ``domain.Settlement`` downloads

.. code:: bash

    $ mythicals sftp -l i

which is typically daemonized via e.g. supervisord like:

.. code:: ini

    [program:mythical-sftp]
    command=mythicals sftp --host=0.0.0.0 --port=4522 --log-conf=/etc/mythical/sftp/log.conf --host-key=/etc/mythical/sftp/host_rsa --forking
    autostart=true
    autorestart=true
    user=mythical
    group=mythical

"""
import calendar
import errno
import functools
import logging
import os
import SocketServer
import time
import threading

import Crypto.Random
import fs
import netaddr
import paramiko
import pwho
import sqlalchemy.orm as saorm

from mythicals import domain, db, tracer, config


logger = logging.getLogger(__name__)


def init(config):
    pass


def as_sftp_error(func):

    func = fs.errors.convert_fs_errors(func)

    name = getattr(func, 'func_name', '<unknown>')

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(
            '%s - enter on (%r,%r) from %s',
            name, args[1:], kwargs, args[0].client_address,
        )
        try:
            rc = func(*args, **kwargs)
        except Exception as ex:
            if hasattr(ex, 'errno'):
                error = ex.errno
            else:
                error = None
            rc = paramiko.SFTPServer.convert_errno(error)
            logger.info(
                '%s - error %s on (%r%r) from %s\n',
                name, rc, args[1:], kwargs, args[0].client_address, exc_info=ex
            )
        logger.debug(
            '%s - exit %s', name, '<data>' if isinstance(rc, basestring) else rc
        )
        return rc

    return wrapper


class SFTPHandle(paramiko.SFTPHandle):

    def __init__(self, owner, path, flags, attr):
        super(SFTPHandle, self).__init__(flags)
        self.owner = owner
        self.path = path
        mode = SFTPHandle.as_mode(flags)
        if 'w' in mode:
            if not self.is_submission:
                raise IOError(errno.EACCES, 'Permission denied')

        self.fo = owner.fs.open(path, mode)

    @classmethod
    def as_mode(cls, flags):
        open_flag = flags & (os.O_RDONLY | os.O_WRONLY | os.O_RDWR)
        if open_flag == os.O_RDONLY:
            mode = 'rb'
        elif open_flag == os.O_WRONLY:
            mode = 'wb'
        elif open_flag == os.O_RDWR:
            mode = 'rwb'
        if flags & os.O_APPEND:
            mode += '+'
        return mode

    @property
    def client_address(self):
        return self.owner.client_address

    @property
    def is_submission(self):
        return (
            self.path.startswith('uploads/bank_account') or
            self.path.startswith('uploads/credit_card') or
            self.path.startswith('uploads/merchant')
        )

    def create_submission(self):
        if self.path.startswith('uploads/bank_account'):
            cls = domain.BankAccountSubmission
        elif self.path.startswith('uploads/credit_card'):
            cls = domain.CreditCardSubmission
        elif self.path.startswith('uploads/merchant'):
            cls = domain.MerchantSubmission
        external_id = os.path.splitext(os.path.basename(self.path))[0]
        obj = cls.create(
            company=self.owner.company,
            location=self.path,
            external_id=external_id,
        )
        db.Session.commit()
        return obj

    def finalize(self):
        if 'w' in self.fo.mode and self.is_submission:
            self.create_submission()

    # paramiko.SFTPHandle

    @as_sftp_error
    def close(self):
        self.fo.close()
        self.finalize()
        return paramiko.SFTP_OK

    @as_sftp_error
    def read(self, offset, length):
        self.fo.seek(offset)
        data = self.fo.read(length)
        return data

    @as_sftp_error
    def write(self, offset, data):
        self.fo.seek(offset)
        self.fo.write(data)
        return paramiko.SFTP_OK

    @as_sftp_error
    def stat(self):
        return self.owner.stat(self.path)


class ServerInterface(paramiko.ServerInterface):

    def __init__(self, client_address):
        self.client_address = client_address
        self.company_id = None

    def company_for(self, username):
        username = (
            username.decode('utf-8')
            if isinstance(username, str)
            else username
        )
        try:
            company = domain.Company.query.filter_by(name=username).one()
        except saorm.exc.NoResultFound:
            return
        return company

    # paramiko.ServerInterface

    def get_allowed_auths(self, username):
        return ','.join(['password'])

    def check_auth_none(self, username):
        logger.info(
            'auth none from %s failed, username=%s ',
            self.client_address, username,
        )
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        logger.info(
            'auth publickey from %s failed, username=%s ',
            self.client_address, username,
        )
        return paramiko.AUTH_FAILED

    def check_auth_password(self, username, password):
        company = self.company_for(username)
        if company is None:
            logger.info(
                'auth password from %s failed, username=%s ',
                self.client_address, username,
            )
            return paramiko.AUTH_FAILED
        if not company.authenticate(password):
            logger.info(
                'auth password from %s failed, username=%s ',
                self.client_address, username,
            )
            return paramiko.AUTH_FAILED
        self.company_id = company.id
        logger.info(
            'auth password from %s succeeded, username=%s ',
            self.client_address, username,
        )
        return paramiko.AUTH_SUCCESSFUL

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        logger.info(
            'channel request denied from %s, kind=%s',
            self.client_address, kind
        )
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED


class SFTPServerInterface(paramiko.SFTPServerInterface):

    def __init__(self, server, *args, **kwargs):
        self.client_address = server.client_address
        self.company_id = server.company_id
        self.fs = None
        super(SFTPServerInterface, self).__init__(server, *args, **kwargs)

    # paramiko.SFTPServerInterface

    def session_started(self):
        tracer.reset()
        self.company = domain.Company.query.get(self.company_id)
        self.fs = self.company.mount

    def session_ended(self):
        self.fs = None
        self.company = None

    @as_sftp_error
    def open(self, path, flags, attr):
        return SFTPHandle(self, path, flags, attr)

    @as_sftp_error
    def list_folder(self, path):
        return [
            self.stat(os.path.join(path, name))
            for name in self.fs.listdir(path)
        ]

    @as_sftp_error
    def stat(self, path):

        def _as_time(v):
            return calendar.timegm(v.utctimetuple())

        info = self.fs.getinfo(path)
        stat = paramiko.SFTPAttributes()

        stat.filename = os.path.basename(path)

        # st_size
        for key in ['st_size', 'size']:
            if key in info:
                stat.st_size = info[key]
                break
        else:
            stat.st_size = 4096 if self.fs.isdir(path) else 0

        # st_mode
        stat.st_mode = info['st_mode']

        # st_atime
        if 'accessed_time' in info:
            stat.st_atime = _as_time(info['accessed_time'])

        # st_mtime
        if 'modified_time' in info:
            stat.st_mtime = _as_time(info['modified_time'])

        return stat

    @as_sftp_error
    def lstat(self, path):
        return self.stat(path)

    @as_sftp_error
    def remove(self, path):
        return paramiko.sftp.SFTP_OP_UNSUPPORTED

    @as_sftp_error
    def rename(self, oldpath, newpath):
        return paramiko.sftp.SFTP_OP_UNSUPPORTED

    @as_sftp_error
    def mkdir(self, path, attr):
        return paramiko.sftp.SFTP_OP_UNSUPPORTED

    @as_sftp_error
    def rmdir(self, path):
        return paramiko.sftp.SFTP_OP_UNSUPPORTED

    @as_sftp_error
    def canonicalize(self, path):
        # FIXME: no path reveals
        return super(SFTPServerInterface, self).canonicalize(path)


class SFTPRequestHandler(
          SocketServer.StreamRequestHandler,
          pwho.StreamRequestMixin,
      ):

    SFTPServerInterface = SFTPServerInterface

    negotiation_poll = 0.1

    negotiation_timeout = 60

    auth_timeout = 60

    join_timeout = 10

    # pwho.StreamRequestMixin

    def proxy_authenticate(self, proxy_info):
        ip = netaddr.IPAddress(proxy_info.destination_address)
        return any(ip in cidr for cidr in config.SFTP_PROXY_CIDRS)

    # SocketServer.StreamRequestHandler

    timeout = 60

    def handle(self):
        try:
            # proxy protocol
            client_address = self.client_address
            proxy_info = self.proxy_protocol(
                error='unread', default=None, authenticate=True,
            )
            if proxy_info:
                client_address = proxy_info.source_address, proxy_info.source_port

            # transport
            t = paramiko.Transport(self.request)
            if self.server.host_key is not None:
                t.add_server_key(self.server.host_key)
            t.set_subsystem_handler(
                'sftp', paramiko.SFTPServer, self.SFTPServerInterface,
            )

            try:
                # serve
                server = ServerInterface(client_address)
                event = threading.Event()
                t.start_server(server=server, event=event)

                # negotiate
                start = time.time()
                while True:
                    if event.wait(self.negotiation_poll):
                        if not t.is_active():
                            ex = t.get_exception() or 'Negotiation failed.'
                            logger.info('%r, disconnecting - %s', self.client_address, ex)
                            return
                        logger.debug('negotiation was OK')
                        break
                    if (self.negotiation_timeout is not None and
                        time.time() - start > self.negotiation_timeout):
                        logger.info('%r, disconnecting - %s', self.client_address, 'Negotiation timed out.')
                        return

                # accepted
                chan = t.accept(self.auth_timeout)
                if chan is None:
                    logger.info('%r, disconnecting - %s', self.client_address, 'auth failed, channel is None.')
                    return

                # command(s)
                while t.isAlive():
                    t.join(timeout=self.join_timeout)
            finally:
                logger.info('%r, cleaning up connection - %s', self.client_address, 'Bye.')
                t.close()
        finally:
            db.teardown_session()


class SFTPServer(SocketServer.TCPServer):

    def __init__(self, address, host_key):
        self.host_key = host_key
        self.client_address = None
        SocketServer.TCPServer.__init__(self, address, SFTPRequestHandler)

    # SocketServer.TCPServer

    allow_reuse_address = True


class ForkingSFTPServer(SocketServer.ForkingMixIn, SFTPServer):

    def finish_request(self, request, client_address):
        Crypto.Random.atfork()
        return SFTPServer.finish_request(self, request, client_address)


class ThreadingSFTPServer(SocketServer.ThreadingMixIn, SFTPServer):

    pass
