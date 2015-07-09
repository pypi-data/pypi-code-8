from traceback import *
from random import *
import copy as cp

from ..node import *

from .transform import *
from .scene import *
from .vecMath import *

quadIndices = (0, 1, 3, 3, 2, 1)

defaultText = 'test'
defaultFont = {'name': 'arial', 'points': 32}
defaultTextColor = [0., 0., 0.]
defaultHighlightColor = [0.7, 0.7, 0.7]
defaultPanelColor = [1., 1., 1.]
defaultBackgroundColor = [0.2, 0.2, 0.2]

layerStep = 0.001
clickStep = 0.01

cursorOk, cursorBeforeText, cursorAfterText, cursorAfterLine = range (4)

halfPi = math.pi / 2

def alphaize (color):
	if color:
		return (color + [1.]) [:4]
	else:
		return None
	
class EditState:
	def __init__ (self, startIndex = 0, cursorIndex = 0, cursorXLocked = 0):
		self.startIndex = startIndex
		self.precursorIndex = cursorIndex
		self.cursorIndex = cursorIndex
		self.cursorXLocked = cursorXLocked
		
	def __str__ (self):
		return str (self.precursorIndex) + ' ' + str (self.cursorIndex)
		
class Core:
	def __init__ (
		self,
		positions,
		textureCoordinates,
		panelColors,
		textColors,
		indices
	):
		self.positions = positions
		self.textureCoordinates = textureCoordinates
		self.panelColors = panelColors
		self.textColors = textColors
		self.indices = indices
		
	def __str__ (self):
		return '''
positions:
{}

indices:
{}
		'''.format (self.positions, self.indices)
		
class BaseView:
	def __init__ (
		self,
		sizeNode = None,
		attitudeNode = None,
		positionNode = None,
	):
		self.sizeNode = getNode (sizeNode, Node ())
		self.scalMatNode = Node () .dependsOn ([self.sizeNode], lambda: getScalMat (self.sizeNode.new))

		self.attitudeNode = getNode (attitudeNode, Node ())
		self.rotMatNode = Node () .dependsOn ([self.attitudeNode], lambda: getRotZYXMat (self.attitudeNode.new))
		
		self.positionNode = getNode (positionNode, Node ())		
		self.translMatNode = Node () .dependsOn ([self.positionNode], lambda: getTranslMat (self.positionNode.new))
		
		self.translRotMatNode = Node () .dependsOn ([self.translMatNode, self.rotMatNode], lambda: self.translMatNode.new * self.rotMatNode.new)
		self.transfMatNode = Node () .dependsOn ([self.translRotMatNode, self.scalMatNode], lambda: self.translRotMatNode.new * self.scalMatNode.new)
		
		self.flatChildViews = []
		
		self.pointerDownNode = Node (None)
		self.pointerUpNode = Node (None)
		self.pointerMoveNode = Node (None)
		
		self.keyDownNode = Node (None)
		self.keyUpNode = Node (None)
		self.keyTextNode = Node (None)
		
		self.hittableNode = Node (False)
		
	def __repr__ (self):
		return self.__class__.__name__
		
	def setFlatChildViews (self, flatChildViews):
		self.flatChildViews = flatChildViews
		for flatChildView in self.flatChildViews:
			flatChildView.parent = self
						
	def postInit (self):
		if self.parent:
			self.globTranslRotMatNode = Node () .dependsOn ([self.parent.globTranslRotMatNode, self.translRotMatNode], lambda: self.parent.globTranslRotMatNode.new * self.translRotMatNode.new)
			self.globTransfMatNode = Node () .dependsOn ([self.globTranslRotMatNode, self.scalMatNode], lambda: self.globTranslRotMatNode.new * self.scalMatNode.new)
		else:
			self.globTranslRotMatNode = Node () .dependsOn ([self.translRotMatNode], lambda: self.translRotMatNode.new)
			self.globTransfMatNode = Node () .dependsOn ([self.transfMatNode], lambda: self.transfMatNode.new)
						
		for childView in self.flatChildViews:
			childView.postInit ()

	def trace (self):
		for nodeName, indent in [
			('sizeNode', False),
			('attitudeNode', False),
			('positionNode', False),
			('scalMatNode', False),
			('rotMatNode', False),
			('translMatNode', False),
			('translRotMatNode', False),
			('transfMatNode', False),
			('coreListNode', False)
		]:
			trace (self, nodeName.strip (), indent)
			
		for childView in self.flatChildViews:
			childView.trace ()
							
	def hitTest (self):
		try:
			if self.hittableNode.new:
				squaredHitDistance = app.mainView.scene.getSquaredHitDistance (app.mainView.scene.window.pointerPosition, self.cornersNode.old [:, 0:3])
				if squaredHitDistance < app.mainView.squaredHitDistance:
					app.mainView.topHitView = self
					app.mainView.squaredHitDistance = squaredHitDistance
			# Due to perspective, a child is not always within the boundaries of its parent, so don't only search 'contained' children
			for childView in self.flatChildViews:
				childView.hitTest ()
		except:
			return None
		
class RectangleView (BaseView):
	normalizedCorners = homogenize (numpy.matrix ((
		(1, 1, 0),
		(-1, 1, 0),
		(-1, -1, 0),
		(1, -1, 0)
	), dtype = typesNp [typesGen ['coordinate']]).T * 0.5)
		
	def __init__ (
		self,
		sizeNode = None,
		attitudeNode = None,
		positionNode = None,
	):
		BaseView.__init__ (
			self,
			sizeNode = sizeNode,
			attitudeNode = attitudeNode,
			positionNode = positionNode
		)

	def postInit (self):
		BaseView.postInit (self)
		
		self.cornersNode = Node () .dependsOn (
			[self.globTransfMatNode],
			lambda: inhomogenize (self.globTransfMatNode.new * self.normalizedCorners)
		)
				
