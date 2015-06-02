# Generate libSDL2 wrappers.

import json
import os.path

from .builder import Builder

header = """# Automatically generated wrappers.
# Override by adding wrappers to helpers.py.
from __sdl import ffi, lib
from .structs import Struct, unbox, SDLError, u8

def _grab_constants(lib):
    for name in dir(lib):
        if name.upper() != name: continue
        value = getattr(lib, name)
        if isinstance(value, int):
            yield (name, value)
            
globals().update(dict(_grab_constants(lib)))
"""


def go():
    from _sdl import cdefs, helpers

    try:
        with open(os.path.join(os.path.dirname(__file__), 'dox.json'), 'r') as funcdocs:
            all_funcdocs = json.load(funcdocs)
    except IOError:
        all_funcdocs = {}

    builder = Builder(all_funcdocs)

    output_filename = os.path.join(os.path.dirname(__file__),
                                   "..",
                                   "_sdl",
                                   "autohelpers.py")
    with open(output_filename, "w+") as output:
        output.write(header)
        builder.generate(output, cdefs=cdefs, helpers=helpers)

if __name__ == "__main__":
    go()
