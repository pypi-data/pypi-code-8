# Dynamic OpenGl 

import sys
import numpy
import math
import datetime
import OpenGL.GL as gl

from ..node import *

from .window import *
from .view import *
from .transform import *
from .shader import *

class Scene:	
	framesPerSecond = 50
	aspectRatio = 1
	initialWindowSize = (512, 512)
	windowBackgroundColor = (0, 0, 0, 1)
	
	fieldOfViewY = 0.3 * 2 * math.atan (0.5)
	zNearFar = [0.4, 1.6]
	
	position = [0, 0, -1]
	attitude = [0, 0, 0]
	size = [1, 1, 1]
	
	def __init__ (self, mainView):
		self.window = Window (self)

		self.mainView = mainView
		self.attitude = self.__class__.attitude
	
		self.lastCoreEvent = 0
			
		# Initialize shaders
		
		self.program = Program (
			Shader (
				'vertex',
				'''
					uniform mat4 cameraMat;
					attribute vec3 position;
					attribute vec4 panelColor;
					attribute vec4 textColor;
					attribute vec2 textureCoordinates;
					varying vec4 panelColorVar;
					varying vec4 textColorVar;
					varying vec2 textureCoordinatesVar;
					void main () {
						gl_Position = vec4 (cameraMat * vec4 (position, 1));
						panelColorVar = panelColor;
						textColorVar = textColor;
						textureCoordinatesVar = textureCoordinates;
					}		
				'''
			),
			Shader (
				'fragment',
				'''
					uniform sampler2D aTexture;
					varying vec4 panelColorVar;
					varying vec4 textColorVar;
					varying vec2 textureCoordinatesVar;
					varying vec4 textureColorVar;
					varying vec4 finalColorVar;
					varying float alpha;
					void main () {
						textureColorVar = texture (aTexture, textureCoordinatesVar);
						alpha = textureColorVar [3];
						finalColorVar = alpha * textColorVar + (1 - alpha) * panelColorVar;
						gl_FragColor = finalColorVar;
					}
				'''
			),
		)
		
	def setCore (self):
		self.attributes = numpy.zeros (self.mainView.totalCoreNode.new.positions.shape [1], [
			('position', typesNp [typesGen ['coordinate']], 3),
			('textureCoordinates', typesNp [typesGen ['coordinate']], 2),
			('panelColor', typesNp [typesGen ['colorComponent']], 4),
			('textColor', typesNp [typesGen ['colorComponent']], 4),
		])
		
		self.attributes ['position'] = self.mainView.totalCoreNode.new.positions.T
		self.attributes ['textureCoordinates'] = self.mainView.totalCoreNode.new.textureCoordinates.T
		self.attributes ['panelColor'] = self.mainView.totalCoreNode.new.panelColors.T
		self.attributes ['textColor'] = self.mainView.totalCoreNode.new.textColors.T
		self.program.setAttributes (self.attributes)
		
		self.indices = numpy.zeros (self.mainView.totalCoreNode.new.indices.shape [0], typesNp [typesGen ['index']])
		self.indices  = self.mainView.totalCoreNode.new.indices
		self.program.setIndices (self.indices)
		
	def setUniforms (self):
		self.sceneTransfMat = getTranslMat (self.position) * getRotZYXMat (self.attitude) * getScalMat (self.size)
		self.program.setUniform ('cameraMat', getPerspMat (self.fieldOfViewY, self.aspectRatio, self.zNearFar) * self.sceneTransfMat)
		self.program.setUniform ('aTexture', 0)
		
	def getNearPoint (self, screenPointPixels):
		# The other needed point for hit testing is the eye at (0, 0, 0)
		# So we just have to intersect lambda * returnvalue with each plane given by four corners
		nearHeight = 2 * self.zNearFar [0] * math.tan (self.fieldOfViewY / 2)
		mPerScreenPixelNear = nearHeight / self.window.height
		return (mPerScreenPixelNear * screenPointPixels [0], mPerScreenPixelNear * screenPointPixels [1], -self.zNearFar [0])

	def getSquaredHitDistance(self, screenPointPixels, panePoints, targetPoint = None):		
		# homoPanePoints:
		# 1-0
		# |
		# 2
		
		rayPoints = inhomogenize (self.sceneTransfMat.I * homogenize (numpy.matrix ((
			(0, 0, 0),
			self.getNearPoint (screenPointPixels)
		), dtype = typesNp [typesGen ['coordinate']]).T))
	
		# screenPointPixels is fixed with respect to the camera
		# panePoints are fixed with respect to the scene
		# rayPoints are fixed with respect to the scene
		# So the hitpoint with the smallest distance to rayPoints [:, 0] counts
	
		# supVecLine + a' * dirVecLine == supVecPlane + b * dirVec0Plane + c * dirVec1Plane ==>
		# supVecLine - supVecPlane == a * dirVecLine + b * dirVec0Plane + c * dirVec1Plane with a == -a' ==>
		# supVecLine - supVecPlane = [dirVecLine, dirVec0Plane, dirVec1Plane] [[a], [b], [c]] ==>
		# [[a], [b], [c]] = [dirVecLine, dirVec0Plane, dirVec1Plane] .I (supVecLine - supVecPlane) =>
		
		supVecLine = rayPoints [:, 0]
		dirVecLine = rayPoints [:, 1] - supVecLine
		
		supVecPlane = panePoints [:, 1]
		dirVec0Plane = panePoints [:, 0] - panePoints [:, 1]
		dirVec1Plane = panePoints [:, 2] - panePoints [:, 1]
		
		try:	# Matrix may be singular
			abc = numpy.hstack ((dirVecLine, dirVec0Plane, dirVec1Plane)) .I * (supVecLine - supVecPlane)
		except:
			return 1e10
		
		hitPoint = supVecLine - abc [0, 0] * dirVecLine
		
		if 0 < abc [1, 0] < 1 and 0 < abc [2, 0] < 1:
			if targetPoint:
				targetPoint = numpy.matrix (targetPoint [0:3]) .T
				hitDifference = targetPoint -  hitPoint
			else:
				hitDifference = (rayPoints [:, 0] - hitPoint)
				
			squaredHitDistance = (hitDifference.T * hitDifference) [0, 0]
			return squaredHitDistance
		else:
			return 1e10
		
	def render (self):
		self.window.render ()
		
	def resize (self):
		self.setUniforms ()
		self.mainView.resize ()
		
	def frame (self):	# Rendering is done at a fixed framerate, even if nothing has changed		
		if self.mainView.totalCoreNode.event > self.lastCoreEvent:
			self.setCore ()
			self.lastCoreEvent = self.mainView.totalCoreNode.event

		if self.mainView.totalCoreNode.event > 1:
			self.setUniforms ()		
			self.render ()
		
		self.oldTime = self.time
		self.time = self.window.getTime ()
		self.deltaTime = self.time - self.oldTime

		self.mainView.frame ()		
		
	def loop (self):
		self.time = self.window.getTime () - 1. / self.framesPerSecond		
		self.window.loop ()
		