class BeamView (BaseView):
	front, rear, left, right, top, bottom = range (6)
	
	def __init__ (
		self,
		childViews = [],
		sizeNode = None,
		attitudeNode = None,
		positionNode = None,
	):
		BaseView.__init__ (
			self,
			sizeNode = sizeNode,
			attitudeNode = attitudeNode,
			positionNode = positionNode
		)

		self.setFlatChildViews (childViews)
		
	def postInit (self):
		BaseView.postInit (self)
		
		for iChildView, childView in enumerate (self.flatChildViews):
			childView.positionNode.dependsOn (
				[self.sizeNode],
				lambda iChildView = iChildView:
						[0, 0, 0.5 * self.sizeNode.new [2]]
					if iChildView == self.front else (
						[0, 0, -0.5 * self.sizeNode.new [2]]
					if iChildView == self.rear else (
						[-0.5 * self.sizeNode.new [0], 0, 0]
					if iChildView == self.left else (
						[0.5 * self.sizeNode.new [0], 0, 0]
					if iChildView == self.right else (
						[0, 0.5 * self.sizeNode.new [0], 0]
					if iChildView == self.top else (
						[0, -0.5 * self.sizeNode.new [0], 0]			
					)))))
			)
			
			childView.attitudeNode.dependsOn (
				[],
				lambda iChildView = iChildView:
						[0, 0, 0]
					if iChildView == self.front else (
						[0, math.pi, 0]
					if iChildView == self.rear else (
						[0, -halfPi, 0]
					if iChildView == self.left else (
						[0, halfPi, 0]
					if iChildView == self.right else (
						[-halfPi, 0, 0]
					if iChildView == self.top else (
						[halfPi, 0, 0]
					)))))
			)
			
			childView.sizeNode.dependsOn (
				[self.sizeNode],
				lambda iChildView = iChildView:
						self.sizeNode.new
					if iChildView in (self.front, self.rear) else (
						[self.sizeNode.new [2], self.sizeNode.new [1], self.sizeNode.new [0]]
					if iChildView in (self.left, self.right) else (
						[self.sizeNode.new [0], self.sizeNode.new [2], self.sizeNode.new [1]]
					))
			)
			
		self.coreListNode = Node () .dependsOn (
			[childView.coreListNode for childView in self.flatChildViews],
			lambda: reduce (lambda list0, list1: list0 + list1, [childView.coreListNode.new for childView in self.flatChildViews])
		)
				
class PanelView (RectangleView):
	textureCoordinates = numpy.matrix ((
		(0, 0),
		(0, 0),
		(0, 0),
		(0, 0)
	), dtype = typesNp [typesGen ['coordinate']]).T
	
	indices = numpy.array (quadIndices, dtype = typesNp [typesGen ['index']]).T
	textColors = numpy.matrix ([(0, 0, 0, 0) for index in range (RectangleView.normalizedCorners.shape [1])]).T

	def __init__ (
		self,
		sizeNode = None,
		attitudeNode = None,
		positionNode = None,
		colorNode = None
	):
		RectangleView.__init__ (
			self,
			sizeNode = sizeNode,
			attitudeNode = attitudeNode,
			positionNode = positionNode
		)
		
		self.colorNode = getNode (colorNode, Node ())
		self.alphaizedColorNode = Node () .dependsOn ([self.colorNode], lambda: alphaize (self.colorNode.new))
		
		self.hittableNode = Node (True)
		self.focusableViewNode = Node (None)
		self.inputableViewNode = Node (None)
		
	def postInit (self):
		RectangleView.postInit (self)
		
		self.coreListNode = Node () .dependsOn (
			[self.cornersNode, self.alphaizedColorNode],
			lambda: [Core (
				positions = self.cornersNode.new,
				textureCoordinates = self.textureCoordinates,
				panelColors = numpy.matrix ([self.alphaizedColorNode.new for index in range (RectangleView.normalizedCorners.shape [1])]).T,
				textColors = self.textColors,
				indices = self.indices
			)]
		)

