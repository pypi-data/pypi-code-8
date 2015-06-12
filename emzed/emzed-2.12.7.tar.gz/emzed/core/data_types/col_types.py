import hashlib
import datetime

import numpy


def unique_id_from(*args):
    h = hashlib.sha256()
    for arg in args:
        h.update(arg)
    return h.hexdigest()


class Blob(object):

    def __init__(self, data, type_=None):
        self.data = data
        self.unique_id = None
        if type_ is None:
            if data.startswith("\x89PNG"):
                type_ = "PNG"
            elif data[0] == "\xff":
                hex_header = "ff d8 ff e0 00 10 4a 46 49 46 00 01"
                jpg_soi_marker = "".join(chr(int(f, 16) for f in hex_header.split()))
                if jpg_soi_marker in data:
                    type_ = "JPG"
            elif data.startswith("emzed_version=2."):
                type_ = "TABLE"
            elif data.startswith("<?xml version=\""):
                type_ = "XML"
        self.type_ = type_

    def __str__(self):
        type_ = "unknown type" if self.type_ is None else "type %s" % self.type_
        return "<Blob %#x of %s>" % (id(self), type_)

    def uniqueId(self):
        if self.unique_id is None:
            self.unique_id = unique_id_from(self.data)
        return self.unique_id


class TimeSeries(object):

    def __init__(self, values, time_stamps=None):
        self.formatter = self._to_str_formatter
        if time_stamps is not None:
            assert len(values) == len(time_stamps)
            type_ = None
            if all(isinstance(ts, datetime.datetime) for ts in time_stamps):
                type_ = datetime.datetime
                if all(ts.resolution == datetime.timedelta(0, 0, 1) for ts in time_stamps):
                    self.formatter = self._date_formatter
                time_stamps = numpy.array(time_stamps, dtype="datetime64[us]")

            elif all(isinstance(ts, int) for ts in time_stamps):
                type_ = int
                time_stamps = numpy.array(time_stamps, dtype=numpy.int64)
            elif all(isinstance(ts, basestring) for ts in time_stamps):
                type_ = basestring
            else:
                t = set(type(ts) for ts in time_stamps)
                raise Exception("can not handle type(s) %s for time_stamps argument" % t)
        else:
            time_stamps = range(len(values))
            type_ = long

        self.type_ = type_

        self.time_stamps = time_stamps
        self.values = numpy.array(values)
        self.unique_id = None

    @staticmethod
    def _date_formatter(ts):
        return str(ts)[:11]

    @staticmethod
    def _to_str_formatter(ts):
        return str(ts)

    def __str__(self):
        min_v = min(self.values)
        max_v = max(self.values)
        min_ts = min(self.time_stamps)
        max_ts = max(self.time_stamps)

        return "<TimeSeries, time=%s..%s, values=%s..%s>" % (min_ts, max_ts, min_v, max_v)

    def uniqueId(self):
        if self.unique_id is None:
            if self.type_ is basestring:
                t_axis_data = self.time_stamps
            else:
                t_axis_data = (str(self.time_stamps.data),)
            self.unique_id = unique_id_from(str(self.type_), self.values.data, *t_axis_data)
        return self.unique_id

    def time_stamps_as_strings(self):
        return [self.formatter(ts) for ts in self.time_stamps]
