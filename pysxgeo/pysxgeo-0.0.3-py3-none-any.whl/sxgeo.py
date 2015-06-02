from struct import unpack
from binascii import hexlify
from socket import inet_aton, error
from math import floor
from datetime import datetime

from pysxgeo import opts

SXGEO_FILE, SXGEO_MEMORY, SXGEO_BATCH = 0, 1, 2

class SxGeo:

    def __init__(self, db_file, mode=SXGEO_FILE):
        '''
        :param db_file: path to db file
        :param mode: processing mode
        '''

        self._fh = open(db_file, 'rb')
        header = self._fh.read(40)

        if header[:3] != b'SxG':
            raise IOError('Can`t open {0}'.format(db_file))

        info = dict(zip(opts.INFO_FIELDS,
                        unpack(opts.INFO_FMT, header[3:])))

        if(info['b_idx_len'] * info['m_idx_len'] * info['range'] *
           info['db_items'] * info['time'] * info['id_len'] == 0):
            raise IOError('Wrong file format {0}'.format(db_file))

        self.range = info['range']
        self.b_idx_len = info['b_idx_len']
        self.m_idx_len = info['m_idx_len']
        self.db_items = info['db_items']
        self.id_len = info['id_len']
        self.max_region = info['max_region']
        self.max_city = info['max_city']
        self.max_country = info['max_country']
        self.country_size = info['country_size']

        self.block_len = 3 + self.id_len
        self.batch_mode = mode & SXGEO_BATCH
        self.memory_mode = mode & SXGEO_MEMORY

        if info['pack_size']:
            self.pack = self._fh.read(info['pack_size']).split(b'\0')
        else:
            self.pack = ''

        self.b_idx_str = self._fh.read(self.b_idx_len * 4)
        self.m_idx_str = self._fh.read(self.m_idx_len * 4)

        self.db_begin = self._fh.tell()

        if self.batch_mode:
            self.b_idx_arr = unpack('>{0:d}L'.format(self.b_idx_len), self.b_idx_str)
            del self.b_idx_str
            self.m_idx_arr = [self.m_idx_str[i:i + 4] for i in range(0, len(self.m_idx_str), 4)]
            del self.m_idx_str

        if self.memory_mode:
            self.db = self._fh.read(self.db_items * self.block_len)
            self.db_regions = self._fh.read(info['region_size']) if info['region_size'] else ''
            self.db_cities = self._fh.read(info['city_size']) if info['city_size'] else ''
            self._fh.close()

        info['regions_begin'] = self.db_begin + self.db_items * self.block_len
        info['cities_begin'] = info['regions_begin'] + info['region_size']

        self.charset = opts.CHARSET[info['charset']]
        self.info = info
        self.__coords = None

    def __search_idx(self, ipn, _min, _max):
        if self.batch_mode:
            piece = lambda x: self.m_idx_arr[x]
        else:
            piece = lambda x: self.m_idx_str[x*4:x*4+4]

        while _max - _min > 8:
            offset = (_min + _max) >> 1
            if ipn > piece(offset):
                _min = offset
            else:
                _max = offset

        while ipn > piece(_min):
            _min += 1
            if not _min < _max:
                break

        return _min

    def __search_db(self, _str, ipn, _min, _max):
        if _max - _min > 1:
            ipn = ipn[1:]
            piece = lambda x: _str[x*self.block_len: x*self.block_len+3]
            while _max - _min > 8:
                offset = (_min + _max) >> 1

                if ipn > piece(offset):
                    _min = offset
                else:
                    _max = offset

            while ipn >= piece(_min):
                _min += 1
                if not _min < _max:
                    break
        else:
            _min += 1

        sliced = _str[_min * self.block_len - self.id_len: _min * self.block_len]
        return int(hexlify(sliced), 16)

    def get_num(self, ip):
        try:
            ipn = inet_aton(ip)
        except error:
            return False

        ip1n = int(ip.split('.')[0])
        if ip1n in (0, 10, 127) or ip1n >= self.b_idx_len:
            return False

        if self.batch_mode:
            t = (self.b_idx_arr[ip1n-1], self.b_idx_arr[ip1n])
        else:
            start = (ip1n-1) * 4
            t = unpack('>II', self.b_idx_str[start:start + 8])

        blocks = dict(zip(('min', 'max'), t))

        if blocks['max'] - blocks['min'] > self.range:
            part = self.__search_idx(ipn, floor(blocks['min'] / self.range),
                                     floor(blocks['max'] / self.range))
            _min = part * self.range if part > 0 else 0
            _max = self.db_items if part > self.m_idx_len else (part + 1) * self.range

            if _min < blocks['min']:
                _min = blocks['min']

            if _max > blocks['max']:
                _max = blocks['max']

        else:
            _min = blocks['min']
            _max = blocks['max']

        if self.memory_mode:
            return self.__search_db(self.db, ipn, _min, _max)
        else:
            self._fh.seek(self.db_begin + _min * self.block_len)
            length = _max - _min
            return self.__search_db(self._fh.read(length * self.block_len),
                                    ipn, 0, length - 1)

    def __read_data(self, seek, _max, _type):
        raw = ''
        if seek and _max:
            if self.memory_mode:
                db = self.db_regions if _type == 1 else self.db_cities
                raw = db[seek: seek+_max]
            else:
                k = 'regions_begin' if _type == 1 else 'cities_begin'
                self._fh.seek(self.info[k] + seek)
                raw = self._fh.read(_max)
        return self.__unpack(self.pack[_type], raw)

    def __parse_city(self, seek, full=False):

        if not self.pack:
            return False

        only_country = False

        if seek < self.country_size:
            country = self.__read_data(seek, self.max_country, 0)
            city = self.__unpack(self.pack[2])
            city['lat'] = country['lat']
            city['lon'] = country['lon']
            only_country = True
        else:
            city = self.__read_data(seek, self.max_city, 2)
            country = {'id': city['country_id'],
                       'iso': opts.ID2ISO[city['country_id']]}
            del city['country_id']

        self.__coords = city['lat'], city['lon']

        if full:
            region = self.__read_data(city['region_seek'], self.max_region, 1)
            if not only_country:
                country = self.__read_data(region['country_seek'], self.max_country, 0)
            del city['region_seek'], region['country_seek']
            return {'city': city, 'region': region, 'country': country}
        else:
            del city['region_seek']
            return {'city': city, 'country': {'id': country['id'], 'iso': country['iso']}}

    def __unpack(self, pack, item=''):
        unpacked = {}
        pos = 0

        l_dict = {
            't': 1, 'T': 1, 'n': 2, 's': 2,
            'S': 2, 'm': 3, 'M': 3, 'd': 8,
        }
        v_dict ={
            't': lambda v: unpack('b', v),
            'T': lambda v: unpack('B', v),
            's': lambda v: unpack('h', v),
            'S': lambda v: unpack('H', v),
            'm': lambda v: unpack('i', v + (b'\xff' if ord(v[2]) >> 7 else b'\0')),
            'M': lambda v: unpack('I', v + b'\0'),  # l & L in PHP and Python do not match
            'i': lambda v: unpack('i', v),
            'I': lambda v: unpack('I', v),
            'f': lambda v: unpack('f', v),
            'd': lambda v: unpack('d', v),
            'n': lambda v: unpack('h', v)[0] / pow(10, int(chr(_type[1]))),
            'N': lambda v: unpack('i', v)[0] / pow(10, int(chr(_type[1]))),
            'c': lambda v: v.decode('utf-8').rstrip(' '),
        }
        for p in pack.split(b'/'):
            _type, name = p.split(b':')
            name = name.decode('utf-8')
            _type0 = chr(_type[0])
            if not item:
                unpacked[name] = '' if _type0 == 'b' or _type0 == 'c' else 0
                continue

            if _type0 == 'c':
                l = int(_type[1:])
            elif _type0 == 'b':
                l = item.find(b'\0', pos) - pos
            else:
                l = l_dict.get(_type0, 4)

            val = item[pos:pos+l]

            v = v_dict.get(_type0)

            if _type0 == 'b':
                v = val
                l += 1
            else:
                v = v(val)

            try:
                v = v.decode('utf-8')
            except AttributeError:
                pass

            pos += l
            unpacked[name] = v[0] if isinstance(v, tuple) else v
        return unpacked

    def get(self, ip):
        return self.get_city(ip) if self.max_city else self.get_country(ip)

    def get_country(self, ip):
        if self.max_city:
            tmp = self.__parse_city(self.get_num(ip))
            return tmp['country']['iso']
        else:
            return opts.ID2ISO[self.get_num(ip)]

    def get_country_id(self, ip):
        if self.max_city:
            tmp = self.__parse_city(self.get_num(ip))
            return tmp['country']['id']
        else:
            return self.get_num(ip)

    def get_city(self, ip, full=False):
        seek = self.get_num(ip)
        return self.__parse_city(seek, full) if seek else False

    def get_coords(self, ip=None):
        if self.__coords is not None:
            return self.__coords

        elif ip is not None:
            if self.get_city(ip):
                return self.__coords

        return False

    def about(self):

        return {
            'Created': datetime.fromtimestamp(self.info['time']),
            'Timestamp': self.info['time'],
            'Charset': self.charset,
            'Type': opts.TYPES[self.info['type']],
            'Byte Index': self.b_idx_len,
            'Main Index': self.m_idx_len,
            'Blocks In Index Item': self.range,
            'IP Blocks': self.db_items,
            'Block Size': self.block_len,
            'City': {
                'Max Length': self.max_city,
                'Total Size': self.info['city_size']
            },
            'Region': {
                'Max Length': self.max_region,
                'Total Size': self.info['region_size']
            },
            'Country': {
                'Max Length': self.max_country,
                'Total Size': self.info['country_size']
            }
        }

    def __del__(self):
        if not self._fh.closed:
            self._fh.close()