class TextView (RectangleView):
	def __init__ (
		self,
		sizeNode = None,
		attitudeNode = None,
		positionNode = None,		
		textNode = None,
		fontNode = None,
		colorNode = None,
	):
		RectangleView.__init__ (
			self,
			sizeNode = sizeNode,
			attitudeNode = attitudeNode,
			positionNode = positionNode
		)
		
		self.textNode = getNode (textNode, Node ())
		self.fontNode = getNode (fontNode, Node ())
		self.colorNode = getNode (colorNode, Node ())
		
		self.alphaizedColorNode = Node () .dependsOn ([self.colorNode], lambda: alphaize (self.colorNode.new))
		self.highlightColorNode = Node (None)
		self.alphaizedHighlightColorNode = Node () .dependsOn ([self.highlightColorNode], lambda: alphaize (self.highlightColorNode.new))
		
	def postInit (self):
		RectangleView.postInit (self)
				
		def getCursorHitOffset ():
			if app.mainView.scene.window.pointerButtons [0]:
				optimalCursorOffset = 0
				minSquaredHitDistance = 1e10
				for cursorOffset in range (self.translatedCoreNode.old.positions.shape [1] / 4):		
					squaredHitDistance = app.mainView.scene.getSquaredHitDistance (app.mainView.scene.window.pointerPosition, self.cornersNode.old [:, 0:3], self.getCursorCoords (cursorOffset, self.translatedCoreNode.old))
					if squaredHitDistance < minSquaredHitDistance:
						optimalCursorOffset = cursorOffset
						minSquaredHitDistance = squaredHitDistance
						
				return optimalCursorOffset
			else:
				return self.cursorHitOffsetNode.old

		self.cursorHitOffsetNode = Node (0) .dependsOn ([self.pointerDownNode, self.pointerMoveNode], getCursorHitOffset) 
			
		def grabInput ():
			if app.mainView.inputViewNode.new == self:
				if app.mainView.inputViewNode.old:
					app.mainView.inputViewNode.old.textNode.dependsOn ()	# Here rather than in else clause of old inputView, to ensure right order
					
				self.textNode.dependsOn (	# Only refers to old rather than new edit state
					[self.keyTextNode, self.keyDownNode],
					getText
				)
				
		app.mainView.inputViewNode.addAction (grabInput)				
				
		def getText ():
			return (
					'{}{}{}'.format (self.textNode.old [0:self.editStateNode.old.cursorIndex], app.mainView.scene.window.text, self.textNode.old [self.editStateNode.old.cursorIndex:])
				if self.keyTextNode.touched else (
					'{}{}'.format (self.textNode.old [0:max (self.editStateNode.old.cursorIndex - 1, 0)], self.textNode.old [self.editStateNode.old.cursorIndex:])
				if app.mainView.scene.window.key == 'Backspace' else (
					'{}{}'.format (self.textNode.old [0:self.editStateNode.old.cursorIndex], self.textNode.old [self.editStateNode.old.cursorIndex + 1:])
				if app.mainView.scene.window.key == 'Delete' else (
					'{}\n{}'.format (self.textNode.old [0:self.editStateNode.old.cursorIndex], self.textNode.old [self.editStateNode.old.cursorIndex:])
				if app.mainView.scene.window.key == 'Return' else (
					self.textNode.old
				))))
			)
					
		def getHardStartIndex ():
			if self.editStateNode.old.startIndex > 0:
				# Search upward for closest hard line end before current topline or for text start
				
				hardStartIndex = min (self.editStateNode.old.startIndex, len (self.textNode.new)) - 1
				# Here we are at the end of the previous hard or soft line, hardStartIndex > 0
				# Clip to end of text when backspacing
					
				if self.textNode.new [hardStartIndex] == '\n':
					hardStartIndex -= 1
				# If it ended with a hard return we've skip that
						
				while hardStartIndex > 0:
					if self.textNode.new [hardStartIndex] == '\n':
						hardStartIndex += 1
						break
						
					hardStartIndex -= 1
					
				# Here we are at the hard beginning of the previous hard or soft line
				return hardStartIndex
			else:
				return 0
					
		self.hardStartIndexNode = Node (None) .dependsOn (
			[self.textNode],
			getHardStartIndex
		)
		
		self.alphabetNode = Node () .dependsOn ([self.fontNode], lambda: app.mainView.scene.window.fontAtlas.getAlphabet (**self.fontNode.new))
		self.lineHeightNode = Node () .dependsOn ([self.alphabetNode], lambda: self.alphabetNode.new.height) 
		self.halfLineHeightNode = Node () .dependsOn ([self.lineHeightNode], lambda: self.lineHeightNode.new / 2) 
		
		def getHardCore ():	# Raw means attitude and position not yet adapted
			text = self.textNode.new + ' '	# Cursor is always in front of char, so extra char needed for cursor at text end
			# chars = ' '	# For debug purposes
			
			scaledPositions = []
			indices = []
			textureCoordinates = []
			
			halfWidth = self.sizeNode.new [0] / 2
			halfHeight = self.sizeNode.new [1] / 2
							
			textXStart = -halfWidth
			textXEnd = halfWidth
			
			lineYStart = halfHeight - self.halfLineHeightNode.new
			
			substrateCellXEnd = textXStart
			substrateCellXStart = substrateCellXEnd
			
			coreStartIndex = self.hardStartIndexNode.new if self.hardStartIndexNode.new != None else self.editStateNode.old.startIndex	# This is where the rendering should begin
			
			yStart = 0 # If hardStartIndex is unused it's just a static text that doesn't need scrolling, so no extra line at bottom (and no extra lines at top).
						
			charIndex = 0	# Index within the visible part or the text
			lineStartIndex = 0	# Start of currently rendered visible line
			safeCharIndex = 0	# Most recent wordwrap point
			while charIndex < len (text) - coreStartIndex:	# As long as there's a tail to print
				char = text [charIndex + coreStartIndex]
				
				# Check for hard and soft newline
				
				hardNewLine = char == '\n'	# If there's an explicit newline, go to next line
				if hardNewLine:
					char = ' '
				
				charMetrics = self.alphabetNode.new.metricsDict [char]
				substrateCellXEnd += self.alphabetNode.new.pixelSize * (charMetrics.advance)	# Compute x position after printing char
				
				softNewLine = substrateCellXEnd > textXEnd and not hardNewLine
				
				# Retract or render
				
				if softNewLine: # Retract
				# If x position after printing char to large and there's a word wrap point after the start of the line, reset state until most recent word wrap point and advance one line
					if safeCharIndex <= lineStartIndex:	# If there's no useful wrap point, just break off the word at the current position
						safeCharIndex = charIndex - 1
						
					charIndex = safeCharIndex
					# chars = chars [ : charIndex]
					scaledPositions = scaledPositions [ : 4 * charIndex]
					indices = indices [ : 6 * charIndex]
					textureCoordinates = textureCoordinates [ : 4 * charIndex]			
				else:	# Render
					# chars += char
					scaledPositions += [
						(substrateCellXEnd, lineYStart + self.halfLineHeightNode.new, 0),
						(substrateCellXStart, lineYStart + self.halfLineHeightNode.new, 0),
						(substrateCellXStart, lineYStart - self.halfLineHeightNode.new, 0),
						(substrateCellXEnd, lineYStart - self.halfLineHeightNode.new, 0)
					]
					substrateCellXStart = substrateCellXEnd
					
					shift = 4 * charIndex
					indices += addScalVec (shift, quadIndices)

					textureCoordinates +=  [
						(charMetrics.yStartNorm, charMetrics.xEndNorm),
						(charMetrics.yStartNorm, charMetrics.xStartNorm),
						(charMetrics.yEndNorm, charMetrics.xStartNorm),
						(charMetrics.yEndNorm, charMetrics.xEndNorm),
					]
					
					charIndex += 1
					
				# If hard or soft newline, go to next line start from retracted or rendered position
					
				if hardNewLine or softNewLine:
					substrateCellXEnd = textXStart
					substrateCellXStart = substrateCellXEnd
					lineYStart -= self.alphabetNode.new.lineHeight
					
					if charIndex == self.editStateNode.old.startIndex - self.hardStartIndexNode.new:
						yStart = lineYStart
					elif yStart - lineYStart > self.sizeNode.new [1] + 2 * self.alphabetNode.new.lineHeight:		# If y position to large, don't print anything more
						break
						
					lineStartIndex = charIndex
				
				# If encountered a true space (not a soft newline), remember it as possible word wrap point
				
				if char == ' ' and not softNewLine:	# If there's whitespace, save state, because this may be a word wrap point
					safeCharIndex = charIndex
					
			if len (scaledPositions):
				scaledPositions = homogenize (numpy.matrix (scaledPositions, dtype = typesNp [typesGen ['coordinate']]) .T)
				nrOfVertices = scaledPositions.shape [1]
				
				indices = numpy.array (indices, dtype = typesNp [typesGen ['index']]) .T
				nrOfIndices = indices.shape [0]
				
				textureCoordinates = numpy.matrix (textureCoordinates, dtype = typesNp [typesGen ['coordinate']]) .T

				panelColors = numpy.matrix ([(0., 0., 0., 0.) for index in range (scaledPositions.shape [1])]) .T
				textColors = numpy.matrix ([self.alphaizedColorNode.new for index in range (scaledPositions.shape [1])]) .T
				
				return Core (
					positions = scaledPositions,
					textureCoordinates = textureCoordinates,
					panelColors = panelColors,
					textColors = textColors,
					indices = indices
				)
			else:
				return None
				
		self.hardCoreNode = Node () .dependsOn (
			[self.textNode, self.hardStartIndexNode, self.sizeNode, self.fontNode, self.alphaizedColorNode],
			getHardCore		
		)
		
		self.editStateNode = Node (EditState ())
	
		def getEditState ():
			def scrollVertically (down, editState):	# It is possible to scroll when here, since the cursor position was checked beforehand
				if down:
					# Init newStartIndex to character before old start index. This is the line we should find the beginning of.
					newStartIndex = editState.startIndex - 1
					oldCursorCoords = self.getCursorCoords  (newStartIndex - self.hardStartIndexNode.new, self.hardCoreNode.new)
					
					# Find line start before that
					while True:
						newStartIndex -= 1
						newCursorCoords = self.getCursorCoords (newStartIndex - self.hardStartIndexNode.new, self.hardCoreNode.new)
						if (
							newCursorCoords == None						# Line "started" with hard return, so now we are above the visible area
							or
							newCursorCoords [1] > oldCursorCoords [1]	# Line "started" with a soft return, so we're still in the visible area
						):
							break

					newStartIndex += 1							
				else:
					# Initialize newStartIndex value of old startIndex
					newStartIndex = editState.startIndex
					oldStartCoords = self.getCursorCoords (newStartIndex - self.hardStartIndexNode.new, self.hardCoreNode.new)
				
					# Find closest hard or soft line end starting a line after current topline
					while True:
						newStartIndex += 1
						if self.getCursorCoords (newStartIndex - self.hardStartIndexNode.new, self.hardCoreNode.new) [1] < oldStartCoords [1]:
							break
												
				editState.startIndex = newStartIndex					
				
				editState.cursorCoords = self.getCursorCoords (editState.cursorIndex - self.hardStartIndexNode.new, self.hardCoreNode.new)
				# Cursor coordinates will be None if at end of text, since there's no character there
								
			def moveCursorHorizontally (right, editState, setPrecursor = False, allowScroll = True):
				# Remember previous cursor position for hightlighting
				if setPrecursor:
					editState.precursorIndex = editState.cursorIndex
					
				# Move cursor to right spot in whole text
				if right:
					if editState.cursorIndex < len (self.textNode.new):
						editState.cursorIndex += 1
					else:
						return cursorBeforeText	# Couldn't move cursor
				else:
					if editState.cursorIndex > 0:
						editState.cursorIndex -= 1
					else:
						return cursorAfterText	# Couldn't move cursor
					
				offset = min (editState.startIndex - self.hardStartIndexNode.new, self.hardCoreNode.new.positions.shape [1] / 4 - 1)
					
				xStart, yStart = self.getCursorCoords (offset, self.hardCoreNode.new) [:2]
				
				cursorOffset = editState.cursorIndex - self.hardStartIndexNode.new
				if cursorOffset >= 0:
					yCursor = self.getCursorCoords (cursorOffset, self.hardCoreNode.new) [1]
				else:
					yCursor = 1e10	# Cursor before hard start, trigger a downscroll
					
				cursorYOffset = yStart - yCursor
				
				if 0 <= cursorYOffset <= self.sizeNode.new [1] - self.alphabetNode.new.lineHeight:
					if xStart > self.getCursorCoords (0, self.hardCoreNode.new) [0]:	# Old start point has become part of previous line by backspace or wordbreak
						scrollVertically (True, editState)
					return cursorOk
				elif allowScroll:
					scrollVertically (not right, editState)	# Should always succeed
					return cursorOk
				else:
					return cursorAfterLine
				
			def moveCursorVertically (down, editState, setPrecursor = False):
				# Attempt moving cursor to right line above or below current
				oldCursorCoords = self.getCursorCoords (editState.cursorIndex - self.hardStartIndexNode.new, self.hardCoreNode.new)
				oldStartIndex = editState.startIndex
				
				while True:
					if moveCursorHorizontally (down, editState, setPrecursor = setPrecursor) != cursorOk:	# Will also scroll if needed
						return False	# Unsuccesful
					
					if self.getCursorCoords (editState.cursorIndex - self.hardStartIndexNode.new, self.hardCoreNode.new) [1] != oldCursorCoords [1] or editState.startIndex != oldStartIndex:
						break			# On right line now
							
				# Move cursor until minimum difference with old x coordinate, scrolling should not happen anymore
				oldDifferenceX = abs (self.getCursorCoords (editState.cursorIndex - self.hardStartIndexNode.new, self.hardCoreNode.new) [0] - editState.cursorXLocked)
				oldCursorIndex = editState.cursorIndex
				
				horizontalResult = None
				while True:
					horizontalResult = moveCursorHorizontally (down, editState, setPrecursor = setPrecursor, allowScroll = False)
					
					if horizontalResult != cursorOk:
						break
						
					differenceX = abs (self.getCursorCoords (editState.cursorIndex - self.hardStartIndexNode.new, self.hardCoreNode.new) [0] - editState.cursorXLocked)
					if differenceX > oldDifferenceX:	# Got further away instead of closer, go back one step
						break
						
					oldCursorIndex = editState.cursorIndex
					oldDifferenceX = differenceX
					
				if horizontalResult in (cursorOk, cursorAfterLine):
					moveCursorHorizontally (not down, editState, setPrecursor = setPrecursor)

				return True
					
			def lockCursorX (editState):
				editState.cursorXLocked = self.getCursorCoords (editState.cursorIndex - self.hardStartIndexNode.new, self.hardCoreNode.new) [0]
				
			editState = cp.deepcopy (self.editStateNode.old)
			
			if app.mainView.inputViewNode.new == self:
				if self.cursorHitOffsetNode.touched:		
					if app.mainView.scene.window.event == pointerDownEvent:
						editState.precursorIndex = editState.cursorIndex
						
					editState.cursorIndex = editState.startIndex + self.cursorHitOffsetNode.new
				elif self.keyTextNode.touched:
					moveCursorHorizontally (True, editState)
					lockCursorX (editState)
				elif self.keyDownNode.touched:
					if app.mainView.scene.window.key == 'Backspace':
						moveCursorHorizontally (False, editState)
						lockCursorX (editState)
					elif app.mainView.scene.window.key == 'Delete':
						lockCursorX (editState)
					elif app.mainView.scene.window.key == 'Return':
						moveCursorHorizontally (True, editState)
						lockCursorX (editState)
					elif app.mainView.scene.window.key == 'Left':
						moveCursorHorizontally (False, editState, setPrecursor = not app.mainView.scene.window.shiftKey)
						lockCursorX (editState)
					elif app.mainView.scene.window.key == 'Right':
						moveCursorHorizontally (True, editState, setPrecursor = not app.mainView.scene.window.shiftKey)
						lockCursorX (editState)
					elif app.mainView.scene.window.key == 'Up':
						moveCursorVertically (False, editState, setPrecursor = not app.mainView.scene.window.shiftKey)
					elif app.mainView.scene.window.key == 'Down':
						moveCursorVertically (True, editState, setPrecursor = not app.mainView.scene.window.shiftKey)
					else:
						pass
				else:
					pass
			else:
				if editState.cursorIndex > len (self.textNode.new):	# There's an extra space at the end
					moveCursorHorizontally (False, editState)
				elif len (self.textNode.old) > len (self.textNode.new) and self.textNode.new [editState.startIndex] != self.textNode.old [editState.startIndex] and editState.startIndex > 0:
					editState.startIndex -= 1
				# editState.precursorIndex = editState.cursorIndex
				
			return editState
			
		def tryGetEditState ():
			try:
				return getEditState ()
			except:
				print traceback.format_exc ()
				raise Error ('Edit state error')
		
		self.editStateNode.dependsOn (
			[app.mainView.inputViewNode, self.keyTextNode, self.keyDownNode, self.hardCoreNode, self.cursorHitOffsetNode],	
			tryGetEditState
		)
	
		def getScrolledCore ():
			start = self.editStateNode.new.startIndex - self.hardStartIndexNode.new
			
			yStart = self.hardCoreNode.new.positions [1, 4 * start]
			
			stop = start + 1
			
			try:	# Clip at lower side of viewport			
				while yStart - self.hardCoreNode.new.positions [1, 4 * stop] < self.sizeNode.new [1] - self.halfLineHeightNode.new:
					stop += 1
			except:	# Not enough text
				pass
			
			shift = (	# From start to hard start
				self.hardCoreNode.new.positions [:, 1] -
				self.hardCoreNode.new.positions [:, 4 * start + 1]
			)
			
			if self.hardCoreNode.new == None:
				return None
			else:
				scrolledCore = (
						Core (
							positions = self.hardCoreNode.new.positions [:, 4 * start : 4 * stop] + shift,
							textureCoordinates = self.hardCoreNode.new.textureCoordinates [:, 4 * start : 4 * stop],
							panelColors = self.hardCoreNode.new.panelColors [:, 4 * start : 4 * stop],
							textColors = self.hardCoreNode.new.textColors [:, 4 * start : 4 * stop],
							indices = self.hardCoreNode.new.indices [6 * start : 6 * stop] - 4 * start
						)
					if self.hardCoreNode.new != None else
						None
				)
								
				editState = self.editStateNode.new
				highlightStartOffset = min (editState.precursorIndex, editState.cursorIndex) - self.hardStartIndexNode.new
				highlightStopOffset = max (editState.precursorIndex, editState.cursorIndex) - self.hardStartIndexNode.new
				
				if self.alphaizedHighlightColorNode.new:
					scrolledCore.panelColors [:, 4 * highlightStartOffset : 4 * highlightStopOffset] = numpy.array (self.alphaizedHighlightColorNode.new) .reshape (4, 1)

				return scrolledCore

		self.scrolledCoreNode = Node () .dependsOn (
			[self.hardCoreNode, self.editStateNode, self.hardStartIndexNode],	# Update display also in label, where editStateNode doesn't change
			getScrolledCore
		)
		
		def getTranslatedCore ():
			return (
					Core (
						positions = inhomogenize (self.globTranslRotMatNode.new * self.scrolledCoreNode.new.positions),
						textureCoordinates = self.scrolledCoreNode.new.textureCoordinates,
						panelColors = self.scrolledCoreNode.new.panelColors,
						textColors = self.scrolledCoreNode.new.textColors,
						indices = self.scrolledCoreNode.new.indices
					)
				if self.scrolledCoreNode.new != None else
					None
			)
		
		self.translatedCoreNode = Node () .dependsOn (
			[self.scrolledCoreNode],
			getTranslatedCore
		)
		
		self.coreListNode = Node () .dependsOn (
			[self.translatedCoreNode],
			lambda: [self.translatedCoreNode.new] if self.translatedCoreNode.new != None else []
		)
		
	def getCursorCoords (self, cursorOffset, core):
		try:
			positions = core.positions
			if 0 <= cursorOffset <= positions.shape [1] / 4:
				result = numpy.mean (positions [:, 4 * cursorOffset + 1 : 4 * cursorOffset + 3], 1) .T.tolist () [0]
				# Correct coordinates with respect to center of TextView == center of LabelView
				result [2] += 2 * layerStep
			else:
				result = None
		except:
			result = None
				
		return result

	def focus (self):
		app.mainView.focusViewNode.follow (self)
		
