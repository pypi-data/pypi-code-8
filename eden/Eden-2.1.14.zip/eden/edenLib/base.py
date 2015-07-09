# Copyright (C) 2005 - 2014 Jacques de Hooge, Geatec Engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.

import os
import warnings

warnings.simplefilter ('error', RuntimeWarning)	# Turn all warnings into errors

class Anything (object):
	pass
	
class Nothing (object):	# If a node is initialized by this class as value, it is considered uninitialized
	pass
	
class Pass (object):	# When a node has this class as value, its action will not be executed
	pass
	
class Application (Anything):	
	def setDebug (self, switch):
		self.logNotifications = switch
		self.setDebugExtra (switch)
		
	debug = property (None, setDebug)
		
application = Application ()
app = application

application.edenLibDirectory = os.path.dirname (os.path.abspath (__file__)) .replace ('\\', '/')
application.edenDirectory = '/'.join (application.edenLibDirectory.split ('/')[:-1])
application.platform = ['Kivy']
