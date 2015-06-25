import pandas as pd
import numpy as np
from nadamq.NadaMq import cPacket, PACKET_TYPES
from arduino_rpc.proxy import ProxyBase



from base_node_rpc.proxy import ProxyBase, I2cProxyMixin, I2cSoftProxyMixin



class Proxy(ProxyBase):


    _CMD_MICROSECONDS = 0x00;
    _CMD_MILLISECONDS = 0x01;
    _CMD_DELAY_US = 0x02;
    _CMD_DELAY_MS = 0x03;
    _CMD_MAX_PAYLOAD_SIZE = 0x04;
    _CMD_RAM_FREE = 0x05;
    _CMD_PIN_MODE = 0x06;
    _CMD_DIGITAL_READ = 0x07;
    _CMD_DIGITAL_WRITE = 0x08;
    _CMD_ANALOG_READ = 0x09;
    _CMD_ANALOG_WRITE = 0x0a;
    _CMD_ARRAY_LENGTH = 0x0b;
    _CMD_ECHO_ARRAY = 0x0c;
    _CMD_STR_ECHO = 0x0d;
    _CMD_I2C_ADDRESS = 0x0e;
    _CMD_SET_I2C_ADDRESS = 0x0f;
    _CMD_I2C_BUFFER_SIZE = 0x10;
    _CMD_I2C_SCAN = 0x11;
    _CMD_I2C_AVAILABLE = 0x12;
    _CMD_I2C_READ_BYTE = 0x13;
    _CMD_I2C_REQUEST_FROM = 0x14;
    _CMD_I2C_READ = 0x15;
    _CMD_I2C_WRITE = 0x16;
    _CMD_I2C_SEND_COMMAND = 0x17;
    _CMD_I2C_COMMAND_READ = 0x18;
    _CMD_SET_SPI_BIT_ORDER = 0x19;
    _CMD_SET_SPI_CLOCK_DIVIDER = 0x1a;
    _CMD_SET_SPI_DATA_MODE = 0x1b;
    _CMD_SPI_TRANSFER = 0x1c;
    _CMD_NAME = 0x1d;
    _CMD_MANUFACTURER = 0x1e;
    _CMD_SOFTWARE_VERSION = 0x1f;
    _CMD_URL = 0x20;
    _CMD_TEST_METHOD = 0x30;


    def microseconds(self):
        command = np.dtype('uint8').type(self._CMD_MICROSECONDS)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def milliseconds(self):
        command = np.dtype('uint8').type(self._CMD_MILLISECONDS)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def delay_us(self, us):
        command = np.dtype('uint8').type(self._CMD_DELAY_US)
        ARG_STRUCT_SIZE = 2
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(us, )],
                               dtype=[('us', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def delay_ms(self, ms):
        command = np.dtype('uint8').type(self._CMD_DELAY_MS)
        ARG_STRUCT_SIZE = 2
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(ms, )],
                               dtype=[('ms', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def max_payload_size(self):
        command = np.dtype('uint8').type(self._CMD_MAX_PAYLOAD_SIZE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def ram_free(self):
        command = np.dtype('uint8').type(self._CMD_RAM_FREE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def pin_mode(self, pin, mode):
        command = np.dtype('uint8').type(self._CMD_PIN_MODE)
        ARG_STRUCT_SIZE = 2
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(pin, mode, )],
                               dtype=[('pin', 'uint8'), ('mode', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def digital_read(self, pin):
        command = np.dtype('uint8').type(self._CMD_DIGITAL_READ)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(pin, )],
                               dtype=[('pin', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def digital_write(self, pin, value):
        command = np.dtype('uint8').type(self._CMD_DIGITAL_WRITE)
        ARG_STRUCT_SIZE = 2
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(pin, value, )],
                               dtype=[('pin', 'uint8'), ('value', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def analog_read(self, pin):
        command = np.dtype('uint8').type(self._CMD_ANALOG_READ)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(pin, )],
                               dtype=[('pin', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint16')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def analog_write(self, pin, value):
        command = np.dtype('uint8').type(self._CMD_ANALOG_WRITE)
        ARG_STRUCT_SIZE = 2
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(pin, value, )],
                               dtype=[('pin', 'uint8'), ('value', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def array_length(self, array):
        command = np.dtype('uint8').type(self._CMD_ARRAY_LENGTH)
        ARG_STRUCT_SIZE = 4

        # Argument is an array, so cast to appropriate array type.
        array = np.ascontiguousarray(array, dtype='uint8')
        array_info = pd.DataFrame([array.shape[0], ],
                                  index=['array', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([array.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(array_info.length['array'], ARG_STRUCT_SIZE + array_info.start['array'], )],
                               dtype=[('array_length', 'uint16'), ('array_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint16')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def echo_array(self, array):
        command = np.dtype('uint8').type(self._CMD_ECHO_ARRAY)
        ARG_STRUCT_SIZE = 4

        # Argument is an array, so cast to appropriate array type.
        array = np.ascontiguousarray(array, dtype='uint32')
        array_info = pd.DataFrame([array.shape[0], ],
                                  index=['array', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([array.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(array_info.length['array'], ARG_STRUCT_SIZE + array_info.start['array'], )],
                               dtype=[('array_length', 'uint16'), ('array_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is an array, so return entire array.
        return result


    def str_echo(self, msg):
        command = np.dtype('uint8').type(self._CMD_STR_ECHO)
        ARG_STRUCT_SIZE = 4

        # Argument is an array, so cast to appropriate array type.
        msg = np.ascontiguousarray(msg, dtype='uint8')
        array_info = pd.DataFrame([msg.shape[0], ],
                                  index=['msg', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([msg.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(array_info.length['msg'], ARG_STRUCT_SIZE + array_info.start['msg'], )],
                               dtype=[('msg_length', 'uint16'), ('msg_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def i2c_address(self):
        command = np.dtype('uint8').type(self._CMD_I2C_ADDRESS)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='int32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def set_i2c_address(self, address):
        command = np.dtype('uint8').type(self._CMD_SET_I2C_ADDRESS)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(address, )],
                               dtype=[('address', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='int32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def i2c_buffer_size(self):
        command = np.dtype('uint8').type(self._CMD_I2C_BUFFER_SIZE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint16')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def i2c_scan(self):
        command = np.dtype('uint8').type(self._CMD_I2C_SCAN)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def i2c_available(self):
        command = np.dtype('uint8').type(self._CMD_I2C_AVAILABLE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='int16')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def i2c_read_byte(self):
        command = np.dtype('uint8').type(self._CMD_I2C_READ_BYTE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='int8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def i2c_request_from(self, address, n_bytes_to_read):
        command = np.dtype('uint8').type(self._CMD_I2C_REQUEST_FROM)
        ARG_STRUCT_SIZE = 2
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(address, n_bytes_to_read, )],
                               dtype=[('address', 'uint8'), ('n_bytes_to_read', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='int8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def i2c_read(self, address, n_bytes_to_read):
        command = np.dtype('uint8').type(self._CMD_I2C_READ)
        ARG_STRUCT_SIZE = 2
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(address, n_bytes_to_read, )],
                               dtype=[('address', 'uint8'), ('n_bytes_to_read', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def i2c_write(self, address, data):
        command = np.dtype('uint8').type(self._CMD_I2C_WRITE)
        ARG_STRUCT_SIZE = 5

        # Argument is an array, so cast to appropriate array type.
        data = np.ascontiguousarray(data, dtype='uint8')
        array_info = pd.DataFrame([data.shape[0], ],
                                  index=['data', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([data.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(address, array_info.length['data'], ARG_STRUCT_SIZE + array_info.start['data'], )],
                               dtype=[('address', 'uint8'), ('data_length', 'uint16'), ('data_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def i2c_send_command(self, address, payload):
        command = np.dtype('uint8').type(self._CMD_I2C_SEND_COMMAND)
        ARG_STRUCT_SIZE = 5

        # Argument is an array, so cast to appropriate array type.
        payload = np.ascontiguousarray(payload, dtype='uint8')
        array_info = pd.DataFrame([payload.shape[0], ],
                                  index=['payload', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([payload.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(address, array_info.length['payload'], ARG_STRUCT_SIZE + array_info.start['payload'], )],
                               dtype=[('address', 'uint8'), ('payload_length', 'uint16'), ('payload_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def i2c_command_read(self, address):
        command = np.dtype('uint8').type(self._CMD_I2C_COMMAND_READ)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(address, )],
                               dtype=[('address', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def set_spi_bit_order(self, order):
        command = np.dtype('uint8').type(self._CMD_SET_SPI_BIT_ORDER)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(order, )],
                               dtype=[('order', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def set_spi_clock_divider(self, divider):
        command = np.dtype('uint8').type(self._CMD_SET_SPI_CLOCK_DIVIDER)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(divider, )],
                               dtype=[('divider', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def set_spi_data_mode(self, mode):
        command = np.dtype('uint8').type(self._CMD_SET_SPI_DATA_MODE)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(mode, )],
                               dtype=[('mode', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def spi_transfer(self, value):
        command = np.dtype('uint8').type(self._CMD_SPI_TRANSFER)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(value, )],
                               dtype=[('value', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def name(self):
        command = np.dtype('uint8').type(self._CMD_NAME)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def manufacturer(self):
        command = np.dtype('uint8').type(self._CMD_MANUFACTURER)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def software_version(self):
        command = np.dtype('uint8').type(self._CMD_SOFTWARE_VERSION)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def url(self):
        command = np.dtype('uint8').type(self._CMD_URL)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def test_method(self):
        command = np.dtype('uint8').type(self._CMD_TEST_METHOD)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='int32')

        # Return type is a scalar, so return first entry in array.
        return result[0]







class I2cProxy(I2cProxyMixin, Proxy):
    pass


class I2cSoftProxy(I2cSoftProxyMixin, Proxy):
    pass

