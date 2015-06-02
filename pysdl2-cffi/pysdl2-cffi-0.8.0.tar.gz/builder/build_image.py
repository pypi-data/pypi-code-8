# Generate SDL_image wrappers.
# Only used at build time.

import os
import re

from .builder import Builder

header = """# Automatically generated wrappers.
# Override by adding wrappers to helpers.py.
from __sdl_image import ffi, lib
from .structs import unbox
from _sdl.structs import SDLError, u8
from _sdl.autohelpers import SDL_Surface, SDL_Texture, SDL_version

from _sdl.lib import SDL_GetError as IMG_GetError
from _sdl.lib import SDL_SetError as IMG_SetError

"""

def go():
    from _sdl_image import cdefs
    builder = Builder()
    output_filename = os.path.join(os.path.dirname(__file__),
                                   "..",
                                   "_sdl_image",
                                   "autohelpers.py")
    with open(output_filename, "w+") as output:
        output.write(header)
        builder.generate(output,
                         cdefs=cdefs,
                         helpers=cdefs,
                         filter=re.compile("^.* IMG_.*$"))

if __name__ == "__main__":
    go()