class LabelView (RectangleView):
	def __init__ (
		self,
		sizeNode = None,
		attitudeNode = None,
		positionNode = None,
		panelColorNode = defaultPanelColor,
		textNode = defaultText,
		fontNode = defaultFont,
		textColorNode = defaultTextColor,
		enabledNode = True,
		focusNode = None,
	):
		RectangleView.__init__ (
			self,
			sizeNode = sizeNode,
			attitudeNode = attitudeNode,
			positionNode = positionNode
		)
		
		self.panelColorNode = getNode (panelColorNode, Node ())
		self.textNode = getNode (textNode, Node ())
		self.fontNode = getNode (fontNode, Node ())
		self.textColorNode = getNode (textColorNode, Node ())
		self.enabledNode = getNode (enabledNode, Node ())
		self.focusNode = getNode (focusNode, Node ())
		
		self.panelView = PanelView (
			sizeNode = self.sizeNode,
			attitudeNode = [0, 0, 0],
			positionNode = [0, 0, 0],
			colorNode = self.panelColorNode
		)
		
		self.textView = TextView (
			sizeNode = Node () .dependsOn ([self.sizeNode], lambda: mulScalVec (0.8, self.sizeNode.new)),
			attitudeNode = [0, 0, 0],
			positionNode = [0, 0, layerStep],
			textNode = self.textNode,
			fontNode = self.fontNode,
			colorNode = self.textColorNode,
		)

		self.setFlatChildViews ([self.panelView, self.textView])
		
	def postInit (self):
		RectangleView.postInit (self)
		
		self.coreListNode = Node () .dependsOn (
			[self.panelView.coreListNode, self.textView.coreListNode],
			lambda: self.panelView.coreListNode.new + self.textView.coreListNode.new
		)
			
