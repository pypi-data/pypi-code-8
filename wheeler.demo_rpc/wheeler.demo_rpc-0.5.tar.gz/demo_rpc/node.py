import types
import pandas as pd
import numpy as np
from nadamq.NadaMq import cPacket, PACKET_TYPES
from arduino_rpc.proxy import ProxyBase
try:
    from google.protobuf.message import Message
    _translate = (lambda arg: arg.SerializeToString()
                  if isinstance(arg, Message) else arg)
except ImportError:
    _translate = lambda arg: arg



from base_node_rpc.proxy import ProxyBase, I2cProxyMixin



class Proxy(ProxyBase):


    _CMD_MICROSECONDS = 0x00;
    _CMD_MILLISECONDS = 0x01;
    _CMD_DELAY_US = 0x02;
    _CMD_DELAY_MS = 0x03;
    _CMD_RAM_FREE = 0x05;
    _CMD_PIN_MODE = 0x06;
    _CMD_DIGITAL_READ = 0x07;
    _CMD_DIGITAL_WRITE = 0x08;
    _CMD_ANALOG_READ = 0x09;
    _CMD_ANALOG_WRITE = 0x0a;
    _CMD_ARRAY_LENGTH = 0x0b;
    _CMD_ECHO_ARRAY = 0x0c;
    _CMD_STR_ECHO = 0x0d;
    _CMD_BASE_NODE_SOFTWARE_VERSION = 0x0e;
    _CMD_NAME = 0x0f;
    _CMD_MANUFACTURER = 0x10;
    _CMD_SOFTWARE_VERSION = 0x11;
    _CMD_URL = 0x12;
    _CMD_UPDATE_EEPROM_BLOCK = 0x20;
    _CMD_READ_EEPROM_BLOCK = 0x21;
    _CMD_I2C_ADDRESS = 0x41;
    _CMD_I2C_BUFFER_SIZE = 0x42;
    _CMD_I2C_SCAN = 0x43;
    _CMD_I2C_AVAILABLE = 0x44;
    _CMD_I2C_READ_BYTE = 0x45;
    _CMD_I2C_REQUEST_FROM = 0x46;
    _CMD_I2C_READ = 0x47;
    _CMD_I2C_WRITE = 0x48;
    _CMD_I2C_REQUEST = 0x60;
    _CMD_LOAD_CONFIG = 0x80;
    _CMD_SAVE_CONFIG = 0x81;
    _CMD_RESET_CONFIG = 0x82;
    _CMD_SERIALIZE_CONFIG = 0x83;
    _CMD_UPDATE_CONFIG = 0x84;
    _CMD_RESET_STATE = 0xa0;
    _CMD_SERIALIZE_STATE = 0xa1;
    _CMD_UPDATE_STATE = 0xa2;
    _CMD_GET_BUFFER = 0xc0;
    _CMD_BEGIN = 0xc1;
    _CMD_PACKET_CRC = 0xc2;
    _CMD_TEST_PARSER = 0xc3;
    _CMD_SET_I2C_ADDRESS = 0xc4;
    _CMD_SET_SERIAL_NUMBER = 0xc5;
    _CMD_SERIAL_NUMBER = 0xc6;
    _CMD_MAX_PAYLOAD_SIZE = 0xc7;
    _CMD_SIZEOF_NODE = 0xc8;
    _CMD_SIZEOF_CONFIG = 0xc9;
    _CMD_SIZEOF_STATE = 0xca;
    _CMD_SIZEOF_PARSER = 0xcb;
    _CMD_SIZEOF_PACKET_STRUCT = 0xcc;
    _CMD_SIZEOF_PACKET = 0xcd;
    _CMD_SIZEOF_SERIAL_HANDLER = 0xce;
    _CMD_SIZEOF_I2C_HANDLER = 0xcf;


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

        array = _translate(array)
        if isinstance(array, str):
            array = map(ord, array)
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

        array = _translate(array)
        if isinstance(array, str):
            array = map(ord, array)
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

        msg = _translate(msg)
        if isinstance(msg, str):
            msg = map(ord, msg)
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


    def base_node_software_version(self):
        command = np.dtype('uint8').type(self._CMD_BASE_NODE_SOFTWARE_VERSION)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


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


    def update_eeprom_block(self, address, data):
        command = np.dtype('uint8').type(self._CMD_UPDATE_EEPROM_BLOCK)
        ARG_STRUCT_SIZE = 6

        data = _translate(data)
        if isinstance(data, str):
            data = map(ord, data)
        # Argument is an array, so cast to appropriate array type.
        data = np.ascontiguousarray(data, dtype='uint8')
        array_info = pd.DataFrame([data.shape[0], ],
                                  index=['data', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([data.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(address, array_info.length['data'], ARG_STRUCT_SIZE + array_info.start['data'], )],
                               dtype=[('address', 'uint16'), ('data_length', 'uint16'), ('data_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def read_eeprom_block(self, address, n):
        command = np.dtype('uint8').type(self._CMD_READ_EEPROM_BLOCK)
        ARG_STRUCT_SIZE = 4
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(address, n, )],
                               dtype=[('address', 'uint16'), ('n', 'uint16'), ])
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

        result = np.fromstring(response.data(), dtype='uint8')

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

        data = _translate(data)
        if isinstance(data, str):
            data = map(ord, data)
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


    def i2c_request(self, address, data):
        command = np.dtype('uint8').type(self._CMD_I2C_REQUEST)
        ARG_STRUCT_SIZE = 5

        data = _translate(data)
        if isinstance(data, str):
            data = map(ord, data)
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

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def load_config(self):
        command = np.dtype('uint8').type(self._CMD_LOAD_CONFIG)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def save_config(self):
        command = np.dtype('uint8').type(self._CMD_SAVE_CONFIG)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def reset_config(self):
        command = np.dtype('uint8').type(self._CMD_RESET_CONFIG)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def serialize_config(self):
        command = np.dtype('uint8').type(self._CMD_SERIALIZE_CONFIG)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def update_config(self, serialized):
        command = np.dtype('uint8').type(self._CMD_UPDATE_CONFIG)
        ARG_STRUCT_SIZE = 4

        serialized = _translate(serialized)
        if isinstance(serialized, str):
            serialized = map(ord, serialized)
        # Argument is an array, so cast to appropriate array type.
        serialized = np.ascontiguousarray(serialized, dtype='uint8')
        array_info = pd.DataFrame([serialized.shape[0], ],
                                  index=['serialized', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([serialized.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(array_info.length['serialized'], ARG_STRUCT_SIZE + array_info.start['serialized'], )],
                               dtype=[('serialized_length', 'uint16'), ('serialized_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def reset_state(self):
        command = np.dtype('uint8').type(self._CMD_RESET_STATE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def serialize_state(self):
        command = np.dtype('uint8').type(self._CMD_SERIALIZE_STATE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def update_state(self, serialized):
        command = np.dtype('uint8').type(self._CMD_UPDATE_STATE)
        ARG_STRUCT_SIZE = 4

        serialized = _translate(serialized)
        if isinstance(serialized, str):
            serialized = map(ord, serialized)
        # Argument is an array, so cast to appropriate array type.
        serialized = np.ascontiguousarray(serialized, dtype='uint8')
        array_info = pd.DataFrame([serialized.shape[0], ],
                                  index=['serialized', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([serialized.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(array_info.length['serialized'], ARG_STRUCT_SIZE + array_info.start['serialized'], )],
                               dtype=[('serialized_length', 'uint16'), ('serialized_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def get_buffer(self):
        command = np.dtype('uint8').type(self._CMD_GET_BUFFER)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def begin(self):
        command = np.dtype('uint8').type(self._CMD_BEGIN)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def packet_crc(self, data):
        command = np.dtype('uint8').type(self._CMD_PACKET_CRC)
        ARG_STRUCT_SIZE = 4

        data = _translate(data)
        if isinstance(data, str):
            data = map(ord, data)
        # Argument is an array, so cast to appropriate array type.
        data = np.ascontiguousarray(data, dtype='uint8')
        array_info = pd.DataFrame([data.shape[0], ],
                                  index=['data', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([data.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(array_info.length['data'], ARG_STRUCT_SIZE + array_info.start['data'], )],
                               dtype=[('data_length', 'uint16'), ('data_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint16')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def test_parser(self, data):
        command = np.dtype('uint8').type(self._CMD_TEST_PARSER)
        ARG_STRUCT_SIZE = 4

        data = _translate(data)
        if isinstance(data, str):
            data = map(ord, data)
        # Argument is an array, so cast to appropriate array type.
        data = np.ascontiguousarray(data, dtype='uint8')
        array_info = pd.DataFrame([data.shape[0], ],
                                  index=['data', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([data.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(array_info.length['data'], ARG_STRUCT_SIZE + array_info.start['data'], )],
                               dtype=[('data_length', 'uint16'), ('data_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def set_i2c_address(self, value):
        command = np.dtype('uint8').type(self._CMD_SET_I2C_ADDRESS)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(value, )],
                               dtype=[('value', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def set_serial_number(self, value):
        command = np.dtype('uint8').type(self._CMD_SET_SERIAL_NUMBER)
        ARG_STRUCT_SIZE = 4
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(value, )],
                               dtype=[('value', 'uint32'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def serial_number(self):
        command = np.dtype('uint8').type(self._CMD_SERIAL_NUMBER)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


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


    def sizeof_node(self):
        command = np.dtype('uint8').type(self._CMD_SIZEOF_NODE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def sizeof_config(self):
        command = np.dtype('uint8').type(self._CMD_SIZEOF_CONFIG)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def sizeof_state(self):
        command = np.dtype('uint8').type(self._CMD_SIZEOF_STATE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def sizeof_parser(self):
        command = np.dtype('uint8').type(self._CMD_SIZEOF_PARSER)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def sizeof_packet_struct(self):
        command = np.dtype('uint8').type(self._CMD_SIZEOF_PACKET_STRUCT)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def sizeof_packet(self):
        command = np.dtype('uint8').type(self._CMD_SIZEOF_PACKET)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def sizeof_serial_handler(self):
        command = np.dtype('uint8').type(self._CMD_SIZEOF_SERIAL_HANDLER)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def sizeof_i2c_handler(self):
        command = np.dtype('uint8').type(self._CMD_SIZEOF_I2C_HANDLER)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]







class I2cProxy(I2cProxyMixin, Proxy):
    pass


