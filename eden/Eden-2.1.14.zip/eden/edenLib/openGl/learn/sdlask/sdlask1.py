from sdl2 import *
from OpenGL.GL import *
from time import *

# === Initialize SDL and OpenGL

SDL_Init (SDL_INIT_VIDEO)
window = SDL_CreateWindow (
	b"Hello World",
	SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
	592, 460,
	SDL_WINDOW_OPENGL
)

context = SDL_GL_CreateContext (window)
glEnable (GL_DEPTH_TEST)
glEnable (GL_BLEND)
glEnable(GL_TEXTURE_2D)
glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glClearColor (0.5, 0.5, 0.5, 1)
glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

# === Set texture

from PIL import Image
import numpy
img = Image.open('flagEn.bmp') # .jpg, .bmp, etc. also work
img_data = numpy.array(list(img.getdata()), numpy.int8)
	
texture = glGenTextures(1)
glPixelStorei(GL_UNPACK_ALIGNMENT,1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)

# === Draw image

glColor (0, 0, 0.5, 1)
glBegin( GL_QUADS )

glVertex2f (-0.5, -0.5)
glTexCoord2f(0, 0)

glVertex2f (0.5, -0.5)
glTexCoord2f(10, 0)

glVertex2f (0.5, 0.5)
glTexCoord2f(10, 10)

glVertex2f (-0.5, 0.5)
glTexCoord2f(0, 10)

glEnd()

SDL_GL_SwapWindow (window)

# === Wait a while then exit

sleep (5)

SDL_DestroyWindow (window)
SDL_Quit ()
 
	