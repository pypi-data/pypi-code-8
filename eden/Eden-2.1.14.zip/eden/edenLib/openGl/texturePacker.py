import numpy

class TexturePacker:	# N.B. Very basic, for small numbers of textures only, optimized for wide textures sorted from high to low
	def __init__ (self, width = 8192, height = 1024):
		self.width = width
		self.height = height
		self.pixelArrayNp = numpy.zeros ((width, height, 4), dtype = numpy.uint8)
		self.freeBlocks = [(width, height, 0, 0)]
		self.usedBlocks = []
		
	def addTexture (self, partialPixelArrayNp):
		width, height = partialPixelArrayNp.shape [:-1]
		
		minWidth = 1e10
		for block in self.freeBlocks:
			if block [0] >= width and block [1] >= height and block [0] < minWidth:
				minWidth = block [0]
				bestBlock = block
				
		self.freeBlocks.remove (bestBlock)
		# Divide bestBlock as:
		# X 0
		# 1 1	
			
		usedChild = (width, height, bestBlock [2], bestBlock [3])
		self.usedBlocks.append (usedChild)
		
		self.freeBlocks.append ((bestBlock [0] - width, height, bestBlock [2] + width, bestBlock [3]))
		self.freeBlocks.append ((bestBlock [0], bestBlock [1] - height, bestBlock [2], bestBlock [3] + height))
			
		self.pixelArrayNp [
			usedChild [2] : usedChild [2] + usedChild [0],
			usedChild [3] : usedChild [3] + usedChild [1]
		] = partialPixelArrayNp
			
		# print '---used---'
		# for ub in self.usedBlocks:
		#	print ub
			
		return usedChild
		