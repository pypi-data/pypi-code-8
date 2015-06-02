"""
Call cffi to compile the extension module.
With cffi 1.0 this is only needed at build time.
"""

import os.path
import cffi
ffi = cffi.FFI()

here = os.path.dirname(__file__)
for filename in ("sdl.h", "defines.h"):
    with open(os.path.join(here, filename), "r") as header:
        ffi.cdef(header.read())

try:
    from _sdl_paths import _headers, _extension_args
except ImportError:
    _headers = {'sdl_h':'', 'sdl_image_h':'', 'sdl_mixer_h':'', 'sdl_ttf_h':''}
    _extenson_args = lambda x: {}

ffi.set_source("__sdl", 
    """
    #include <%(sdl_h)s>
    """ % _headers,
    **_extension_args('sdl'))
    
if __name__ == "__main__":
    ffi.compile()
