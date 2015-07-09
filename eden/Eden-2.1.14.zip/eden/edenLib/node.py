# Copyright (C) 2005 - 2014 Jacques de Hooge, Geatec Engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.

import sys

from .base import *
from .util import *

currentEvent = UniqueNumber (1)
triggerNode = CallableValue ()

indentLevel = 0
recursionMessage = 'recursive node evaluation'
maxRecursionCount = 10

class Transactor:
	def __init__ (self):
		self.clear ()

	def clear (self):
		self.updatedNodes = []
	
	def add (self, node):
		self.updatedNodes.append (node)
		
	def contains (self, node):
		return node in self.updatedNodes	# Reference equality
			
	def rollBack (self):
		for node in self.updatedNodes:
			node.rollBack ()
			
	def act (self):
		for node in self.updatedNodes:
			node.act ()
			
transactor = Transactor ()

class Node (object):							# Node representing atomary partial state in a state machine
	def __init__ (self, value = Nothing):				# Initial value is optional, not needed in case of dependent nodes ('Nothing' introduced y15m02d14)
		self.sinkNodes = []								# Nodes that depend on this node
		self.links = []									# Zero or more links to bareRead / bareWrite pairs
		self.exceptions = []
		self.actions = []
		self.validator = lambda value: True				# Validators are deprecated, use exceptions instead
		
		self.persistent = False							# Assume not worth persisting
		self.recursionCount = 0
		
		if value ==  Nothing:							# If node is uninitialized
			self.event = 0								#	It should be updated
		else:											# If node is supposed to be freely initialized
			self.currentValue = value					#	Free initialisation
			self.previousValue = self.currentValue		#	Make sure previousValue is available in case of free initialisation
			self.event = currentEvent ()				#	Remember up to date
			
			if not value is None:						#	If it is a freely initialized ordinary node rather than an event-only node
				self.persistent = True					#		Remember it is part of a non-redundant basis for persistence
				
		self.traceName = ''
			
	version = property (lambda self: self.event)
	
	def trace (self, traceName, indent = False):
		self.traceName = traceName
		self.indent = indent
		return self
		
	def printTrace (self, getMessage, newLine = False, indent = None):
		if self.traceName and not self.traceName.startswith ('_'):
			global indentLevel
			
			if self.indent and indent == '+':
				indentLevel += 1

			indents = indentLevel * '\t'
			splitName = self.traceName.split ('.')
			if len (splitName) == 2:
				print '{0}{1}<TRACE> {2:<20}{3:>20}: {4}, event {5}'.format ('\n' if newLine else '', indents, splitName [0], splitName [1], getMessage (), self.event)
			else:
				print '{0}{1}<TRACE> {2:>20}: {3}, event {4}'.format ('\n' if newLine else '', indents, splitName [0], getMessage (), self.event)

			if self.indent and indent == '-':
				indentLevel -= 1

				
	def dependsOn (self, sourceNodes = [], getter = lambda: None):		# Lay dependency relations this node and other nodes that it depends on	
		if hasattr (self, 'sourceNodes'):				# If dependsOn was called before for this node
			for sourceNode in self.sourceNodes:			#	For all nodes that this node depended upon previously
				sourceNode.sinkNodes.remove (self)		#		Remove the old dependency
	
		for sourceNode in sourceNodes:					# For each node that this node depends upon
			sourceNode.sinkNodes.append (self)			#	Register this node with that other node
			
		self.sourceNodes = sourceNodes					# Remember sourceNodes
			
		self.getter = getter							# Lay down how to construct the value of this node from the values of those others
		
		if sourceNodes:
			try:
				self.invalidate ()							# Force calling getter, even if node was initialized, and propagation
				self.evaluate ()							# Dependent initialisation by backward evaluation
			except:												 
				pass										# Lacks some needed dependency, or getter is incomputable, wait for initialisation by forward propagation
			
		return self
		
	def addException (self, condition, aClass, message):
		self.exceptions.append ((condition, aClass, message))
		return self
		
	def addAction (self, action):	# Convenience method, mainly to allow call chaining, added y14m12d10
		self.actions.append (action)
		return self
				
	def invalidate (self):							# Invalidation phase, to know where to propagate and prevent cycles
		self.printTrace (lambda: 'START invalidate', indent = '+')
	
		# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		if hasattr (self, 'currentValue'):			#		If already initialised
			if not transactor.contains (self):		#			If currentValue not already saved (prevent saving intermediate from follow)
				self.previousValue = self.currentValue	#			Remember previousValue early to enable rollBack if getter raises exception
				transactor.add (self)					#			Register that this node may alter its value as part of the current transaction
		# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

		self.event = 0									# Should be updated ??? Only if it does not have the current event number?

		for sinkNode in self.sinkNodes:					# For all nodes that depend upon this node
			sinkNode.printTrace (lambda: 'Before possible invalidation', indent = '+')
			if sinkNode.event != 0:						#	If not closing a cycle	(flaw: if previous evaluation failed, event will be stuck at 0)
				sinkNode.invalidate ()					#		Invalidate that dependent node
			sinkNode.printTrace (lambda: 'After possible invalidation', indent = '-')

		self.printTrace (lambda: 'END invalidate', indent = '-')				
				
	def validate (self):
		for exception in self.exceptions:
			try:	# Try and except block swapped y14m12d24
				if exception [0] ():
					raise exception [1] (exception [2])
			except TypeError:						# Checkfunctions with self.currentValue parameter are deprecated
				currentValue = self.currentValue if hasattr (self, 'currentValue') else 'not yet inialized'
				if exception [0] (currentValue):
					raise exception [1] (exception [2])
	
		if not hasattr (self, 'currentValue') or not self.validator (self.currentValue):	# Validators are deprecated
			raise Error ('Node value invalid')

	def evaluate (self):							# Evaluation phase, two way propagation
		self.printTrace (lambda: 'START evaluate', indent = '+')
		
		if self.event == 0:	# So only nodes that lay on the trigger path are REALLY ever computed!
			if self.recursionCount > maxRecursionCount:
				currentValue = self.currentValue if hasattr (self, 'currentValue') else 'not yet initialized'
				self.printTrace (lambda: 'Value before evaluation is {0}, {1}'.format (currentValue, recursionMessage.upper ()))
				raise FatalError (capitalize (recursionMessage))
			else:
				self.recursionCount += 1
				try:
					if hasattr (self, 'currentValue'):			#		If already initialised
