import ctypes
import numpy

import OpenGL.GL as gl

from .window import *

class Shader:
	def __init__ (self, aType, code):
		self.aType = aType
		self.code = code
		
		self.shaderGl = gl.glCreateShader (shaderTypesGl [self.aType])
		gl.glShaderSource (self.shaderGl, self.code)
		gl.glCompileShader (self.shaderGl)
		
class Program:	
	def __init__ (self, *shaders):
		self.testShaders = shaders
	
		self.programGl = gl.glCreateProgram ()
		
		for shader in shaders:					
			gl.glAttachShader (self.programGl, shader.shaderGl)
			
		gl.glLinkProgram (self.programGl)
		
		for shader in shaders:
			gl.glDetachShader (self.programGl, shader.shaderGl)
			
		gl.glUseProgram (self.programGl)
		
	def setAttributes (self, attributes):
		attributeBuffer = gl.glGenBuffers (1)	# Get unused identifier
		gl.glBindBuffer (gl.GL_ARRAY_BUFFER, attributeBuffer)	# Allocate GPU buffer
		gl.glBufferData (gl.GL_ARRAY_BUFFER, attributes.nbytes, attributes, gl.GL_STATIC_DRAW)	# Copy data to GPU buffer 
	
		stride = attributes.dtype.itemsize	
		offset = 0
		
		for attributeName in attributes.dtype.names:
			location = gl.glGetAttribLocation (self.programGl, attributeName)	# Get meta-info object of attribute
			attribute = attributes.dtype [attributeName]
			dimension = attribute.shape [0]
			typeGen = attribute.subdtype [0] .name
			gl.glEnableVertexAttribArray (location)	# Make attribute accessible in vertex attribute array
			gl.glVertexAttribPointer (location, dimension, typesGl [typeGen], False, stride, ctypes.c_void_p (offset))	# Connect vertex attribute array to the right places the in already filled buffer
			offset += attribute.itemsize
	
	def setIndices (self, indices):
		indexBuffer = gl.glGenBuffers (1)	# Get empty buffer
		gl.glBindBuffer (gl.GL_ELEMENT_ARRAY_BUFFER, indexBuffer)	# Make buffer current
		gl.glBufferData (gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_STATIC_DRAW)	# Copy data to buffer
		
	def setUniform (self, name, value):
		location = gl.glGetUniformLocation (self.programGl, name)	# Reference to named field in program
		if isinstance (value, numpy.matrix):
			if value.shape == (4, 4):
				gl.glUniformMatrix4fv (location, 1, gl.GL_FALSE, value.T.tolist ())
			elif value.shape == (4, 1):
				gl.glUniform4fv (location, 1, value.tolist ())
			else:
				raise Exception ('Invalid uniform shape')
		elif isinstance (value, float):
			gl.glUniform1f (location, value)
		elif isinstance (value, int):
				gl.glUniform1i (location, value)
		else:
			raise Exception ('Invalid uniform type')
			