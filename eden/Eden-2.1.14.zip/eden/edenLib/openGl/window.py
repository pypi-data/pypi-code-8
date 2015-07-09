import numpy
import OpenGL.GL as gl
import sdl2
import sdl2.sdlttf as ttf
import sdl2.sdlimage as img
import sdl2.ext as ext
import ctypes

from ctypes import *

from ..util import *
from .texturePacker import *
from .vecMath import *

shaderTypesGl = {'vertex': gl.GL_VERTEX_SHADER, 'fragment': gl.GL_FRAGMENT_SHADER}

typesGen = {'coordinate': 'float32', 'colorComponent': 'float32', 'index': 'uint16'}
typesNp = {'float32': numpy.float32, 'uint16': numpy.uint16}
typesGl = {'float32': gl.GL_FLOAT, 'uint16': gl.GL_UNSIGNED_SHORT}

pointHeight = 34e-5

resizeEvent, pointerDownEvent, pointerMoveEvent, pointerUpEvent, keyDownEvent, keyUpEvent, textEvent = range (7)
		
class CharMetrics:
	def __init__ (self, alphabet, xStart, xMin, xMax, yMin, yMax, advance):
		self.alphabet = alphabet
		self.xStart = xStart
		self.xMin = xMin
		self.xMax = xMax
		self.yMin = yMin 
		self.yMax = yMax
		self.advance = advance
		
	def setTextureCoords (self):
		self.xStartNorm = self.alphabet.xStartNorm +  self.alphabet.xNormFactor * self.xStart
		self.xEndNorm = self.xStartNorm + self.alphabet.xNormFactor * (self.advance - 1)
		self.yStartNorm = self.alphabet.yStartNorm
		self.yEndNorm = self.yStartNorm + self.alphabet.heightNorm
		
class Alphabet:
	def __init__ (self, fontAtlas, name, points, style):
		self.fontAtlas = fontAtlas
		self.name = name
		self.points = points
		self.style = style
		
		self.height = pointHeight * self.points		
		
		self.metricsDict = {}
		color = sdl2.SDL_Color ( *(255 * numpy.array ((0, 0, 0, 1))))

		fontFileName = os.path.join (os.environ ["windir"], "Fonts", '{}.ttf'.format (self.name))
		self.font = ttf.TTF_OpenFont (fontFileName, self.points)
		ttf.TTF_SetFontKerning (self.font, 0)
		ttf.TTF_SetFontHinting(self.font, ttf.TTF_HINTING_NONE)

		self.fontHeightPixels = ttf.TTF_FontHeight (self.font)
		self.pixelSize = self.height / self.fontHeightPixels
		
		self.lineHeightPixels = ttf.TTF_FontLineSkip (self.font)
		self.lineHeight = self.pixelSize * self.lineHeightPixels
		
		xStart = 0
		xMin = c_long()
		xMax = c_long ()
		yMin = c_long ()
		yMax = c_long ()
		advance = c_long (0)
		
		for char in self.fontAtlas.charList:
			ttf.TTF_GlyphMetrics (self.font, ord (char), byref (xMin), byref (xMax), byref (yMin), byref (yMax), byref (advance))
			self.metricsDict [char] = CharMetrics (self, xStart, xMin.value, xMax.value, yMin.value, yMax.value, advance.value)
			xStart += advance.value
			
		self.surface = ttf.TTF_RenderText_Blended (self.font, ''.join (self.fontAtlas.charList), color) .contents
		ttf.TTF_CloseFont (self.font)
		
		self.pixelArrayNp = numpy.copy (sdl2.ext.pixels3d (self.surface))	# Copy to prevent memory corruption, sdl2.ext.pixels3d is experimental
		
		sdl2.SDL_FreeSurface (self.surface)
		
		self.widthPixels, self.heightPixels, self.xStartPixels, self.yStartPixels = self.fontAtlas.texturePacker.addTexture (self.pixelArrayNp)
		
		self.xNormFactor = 1. / self.fontAtlas.texturePacker.pixelArrayNp.shape [0]
		self.yNormFactor = 1. / self.fontAtlas.texturePacker.pixelArrayNp.shape [1]
		
		self.widthNorm = self.xNormFactor * self.widthPixels
		self.heightNorm = self.yNormFactor * self.heightPixels
		self.xStartNorm = self.xNormFactor * self.xStartPixels
		self.yStartNorm = self.yNormFactor * self.yStartPixels
		
		for char in self.fontAtlas.charList:
			self.metricsDict [char] .setTextureCoords ()
			
		gl.glTexImage2D (gl.GL_TEXTURE_2D, 0, gl.GL_RGBA8, self.fontAtlas.texturePacker.pixelArrayNp.shape [1], self.fontAtlas.texturePacker.pixelArrayNp.shape [0], 0, gl.GL_BGRA, gl.GL_UNSIGNED_BYTE, self.fontAtlas.texturePacker.pixelArrayNp)
		
