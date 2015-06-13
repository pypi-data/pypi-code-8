import ctypes


class MPQFileData(ctypes.Structure):
    _fields_ = [
        ('filename', ctypes.c_char * 1024),
        ('plainpath', ctypes.c_char_p),
        ('hashindex', ctypes.c_int, 32),
        ('blockindex', ctypes.c_int, 32),
        ('filesize', ctypes.c_int, 32),
        ('fileflags', ctypes.c_int, 32),
        ('compsize', ctypes.c_int, 32),
        ('filetimelo', ctypes.c_int, 32),
        ('filetimehi', ctypes.c_int, 32),
        ('locale', ctypes.c_int, 32)
    ]
