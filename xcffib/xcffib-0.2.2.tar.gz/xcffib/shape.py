import xcffib
import struct
import six
MAJOR_VERSION = 1
MINOR_VERSION = 1
key = xcffib.ExtensionKey("SHAPE")
_events = {}
_errors = {}
from . import xproto
class SO:
    Set = 0
    Union = 1
    Intersect = 2
    Subtract = 3
    Invert = 4
class SK:
    Bounding = 0
    Clip = 1
    Input = 2
class NotifyEvent(xcffib.Event):
    def __init__(self, unpacker):
        xcffib.Event.__init__(self, unpacker)
        base = unpacker.offset
        self.shape_kind, self.affected_window, self.extents_x, self.extents_y, self.extents_width, self.extents_height, self.server_time, self.shaped = unpacker.unpack("xB2xIhhHHIB11x")
        self.bufsize = unpacker.offset - base
    def pack(self):
        buf = six.BytesIO()
        buf.write(struct.pack("=B", 0))
        buf.write(struct.pack("=B2xIhhHHIB11x", self.shape_kind, self.affected_window, self.extents_x, self.extents_y, self.extents_width, self.extents_height, self.server_time, self.shaped))
        buf_len = len(buf.getvalue())
        if buf_len < 32:
            buf.write(struct.pack("x" * (32 - buf_len)))
        return buf.getvalue()
_events[0] = NotifyEvent
class QueryVersionReply(xcffib.Reply):
    def __init__(self, unpacker):
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.major_version, self.minor_version = unpacker.unpack("xx2x4xHH")
        self.bufsize = unpacker.offset - base
class QueryVersionCookie(xcffib.Cookie):
    reply_type = QueryVersionReply
class QueryExtentsReply(xcffib.Reply):
    def __init__(self, unpacker):
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.bounding_shaped, self.clip_shaped, self.bounding_shape_extents_x, self.bounding_shape_extents_y, self.bounding_shape_extents_width, self.bounding_shape_extents_height, self.clip_shape_extents_x, self.clip_shape_extents_y, self.clip_shape_extents_width, self.clip_shape_extents_height = unpacker.unpack("xx2x4xBB2xhhHHhhHH")
        self.bufsize = unpacker.offset - base
class QueryExtentsCookie(xcffib.Cookie):
    reply_type = QueryExtentsReply
class InputSelectedReply(xcffib.Reply):
    def __init__(self, unpacker):
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.enabled, = unpacker.unpack("xB2x4x")
        self.bufsize = unpacker.offset - base
class InputSelectedCookie(xcffib.Cookie):
    reply_type = InputSelectedReply
class GetRectanglesReply(xcffib.Reply):
    def __init__(self, unpacker):
        xcffib.Reply.__init__(self, unpacker)
        base = unpacker.offset
        self.ordering, self.rectangles_len = unpacker.unpack("xB2x4xI20x")
        self.rectangles = xcffib.List(unpacker, xproto.RECTANGLE, self.rectangles_len)
        self.bufsize = unpacker.offset - base
class GetRectanglesCookie(xcffib.Cookie):
    reply_type = GetRectanglesReply
class shapeExtension(xcffib.Extension):
    def QueryVersion(self, is_checked=True):
        buf = six.BytesIO()
        buf.write(struct.pack("=xx2x"))
        return self.send_request(0, buf, QueryVersionCookie, is_checked=is_checked)
    def Rectangles(self, operation, destination_kind, ordering, destination_window, x_offset, y_offset, rectangles, is_checked=False):
        buf = six.BytesIO()
        buf.write(struct.pack("=xB2xBBxIhh", operation, destination_kind, ordering, destination_window, x_offset, y_offset))
        buf.write(xcffib.pack_list(rectangles, xproto.RECTANGLE))
        return self.send_request(1, buf, is_checked=is_checked)
    def Mask(self, operation, destination_kind, destination_window, x_offset, y_offset, source_bitmap, is_checked=False):
        buf = six.BytesIO()
        buf.write(struct.pack("=xB2xB2xIhhI", operation, destination_kind, destination_window, x_offset, y_offset, source_bitmap))
        return self.send_request(2, buf, is_checked=is_checked)
    def Combine(self, operation, destination_kind, source_kind, destination_window, x_offset, y_offset, source_window, is_checked=False):
        buf = six.BytesIO()
        buf.write(struct.pack("=xB2xBBxIhhI", operation, destination_kind, source_kind, destination_window, x_offset, y_offset, source_window))
        return self.send_request(3, buf, is_checked=is_checked)
    def Offset(self, destination_kind, destination_window, x_offset, y_offset, is_checked=False):
        buf = six.BytesIO()
        buf.write(struct.pack("=xB2x3xIhh", destination_kind, destination_window, x_offset, y_offset))
        return self.send_request(4, buf, is_checked=is_checked)
    def QueryExtents(self, destination_window, is_checked=True):
        buf = six.BytesIO()
        buf.write(struct.pack("=xx2xI", destination_window))
        return self.send_request(5, buf, QueryExtentsCookie, is_checked=is_checked)
    def SelectInput(self, destination_window, enable, is_checked=False):
        buf = six.BytesIO()
        buf.write(struct.pack("=xx2xIB3x", destination_window, enable))
        return self.send_request(6, buf, is_checked=is_checked)
    def InputSelected(self, destination_window, is_checked=True):
        buf = six.BytesIO()
        buf.write(struct.pack("=xx2xI", destination_window))
        return self.send_request(7, buf, InputSelectedCookie, is_checked=is_checked)
    def GetRectangles(self, window, source_kind, is_checked=True):
        buf = six.BytesIO()
        buf.write(struct.pack("=xx2xIB3x", window, source_kind))
        return self.send_request(8, buf, GetRectanglesCookie, is_checked=is_checked)
xcffib._add_ext(key, shapeExtension, _events, _errors)