class FontAtlas:
	def __init__ (self):
		ttf.TTF_Init ()
		
		self.charList = [chr (i) for i in range (32, 127)]
		self.texturePacker = TexturePacker ()
		self.fontDict = {}
		
		self.texture = gl.glGenTextures (1) # Generate unique id for 1 texture 
		gl.glActiveTexture(gl.GL_TEXTURE0)	# Set active texture that that subsequent texture state calls will affect
		gl.glBindTexture (gl.GL_TEXTURE_2D_MULTISAMPLE, self.texture)	# Bind active texture to unique id (why the hassle...)
		
		gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
		gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
		
		gl.glTexParameteri (gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
		gl.glTexParameteri (gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
		
	def getAlphabet (self, name = 'arial', points = 32, style = 'normal', height = None):
		if height:
			points = int (self.height / pointHeight)
		else:
			height = pointHeight * points
			
		if name in self.fontDict:
			nameSet = self.fontDict [name]
		else:
			nameSet = {}
			self.fontDict [name] = nameSet
			
		if points in nameSet:
			pointSet = nameSet [points]
		else:
			pointSet = {}
			nameSet [points] = pointSet
			
		if style in pointSet:
			alphabet = pointSet [style]
		else:
			alphabet = Alphabet (self, name, points, style)			
			pointSet [style] = alphabet

		return alphabet

class Window:
	def __init__ (self, scene):
		self.scene = scene
	
		if sdl2.SDL_Init (sdl2.SDL_INIT_VIDEO) != 0:
			raise Error (sdl2.SDL_GetError ())
 
		sdl2.SDL_GL_SetAttribute (sdl2.SDL_GL_RED_SIZE, 8)
		sdl2.SDL_GL_SetAttribute (sdl2.SDL_GL_GREEN_SIZE, 8)
		sdl2.SDL_GL_SetAttribute (sdl2.SDL_GL_BLUE_SIZE, 8)
		sdl2.SDL_GL_SetAttribute (sdl2.SDL_GL_ALPHA_SIZE, 8)
		 
		sdl2.SDL_GL_SetAttribute (sdl2.SDL_GL_DEPTH_SIZE, 24)
		sdl2.SDL_GL_SetAttribute (sdl2.SDL_GL_DOUBLEBUFFER, 1)

		sdl2.SDL_GL_SetAttribute (sdl2.SDL_GL_ACCELERATED_VISUAL, 1)	 
		 
		sdl2.SDL_GL_SetAttribute (sdl2.SDL_GL_MULTISAMPLEBUFFERS, 1)
		sdl2.SDL_GL_SetAttribute (sdl2.SDL_GL_MULTISAMPLESAMPLES, 16)
		
		# debugBuffers = c_long ()
		# sdl2.SDL_GL_GetAttribute (gl.GL_SAMPLE_BUFFERS, debugBuffers)
		# print 'Multisample buffers: {}'.format (debugBuffers.value)
		
		# debugSamples = c_long ()
		# sdl2.SDL_GL_GetAttribute (gl.GL_SAMPLES, debugSamples)
		# print 'Multisample samples: {}'.format (debugSamples.value)			
			
		# print '>>>', sdl2.SDL_GetError (), '<<<'

		self.width = self.scene.initialWindowSize [0]
		self.height = self.scene.initialWindowSize [1]
					
		self.window = sdl2.SDL_CreateWindow (
			'OpenGL test',
			sdl2.SDL_WINDOWPOS_UNDEFINED,
			sdl2.SDL_WINDOWPOS_UNDEFINED,
			self.width,
			self.height,
			sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_RESIZABLE
		)
		
		if not self.window:
			raise Error (sdl2.SDL_GetError ())

		self.context = sdl2.SDL_GL_CreateContext (self.window)
		gl.glPixelStorei (gl.GL_UNPACK_ALIGNMENT, 1)		
		gl.glEnable (gl.GL_DEPTH_TEST)
		gl.glEnable (gl.GL_BLEND)
		gl.glEnable (gl.GL_MULTISAMPLE)
		gl.glHint (gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST );
		gl.glHint (gl.GL_POLYGON_SMOOTH_HINT, gl.GL_NICEST );
		gl.glEnable (gl.GL_LINE_SMOOTH);
		gl.glEnable (gl.GL_POLYGON_SMOOTH);		
		gl.glBlendFunc (gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
		gl.glEnable(gl.GL_TEXTURE_2D)
		gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_REPLACE)
		
		self.delayMilliSeconds = 1000 / self.scene.framesPerSecond	# Must be int
		
		self.fontAtlas = FontAtlas ()
		
		self.resize = lambda: None
		self.frame = lambda: None
		
		self.pointerButtons = [False, False, False]
		self.oldPointerButtons = self.pointerButtons
		
		self.pointerPosition = [-1000000, -1000000]
		self.oldPointerPosition = self.pointerPosition
		self.pointerDelta = subVec (self.pointerPosition, self.oldPointerPosition)
		
		self.key = ''
		self.text = ''
		
		self.shiftKey = False
		self.controlKey = False
		self.altKey = False
		
		self.lastEvent = None
		
	def clear (self):
		gl.glClearColor (*self.scene.windowBackgroundColor)
		
	def loop (self):
		def getCentralCoordinates (x, y):
			return [x - (self.width / 2.), (self.height / 2.) - y]
	
		event = sdl2.SDL_Event ()
		running = True
		while running:
			if sdl2.SDL_PollEvent (ctypes.byref (event)):
				if event.type == sdl2.SDL_QUIT:
					running = False
				elif event.type == sdl2.SDL_WINDOWEVENT:
					if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
						self.event = resizeEvent
						self.width = event.window.data1
						self.height = event.window.data2
						self.scene.aspectRatio = float (self.width) / self.height
						gl.glViewport (0, 0, self.width, self.height);		

						self.scene.resize ()
				elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
					self.event = pointerDownEvent
					self.oldPointerButtons = self.pointerButtons [:]
					self.pointerButtons [event.button.button - 1] = True
					self.oldPointerPosition = self.pointerPosition
					self.pointerPosition = getCentralCoordinates (event.button.x, event.button.y)
					self.scene.mainView.pointerDownAnyNode.change ()
				elif event.type == sdl2.SDL_MOUSEMOTION:
					self.event = pointerMoveEvent
					self.oldPointerPosition = self.pointerPosition
					self.pointerPosition = getCentralCoordinates (event.motion.x, event.motion.y)
					self.scene.mainView.pointerMoveAnyNode.change ()
				elif event.type == sdl2.SDL_MOUSEBUTTONUP:
					self.event = pointerUpEvent
					self.oldPointerButtons = self.pointerButtons [:]
					self.pointerButtons [event.button.button - 1] = False
					self.oldPointerPosition = self.pointerPosition
					self.pointerPosition = getCentralCoordinates (event.button.x, event.button.y)
					self.scene.mainView.pointerUpAnyNode.change ()
				elif event.type == sdl2.SDL_KEYDOWN:
					self.event = keyDownEvent
					self.key = sdl2.SDL_GetKeyName (event.key.keysym.sym)
					if self.key == 'Shift':
						self.shiftKey = True
					elif self.key == 'Control':
						self.controlKey = True
					elif self.key == 'Alt':
						self.altKey = True
					self.scene.mainView.keyDownAnyNode.change ()
				elif event.type == sdl2.SDL_KEYUP:
					self.event = keyUpEvent
					self.key = sdl2.SDL_GetKeyName (event.key.keysym.sym)
					if self.key == 'Shift':
						self.shiftKey = False
					elif self.key == 'Control':
						self.controlKey = False
					elif self.key == 'Alt':
						self.altKey = False
					self.scene.mainView.keyUpAnyNode.change ()
				elif event.type == sdl2.SDL_TEXTINPUT:
					self.event = textEvent
					self.text = event.text.text
					self.scene.mainView.keyTextAnyNode.change ()
						
			self.scene.frame ()

			sdl2.SDL_Delay (self.delayMilliSeconds)
					
		sdl2.SDL_GL_DeleteContext (self.context)
		sdl2.SDL_DestroyWindow (self.window)
		sdl2.SDL_Quit
		
	def getTime (self):
		return sdl2.SDL_GetTicks () / 1000.
					
	def render (self):
		gl.glClear (gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
		gl.glDrawElements (gl.GL_TRIANGLES, self.scene.indices.shape [0], typesGl [typesGen ['index']], None)
		sdl2.SDL_GL_SwapWindow (self.window)
		
	def terminate (self):
		gl.glDeleteTextures (texture)
		