#						if not transactor.contains (self):		#			If currentValue not already saved (prevent saving intermediate from follow)
#							self.previousValue = self.currentValue	#			Remember previousValue early to enable rollBack if getter raises exception
#							transactor.add (self)					#			Register that this node may alter its value as part of the current transaction
						
						self.printTrace (lambda: 'Value before evaluation is {0}'.format (self.currentValue))
						self.currentValue = self.getter ()		#			Compute currentValue, backpropagate if needed to evaluate getter
						self.printTrace (lambda: 'Value after evaluation is {0}'.format (self.currentValue))
					else:										#		If not yet initialized
						self.printTrace (lambda: 'Value before evaluation is not yet initialized')
						self.currentValue = self.getter ()		#			Dependent initialisation. backpropagate if needed to evaluate getter
						self.printTrace (lambda: 'Value after evaluation is {0}'.format (self.currentValue))
						self.previousValue = self.currentValue	#			Make sure previousValue is available in case of dependent initialisation
						
					self.event = currentEvent ()				#		Certainly currentValue is up to date at this point
					self.propagate ()							#		Forward propagation
				finally:											# Even if getter raises an exception
					self.recursionCount = 0							#	Re-enable evaluation
					
		self.printTrace (lambda: 'END evaluate', indent = '-')
		return self.currentValue						# Return possible updated currentValue
			
	def propagate (self):						# Forward propagation
		self.validate ()							#	Correct mistakes early, get report on changed node, rather than dependent one
		
		self.printTrace (lambda: 'Writing to {0} links'.format (len (self.links)))
		for link in self.links:						#	For each GUI element associated with this node
			link.write ()							#		Update that GUI element
		
		self.printTrace (lambda: 'Propagating to {0} sink nodes'.format (len (self.sinkNodes)))
		for sinkNode in self.sinkNodes:				#	For all sinkNodes
			if not sinkNode.recursionCount:			#		Unless sinkNode is already under evaluation
				sinkNode.evaluate ()				#			Make sure it evaluates, since no other node may ask it to
			else:
				sinkNode.printTrace (lambda: 'Propagate, blocked')					
									
	def act (self):						# Called at the end of transaction, to ensure updated values, e.g. on entering an event loop
		if not (type (self.new) == type (Pass) and self.new == Pass):
			if hasattr (self, 'action'):	# "Old style" single action functionality kept for backward compatibility
				self.action ()
				
			for action in self.actions:		# Perform all "new style" chainable actions associated with this node
				action ()
			
	new = property (evaluate)													# Reading property yields value of node after current event

	old = property (lambda self: ifExpr (self.event == currentEvent (),			# Reading property yields value of node before current event
		self.previousValue,
		self.currentValue
	))
				
	touched = property (lambda self: self.event in (currentEvent (), 0) and self.event != 1)
	triggered = property (lambda self: self is triggerNode ())
	
	def convert (self, convertibleValue):
		return getAsTarget (convertibleValue, self.currentValue.__class__)
	
	def change (self, convertibleValue = None, retrigger = False):					# Initiate a change
		if app.handlingNotification:
			return																	#	Forms.Message.Show causes a redundant LostFocus message, that trigger an extra call to Node.change
	
		transactor.clear ()															#	Start new transaction early, to make it work for conversion errors as well
		self.previousValue = self.currentValue										#	Save previousValue early to enable rollback. No problem if currentValue remains unaltered.
		transactor.add (self)														#	Even if currentValue remains unaltered, the GUI should possibly be rolled back
		
		try:
			convertedValue = self.convert (convertibleValue)
			
			if retrigger or self.currentValue == None or convertedValue != self.currentValue:	# If retrigger or value changed (Test for None added y15m02d07)
				triggerNode.value = self											#	Remember that this node started the propagation
				self.invalidate ()													#	Invalidate this node and dependent nodes
				self.event = currentEvent.getNext	()								#	Make this node valid

				self.printTrace (lambda: 'Event {0}, change from {1} to {2}'.format (self.event, self.currentValue, convertedValue), True)
				
				self.currentValue = convertedValue									#	Store new, converted value in this node
				self.propagate ()													#	Propagate new value to dependent nodes
				transactor.act ()													#	Late, since actions may need node values and may even enter event loops
			
		except Refusal as refusal:
			handleNotification (refusal)
			transactor.rollBack ()
			
		except Exception as exception:	# This is a barebones Python exception, so convert it to Eden exception
			handleNotification (Objection (exMessage (exception), report = exReport (exception)))
			transactor.rollBack ()
			
	def follow (self, convertibleValue = None, retrigger = False):
		if not transactor.contains (self):
			self.previousValue = self.currentValue
			transactor.add (self)
		
		convertedValue = self.convert (convertibleValue)
		
		if retrigger or self.currentValue == None or convertedValue != self.currentValue:	# (Test for None added y15m02d07)
			self.invalidate ()
			
			self.printTrace (lambda: 'Follow from {0} to {1}'.format (self.currentValue, convertedValue))
			self.currentValue = convertedValue									#	Store new, converted value in this node
			self.event = currentEvent ()										#	Make this node valid
			self.propagate ()													#	Propagate new value to dependent nodes
			
			# Don't call transactor.act here, since it would for the second time perform all actions
			# Since the new changed nodes are appended to the nodelist of the transaction, their actions are performed anyhow
						
	state = property (evaluate, lambda self, convertibleValue: self.follow (convertibleValue, True))
			
	def rollBack (self):						#	Restore previous state after exception in change of evaluate
		self.currentValue = self.previousValue		#	Restore previous value
		self.event = currentEvent ()				#	State is result of currentEvent, with a rollBack, even in case of a rollBack
		
		for link in self.links:						#	For each GUI element associated with this node
			link.write ()							#		Restore that GUI element
			
	def tagged (self, tag):
		self.tag = tag
		return self