class ButtonView (RectangleView):
	def __init__ (
		self,
		sizeNode = None,
		attitudeNode = None,
		positionNode = None,
		panelColorNode = defaultPanelColor,
		sideColorNode = None,
		textNode = defaultText,
		fontNode = defaultFont,
		textColorNode = defaultTextColor,
		pressedNode = None,
		enabledNode = True,
		focusNode = None
	):
		RectangleView.__init__ (
			self,
			sizeNode = sizeNode,
			attitudeNode = attitudeNode,
			positionNode = positionNode
		)	

		self.panelColorNode = getNode (panelColorNode, Node ())
		self.sideColorNode = getNode (sideColorNode, Node () .dependsOn ([self.panelColorNode], lambda: mulScalVec (0.5, self.panelColorNode.new)))
		self.textNode = getNode (textNode, Node ())
		self.fontNode = getNode (fontNode, Node ())
		self.textColorNode = getNode (textColorNode, Node ())
		self.pressedNode = getNode (pressedNode, Node ())
		self.enabledNode = getNode (enabledNode, Node ())
		self.focusNode = getNode (focusNode, Node ())
		
		self.labelView = LabelView (
			panelColorNode = self.panelColorNode,
			textNode = self.textNode,
			fontNode = self.fontNode,
			textColorNode = self.textColorNode		
		)
		
		self.beamSizeNode = Node ()
		self.beamPositionNode = Node ()
		
		self.beamView = BeamView (
			childViews =
				[self.labelView] +
				[PanelView (colorNode = self.panelColorNode)] +
				[PanelView (colorNode = self.sideColorNode) for i in range (4)],
			sizeNode = self.beamSizeNode,
			attitudeNode = [0, 0, 0], 
			positionNode = self.beamPositionNode
		)
		
		self.setFlatChildViews ([self.beamView])
		
	def postInit (self):
		RectangleView.postInit (self)
		
		self.pressedNode.dependsOn (
			[self.labelView.panelView.pointerDownNode, app.mainView.pointerUpAnyNode],
			lambda: self.labelView.panelView.pointerDownNode.touched
		)		
		
		self.beamSizeNode.dependsOn (
			[self.sizeNode, self.pressedNode],
			lambda: [self.sizeNode.new [0], self.sizeNode.new [1], layerStep] if self.pressedNode.new else [self.sizeNode.new [0], self.sizeNode.new [1], layerStep + clickStep]
		)
		
		self.beamPositionNode.dependsOn (
			[self.beamSizeNode],
			lambda: [0, 0, 0.5 * self.beamSizeNode.new[2]]
		)		
		
		self.coreListNode = Node () .dependsOn (
			[self.beamView.coreListNode],
			lambda: self.beamView.coreListNode.new
		)
					
