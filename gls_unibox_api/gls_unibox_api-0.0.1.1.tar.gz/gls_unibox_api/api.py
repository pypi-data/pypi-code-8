# -*- coding: utf-8 -*-
import inspect
import socket
import logging

logger = logging.getLogger('gls_unibox_api')


from . import fields
from .tags import StartTag, EndTag


class SoftwareInformation(fields.FieldGroup):
    "Software info"
    name = fields.Char('T050', length=20)
    version = fields.Char('T051', length=20)

    def __init__(self, *args, **kwargs):
        super(SoftwareInformation, self).__init__(*args, **kwargs)

        self.values = {}


class ServiceData(fields.FieldGroup):
    """
    Service Data Element
    """
    national_product = fields.Char('T200', length=3)
    # future fields.Char('T201', length=2)
    # future fields.Char('T202', length=2)
    cash_service = fields.Char('T203', length=2)
    express = fields.Char('T204', length=2)
    weight = fields.Char('T205', length=2)
    product_flag = fields.Char('T206', length=3)
    service_flag = fields.Char('T207', length=3)
    incoterms = fields.Int('T210', length=2)

    def __init__(self, *args, **kwargs):
        super(ServiceData, self).__init__(*args, **kwargs)

        self.values = {}


class PickUpAddress(fields.FieldGroup):
    """
    A pick up address Element
    """
    name = fields.Char('T900', length=50)
    name2 = fields.Char('T901', length=50)
    name3 = fields.Char('T902', length=50)
    street = fields.Char('T903', length=50)
    country = fields.Char('T904', length=2)
    zip = fields.Char('T905', length=10)
    place = fields.Char('T906', length=50)
    phone = fields.Char('T907', length=15)

    def __init__(self, *args, **kwargs):
        super(PickUpAddress, self).__init__(*args, **kwargs)

        self.values = {}


class PickUp(fields.FieldGroup):
    date = fields.Date('T908', separator='.')

    def __init__(self, *args, **kwargs):
        super(PickUp, self).__init__(*args, **kwargs)

        self.values = {}


class Consignor(fields.FieldGroup):
    "Consignor/Shipper"
    customer_number = fields.Long('T805', length=10)
    salutation = fields.Char('T809', length=50)
    name = fields.Char('T810', length=50)
    name2 = fields.Char('T811', length=50)
    name3 = fields.Char('T812', length=50)
    street = fields.Char('T820', length=50)
    country = fields.Char('T821', length=2)
    zip = fields.Char('T822', length=10)
    consignor = fields.Char('T823', length=50)
    place = fields.Char('T864', length=30)

    label = fields.Char('T850')

    def __init__(self, *args, **kwargs):
        super(Consignor, self).__init__(*args, **kwargs)

        self.values = {}


class Consignee(fields.FieldGroup):
    """
    A Structure representing an address
    """
    customer_number_label = fields.Char('T851', length=25)
    customer_number = fields.Long('T852', length=10)

    id_type = fields.Char('T853', length=25)
    id_value = fields.Char('T854', length=25)

    salutation = fields.Char('T859', length=50)
    name = fields.Char('T860', length=40)
    name2 = fields.Char('T861', length=40)
    name3 = fields.Char('T862', length=40)
    street = fields.Char('T863', length=50)
    place = fields.Char('T864', length=30)

    # Defined out of range
    zip = fields.Char('T330', length=10)
    country = fields.Char('T100', length=2)

    def __init__(self, *args, **kwargs):
        super(Consignee, self).__init__(*args, **kwargs)

        self.values = {}


class Client(object):
    """
    GLS Unibox connection API
    """

    def __init__(self, server, port, test=False):
        self.server = server
        self.port = int(port)
        self.test = test

    def get_socket_conn(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.server, self.port))
        return s

    def request(self, tags):
        values = (StartTag.code + '|'.join(tags) + '|' + EndTag.code)
        logger.debug('Request::values::%s', values)

        s = self.get_socket_conn()
        s.sendall(values)

        response = ''
        while True:
            data = s.recv(1024)
            response += data
            if not data:
                break

        s.close()

        logger.debug('Response::values::%s', response)

        return response


class CommonMixin(object):
    """
    Mixin with fields common to all requests
    """
    software = SoftwareInformation()
    location = fields.Char('T8700', length=6)

    #: Special functions have the following possibilities
    #:
    #: * NOPRINT - Parcel data is returned through the stream
    #: * NOSAVE - For prechecking or testing, where neither the storing or
    #:   printing of the label happens.
    special_functions = fields.MultipleChoice('T090')


class ShipmentMixin(object):
    """
    Mixin with fields specific to the shipment
    """
    parcel_number = fields.Char('T400')

    epl_depot_number = fields.Char('T101')
    hub = fields.Char('T110')
    bar_code = fields.Long('T300')
    sorting_flag = fields.Int('T310')

    last_routing_update = fields.Date('T520')
    parcel_weight = fields.Decimal('T530')
    shipping_date = fields.Date('T545', separator='.')

    consignee = Consignee()
    consignor = Consignor()
    pick_up_address = PickUpAddress()

    # XXX: Not sure exactly what this is
    parcel = fields.Int('T8904')
    quantity = fields.Int('T8905')

    gls_contract = fields.Char('T8914', length=10)
    gls_customer_id = fields.Long('T8915', length=10)


class Shipment(ShipmentMixin, CommonMixin):
    """
    Return an instance of the shipment class
    """
    def __init__(self, client):

        self.client = client

        # Initialize the values holder
        self.values = {}

        if self.client.test:
            self.special_functions = ['NOSAVE']

    def get_tags(self):
        """
        Returns all the tags (with their messages) as a list
        """
        tags = []

        def field_predicate(object):
            if object is None:
                return
            return isinstance(object, fields.BaseField)

        def field_group_predicate(object):
            if object is None:
                return
            return isinstance(object, fields.FieldGroup)

        def collect_tags(obj):
            for name, field in inspect.getmembers(
                    obj.__class__, field_predicate):
                value = getattr(obj, name)
                if value is None:
                    continue
                tags.append(':'.join((field.code, field.to_string(value))))

        # Collect the tags from fields in class
        collect_tags(self)

        # Collect the tags from fields in field groups
        for name, field_group in inspect.getmembers(
                self.__class__, field_group_predicate):
            field_group = getattr(self, name)
            collect_tags(field_group)

        return tags

    def create_label(self):
        """
        Tries to create a label on the GLS Unibox and returns a response
        """
        return self.client.request(self.get_tags())


class Response(ShipmentMixin, CommonMixin):
    """
    A response object received from GLS
    """
    def __init__(self, values):
        self.values = values

    @classmethod
    def parse(cls, string):
        """
        Parse the response.
        """
        values = {}

        for pair in string.replace(
                StartTag.code, '').replace(EndTag.code, '').split('|'):
            if ':' not in pair:
                continue
            tag, value = pair.split(':', 1)
            values[tag] = value

        return cls(values)