class Link:	# Link between a node and a particular bareRead / bareWrite pair of the possible multiple bareRead / bareWrite pairs within a view
			# Maintains multiple reading / writing states per view so that e.g. caption can follow content
						
	def	__init__ (self, node, bareRead, bareWrite):					# Tie link to node and to bareRead / bareWrite pair
		node.links.append (self)										# Add this link to links of node
		
		self.bareRead = bareRead if bareRead else lambda params: None	# Remember bareRead
		self.reading = False											# Not busy reading
		
		self.bareWrite = bareWrite if bareWrite else lambda: None		# Remember bareWrite
		self.writing = False											# Not busy writing
		
		self.writeBack = True											# Allow this view to be written back to as result of reading it (auto formatting)
		
	def read (self, *params):				# Read info from this view into associated node
		if not self.writing:					# Prevent reading back half-written data, e.g. at re-checking items in a listView
			self.reading = True					#	Remember reading, to prevent writing while reading if no-writeback mode (see write method)
			self.bareRead (params)				#		Low level read from widget and / or event params
			self.reading = False				#	Remember not reading anymore
		
	def write (self):							# Write info from associated node to this view
		if self.writeBack or not self.reading:		# Prevent bareWrite as consequence of a read on the same view, if no-writeBack mode
			if not self.writing:					#	Prevent recursive bareWrite as side effect of node () call in bareWrite
				self.writing = True					#		Remember busy writing
				
				try:								#		If the widget is already instantiated
					self.bareWrite ()				#			Low level write to widget
				except AttributeError as e:				#		If widget is not yet instantiated (while passing parameters to execute)
					pass							#			Do nothing
				except TypeError:					#		If widget is not yet instantiated (while passing parameters to execute)
					pass							#			Do nothing
				except NameError, e:				#		!!! Tree drag&drop lifetime workaround
					print 'NameError in Link.write', str (e)
					
				self.writing = False				#		Remember not busy writing anymore
				
def getNode (valueOrNode, resultIfNone = None):
	if valueOrNode is None:	# e.g. valueOrNode == False should lead to condition == True
		return resultIfNone
	else:
		if valueOrNode.__class__ == Node:
			return valueOrNode
		else:	
			return Node (valueOrNode)
			
def trace (anObject, nodeName, indent = False):
	try:
		getattr (anObject, nodeName) .trace ('{}.{}'.format (anObject.__class__.__name__, nodeName), indent)
	except Exception as exception:
		# print 'Ad hoc trace registration failed: {}'.format (exception)
		pass

