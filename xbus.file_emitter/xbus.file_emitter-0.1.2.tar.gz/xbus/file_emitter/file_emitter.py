"""Generic Xbus file emitter."""

from aiozmq import rpc
import asyncio
import datetime
from decimal import Decimal
import msgpack
import pyjon.descriptors as pjdesc
from xml.etree import cElementTree as et


class FileEmitterException(Exception):
    pass


class FileEmitter(object):
    """Generic Xbus file emitter."""

    def __init__(
        self, broker_front_url, login, password, descriptors, loop=None
    ):
        """Initialize the file emitter and descriptors.

        :param broker_front_url: URL of the Xbus front-end.
        :param login: Login to log into the Xbus front-end.
        :param login: Password to log into the Xbus front-end.
        :param descriptors: List of input descriptors.
        :type desriptors: List of strings.
        :param loop: 0mq loop.

        :raise FileEmitterException.
        """

        self._broker_front_url = broker_front_url
        self._loop = loop
        self._login = login
        self._password = password
        self._client = None
        self._token = None

        self.descriptors = {}

        for descriptor in descriptors:

            try:
                root = et.fromstring(descriptor)

                if root.tag == 'descriptor':
                    desc_elems = [root]
                else:
                    desc_elems = root.findall('descriptor')

                for desc_elem in desc_elems:

                    header = desc_elem.find('header')
                    name_elem = header.find('name')
                    name = name_elem.text
                    event_type_elem = header.find('eventtype')
                    event_type = event_type_elem.text
                    self.descriptors[name] = (desc_elem, event_type)

            except et.ParseError:
                raise FileEmitterException('Invalid descriptor')

    @asyncio.coroutine
    def login(self):
        """Log into the Xbus front-end.

        :raise FileEmitterException.
        """

        self._client = yield from rpc.connect_rpc(
            connect=self._broker_front_url, loop=self._loop
        )
        token = yield from self._client.call.login(self._login, self._password)
        if not token:
            raise FileEmitterException('Access error')
        self._token = token

    @asyncio.coroutine
    def send_files(self, files, encoding='utf-8'):
        """Send files into Xbus.

        :param files: List of (file descriptor, pyjon descriptor name) tuples.
        "pyjon_descriptor_name" parameters must refer to pyjon descriptors
        defined at the initialization of the class. They may be null, in which
        case the first defined pyjon descriptor will be used.
        :type files: List of tuples.

        :return: Envelope ID.

        :raise FileEmitterException.
        """

        envelope_id = yield from self._client.call.start_envelope(self._token)

        for file, desc_name in files:

            # Either use the specified descriptor or just pick the first one.
            if desc_name:
                desc_elem, event_type = self.descriptors[desc_name]
            else:
                desc_elem, event_type = next(iter(self.descriptors.values()))
            descriptor = pjdesc.Descriptor(desc_elem, encoding)

            try:
                yield from self.send_file(
                    envelope_id, event_type, file, descriptor
                )

            except pjdesc.exceptions.DescriptorError as e:
                raise FileEmitterException('%s - %s' % (type(e), e))

        yield from self._client.call.end_envelope(
            self._token, envelope_id
        )

        return envelope_id

    @asyncio.coroutine
    def send_file(self, envelope_id, event_type, data_file, descriptor):
        """Send a file into Xbus.

        :param descriptor: A pyjon descriptor.

        :raise FileEmitterException.
        """

        # TODO Get the amount of lines without reading the whole file?
        # num_lines = sum(1 for _ in data_file)
        num_lines = 0

        data_file.seek(0)
        data_iter = descriptor.read(data_file)
        event_id = yield from self._client.call.start_event(
            self._token, envelope_id, event_type, num_lines
        )
        if not event_id:
            raise FileEmitterException('Could not create a message.')
        for data_item in data_iter:
            data = {}
            for key, val in data_item.iteritems():
                if key == 'data_row__':
                    # Added by pyjon descriptor; ignore.
                    continue
                if isinstance(val, datetime.date):
                    data[key] = val.strftime('%Y-%m-%d')
                elif isinstance(val, datetime.time):
                    data[key] = val.strftime('%H:%M:%S')
                elif isinstance(val, Decimal):
                    data[key] = float(val)
                else:
                    data[key] = val
            yield from self._client.call.send_item(
                self._token, envelope_id, event_id,
                msgpack.packb(data, use_bin_type=True)
            )
        yield from self._client.call.end_event(
            self._token, envelope_id, event_id
        )