class EditView (RectangleView):
	def __init__ (
		self,
		sizeNode = None,
		attitudeNode = None,
		positionNode = None,
		panelColorNode = defaultPanelColor,
		textNode = defaultText,
		fontNode = defaultFont,
		textColorNode = defaultTextColor,
		highlightColorNode = defaultHighlightColor,
		enabledNode = True,
		focusNode = None
	):
		RectangleView.__init__ (
			self,
			sizeNode = sizeNode,
			attitudeNode = attitudeNode,
			positionNode = positionNode
		)
		
		self.panelColorNode = getNode (panelColorNode, Node ())
		self.textNode = getNode (textNode, Node ())
		self.fontNode = getNode (fontNode, Node ())
		self.textColorNode = getNode (textColorNode, Node ())
		self.highlightColorNode = getNode (highlightColorNode, Node ())
		self.enabledNode = getNode (enabledNode, Node ())
		self.focusNode = getNode (focusNode, Node ())
		
		self.labelView = LabelView (
			sizeNode = self.sizeNode,
			attitudeNode = [0, 0, 0],
			positionNode = [0, 0, 0],
			panelColorNode = self.panelColorNode,
			textNode = self.textNode,
			fontNode = self.fontNode,
			textColorNode = self.textColorNode,
			enabledNode = False,
		)
		
		self.labelView.panelView.focusableViewNode = Node (self)
		self.labelView.panelView.inputableViewNode = Node (self.labelView.textView)

		self.labelView.textView.highlightColorNode.dependsOn ([self.highlightColorNode], lambda: self.highlightColorNode.new)
		
		self.cursorView = PanelView (
			attitudeNode = [0, 0, 0],
			colorNode = self.textColorNode
		)
		
		self.setFlatChildViews ([self.labelView, self.cursorView])
		
	def postInit (self):
		RectangleView.postInit (self)
				
		def grabFocus ():
			app.mainView.focusViewNode.follow (self)
			app.mainView.inputViewNode.follow (self.labelView.textView)
		
		self.labelView.panelView.pointerDownNode.addAction (grabFocus)
		
		self.cursorView.sizeNode.dependsOn (
			[self.labelView.textView.lineHeightNode],
			lambda: [0.001, self.labelView.textView.lineHeightNode.new, 1]
		)
		
		def getCursorPosition ():	
			return self.labelView.textView.getCursorCoords (
				self.labelView.textView.editStateNode.new.cursorIndex - self.labelView.textView.editStateNode.new.startIndex,
				self.labelView.textView.scrolledCoreNode.new
			)
			
		self.cursorView.positionNode.dependsOn (
			[self.labelView.textView.scrolledCoreNode],
			getCursorPosition
		)
		
		def getCoreList ():
			return (
					self.labelView.coreListNode.new + self.cursorView.coreListNode.new
				if app.mainView.focusViewNode.new == self and self.enabledNode.new and app.mainView.blinkNode.new else
					self.labelView.coreListNode.new
			)
		
		self.coreListNode = Node () .dependsOn (
			[app.mainView.focusViewNode, self.enabledNode, app.mainView.blinkNode, self.labelView.coreListNode, self.cursorView.coreListNode],
			getCoreList
		)
		
