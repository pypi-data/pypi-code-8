import logging
import urllib.request

class SklItem:
	"""Skeleton Scene Item"""
	def __init__(self,sceneId,timestamp,resourceURL):
		self.id = sceneId
		self.timestamp = timestamp
		self.processes = []
		self.resourceURL = resourceURL

	def GetData(self):
		response = urllib.request.urlopen(self.resourceURL)

		readResponse = list(response.read())

		return readResponse