class GridView (RectangleView):
	def __init__ (
		self,
		childViews,
		sizeNode = None,
		attitudeNode = None,
		positionNode = None
	):
		RectangleView.__init__ (
			self,
			sizeNode = sizeNode,
			attitudeNode = attitudeNode,
			positionNode = positionNode
		)
		
		self.childViews = childViews
		flatChildViews = []
		
		# Internal format:
		#	[
		#		[[[<chieldView>, <startSpan>, <span>], [<chieldView>, <startSpan>, <span>], ...], <startWeight>, <weight>]	
		#		[[[<chieldView>, <startSpan>, <span>], [<chieldView>, <startSpan>, <span>], ...], <startWeight>, <weight>]	
		#		...
		#	]
		
		self.rows = []
		for rowOrWeight in self.childViews:
			if isinstance (rowOrWeight, int):
				self.rows [-1][2] = rowOrWeight	# Replace 1 by explicet row weight
			else:
				if rowOrWeight:
					self.rows.append ([[], None, 1])	# Append new row with implicit weight of 1
					for viewOrSpan in rowOrWeight:
						if isinstance (viewOrSpan, int):
							self.rows [-1][0][-1][2] = viewOrSpan
						elif viewOrSpan:
							self.rows [-1][0] .append ([viewOrSpan, None, 1])
							flatChildViews.append (viewOrSpan)
						else:
							self.rows [-1][0] .append ([EmptyView (), None, 1])
				else:
					self.rows.append ([[[EmptyView (), None, 1]], None, 1])
				
		self.maxRowSpan = 0.
		self.totalRowWeight = 0.
		for row in self.rows:
			row [1] = self.totalRowWeight
			self.totalRowWeight += row [2]
			totalElementSpan = 0.
			for element in row [0]:
				element [1] = totalElementSpan
				totalElementSpan += element [2]
			if totalElementSpan > self.maxRowSpan:
				self.maxRowSpan = totalElementSpan
					
		self.setFlatChildViews (flatChildViews)
		
		for row in self.rows:
			for element in row [0]:
				element [0] .sizeNode.dependsOn (
					[self.sizeNode], 
					lambda row = row, element = element: mulVec (
						self.sizeNode.new,
						[element [2] / self.maxRowSpan, row [2] / self.totalRowWeight, 1]
					)
				)
				
				element [0] .attitudeNode.dependsOn ([], lambda: [0, 0, 0])
				
				element [0] .positionNode.dependsOn (
					[self.sizeNode],
					lambda row = row, element = element:
						mulVec (
							self.sizeNode.new,
							[-0.5 + (element [1]  + 0.5 * element [2]) / self.maxRowSpan, 0.5 - (row [1] + 0.5 * row [2]) / self.totalRowWeight, 0]
						)
				)
							
	def postInit (self):
		RectangleView.postInit (self)
		
		self.coreListNode = Node () .dependsOn (
			[childView.coreListNode for childView in self.flatChildViews],
			lambda: reduce (lambda list0, list1: list0 + list1, [childView.coreListNode.new for childView in self.flatChildViews])
		)
		
class HGridView (GridView):
	def __init__ (self, childViews):
		GridView.__init__ (self, [childViews])
		
class VGridView (GridView):
	def __init__ (self, childViews):
		weightedRows = []
		for viewOrWeight in childViews:
			if isinstance (viewOrWeight, BaseView):		
				weightedRows.append ([viewOrWeight])
			elif viewOrWeight is None:
				weightedRows.append ([])
			else:
				weightedRows.append (viewOrWeight)
		GridView.__init__ (self, weightedRows)
		
class MainView (RectangleView):
	def __init__ (self,
		clientView,
		sizeNode = [1, 1, 1],
		attitudeNode = [0, 0, 0],
		positionNode = [0, 0, 0],
		colorNode = defaultBackgroundColor
	):
		RectangleView.__init__ (
			self,
			sizeNode = sizeNode,
			attitudeNode = attitudeNode,
			positionNode = positionNode
		)		

		self.clientView = clientView
		app.mainView = self
		self.scene = Scene (self)				
		self.setFlatChildViews ([self.clientView])
		# self.trace ()
		
		self.clientView.sizeNode.dependsOn ([self.sizeNode], lambda: self.sizeNode.new)
		self.clientView.attitudeNode.dependsOn ([self.attitudeNode], lambda: [0.3, 0, 0])
		self.clientView.positionNode.dependsOn ([self.positionNode], lambda: [0, 0, 0])
		
		def setColor ():
			self.scene.windowBackgroundColor = self.alphaizedColorNode.new
			self.scene.window.clear ()
				
		self.colorNode = getNode (colorNode, Node ())
		self.alphaizedColorNode = Node () .dependsOn ([self.colorNode], lambda: alphaize (self.colorNode.new)) .addAction (setColor)
		
		setColor ()
		
		self.initNode = Node (None)
			
		alphabet = app.mainView.scene.window.fontAtlas.getAlphabet (**defaultFont)
		
		self.topHitViewNode = Node (None)
		self.focusViewNode = Node (None)
		self.inputViewNode = Node (None)
		
		self.blinkNode = Node (False)
			
		def pointerDownAny ():
			if self.inputViewNode.new:			
				self.inputViewNode.new.pointerDownNode.follow ()
			
		self.pointerDownAnyNode = Node (None) .addAction (pointerDownAny)

		def pointerMoveAny ():
			if self.inputViewNode.new:
				self.inputViewNode.new.pointerMoveNode.follow ()
								
		self.pointerMoveAnyNode = Node (None) .addAction (pointerMoveAny)
		
		def pointerUpAny ():
			if self.inputViewNode.new:
				self.inputViewNode.new.pointerUpNode.follow ()
			
		self.pointerUpAnyNode = Node (None) .addAction (pointerUpAny)
		
		def getTopHitView ():
			self.topHitView = None
			self.squaredHitDistance = 1e10
			self.hitTest ()
			return self.topHitView
			
		self.topHitViewNode.dependsOn (
			[self.pointerDownAnyNode, self.pointerMoveAnyNode, self.pointerUpAnyNode],
			getTopHitView
		)
		
		self.focusViewNode.dependsOn (
			[self.topHitViewNode],
			lambda: self.topHitViewNode.new.focusableViewNode.new if self.topHitViewNode.new else None
		)
		
		self.inputViewNode.dependsOn (
			[self.topHitViewNode],
			lambda: self.topHitViewNode.new.inputableViewNode.new if self.topHitViewNode.new else None
		)
		
		def keyDownAny ():
			if self.inputViewNode.new:
				self.inputViewNode.new.keyDownNode.follow ()
			
		self.keyDownAnyNode = Node (None) .addAction (keyDownAny)
		
		def keyUpAny ():
			if self.inputViewNode.new:
				self.inputViewNode.new.keyUpNode.follow ()
			
		self.keyUpAnyNode = Node (None) .addAction (keyUpAny)
		
		def keyTextAny ():
			if self.inputViewNode.new:
				self.inputViewNode.new.keyTextNode.follow ()
			
		self.keyTextAnyNode = Node (None) .addAction (keyTextAny)
		
		self.postInit ()	# MainView contructed as completely as possible at this point
		
	def postInit (self):
		self.parent = None
		RectangleView.postInit (self)
		self.globTransfMatNode = Node () .dependsOn ([self.transfMatNode], lambda: self.transfMatNode.new)
	
		self.coreListNode = Node () .dependsOn (
			[self.clientView.coreListNode],
			lambda: self.clientView.coreListNode.new
		)
		
		def getTotalCore ():
			offsetRef = [0]
			
			def currentOffset (positions, offsetRef):
				result = offsetRef [0]
				offsetRef [0] += positions.shape [1]
				return result
				
			return Core (
				positions = numpy.hstack ([core.positions for core in self.coreListNode.new]),
				textureCoordinates = numpy.hstack ([core.textureCoordinates for core in self.coreListNode.new]),
				panelColors = numpy.hstack ([core.panelColors for core in self.coreListNode.new]),
				textColors = numpy.hstack ([core.textColors for core in self.coreListNode.new]),
				indices = numpy.hstack ([core.indices + currentOffset (core.positions, offsetRef) for core in self.coreListNode.new])
			)
			
		self.totalCoreNode = Node () .dependsOn (
			[self.initNode, self.coreListNode],
			getTotalCore
		)

	def resize (self):
		pass
			
	def frame (self):
		self.blink = int (2 * self.scene.time) % 2
		if self.blink:
			self.blinkNode.change (True)
		else:
			self.blinkNode.change (False)
			
		self.scene.attitude [1] = 0 # += 0.1 * 2 * math.pi * self.scene.deltaTime
		
	def execute (self, *args, **kwargs):
		self.initNode.change ()
		self.args = args
		self.scene.loop ()
		