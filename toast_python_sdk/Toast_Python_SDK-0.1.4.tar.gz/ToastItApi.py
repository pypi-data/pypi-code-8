import logging
import json
from nap.url import Url
from SklItem import SklItem
from datetime import datetime

class ToastItApi:
	"""Toast-it.io API"""
	def __init__(self,url):
		self.apiUrl = url
		self.api = Url(self.apiUrl)
		self.jsonHeader = {'Content-type': 'application/json'}

	def GetAllNew(self):
		# Get scenes
		allScenes = self.GetAll()
		newScenes = []

		for scene in allScenes:
			isNew = True
			
			if scene.status == 'PENDING':
				newScenes.append(scene)

		return newScenes

	def GetAllNewForGenerator(self,generatorName):
		# Get scenes
		newScenes = self.GetAllNew()
		scenes = []

		for scene in newScenes:
			isNew = True
			
			if scene.generator == generatorName:
				scenes.append(scene)

		return scenes

	def GetAll(self):
		# Get scenes
		scenes = self.api.get('scene-requests').json()

		sceneObjs = []

		for scene in scenes:
			logging.debug(scene)
			item = SklItem(scene['sceneID'],scene['createdAt'],scene['resourceURI'])
			item.status = scene['status']
			item.generator = scene['generatorName']
			logging.info('Found item with resource location "%s"',item.resourceURL)

			sceneObjs.append(item)

		return sceneObjs

	def StartProcessing(self, sklItem):
		response = self.api.put('scene-requests/%s/%s' % (sklItem.id,sklItem.timestamp), data=json.dumps({'status': 'IN_PROGRESS'}),headers=self.jsonHeader)
		
		if response.status_code != 200:
			raise Exception('Creating a new process in the skeleton API failed. Received %s status code',response.status_code)

		logging.debug("Starting to process %s",sklItem.id)

		return

	def FailProcessing(self,sklItem):
		response = self.api.put('scene-requests/%s/%s' % (sklItem.id,sklItem.timestamp), data=json.dumps({'status': 'FAILED'}),headers=self.jsonHeader)
		
		if response.status_code != 200:
			raise Exception('Creating a new process in the skeleton API failed. Received %s status code',response.status_code)

		logging.debug("Starting to process %s",sklItem.id)

		return

	def CompleteProcessing(self,sklItem):
		logging.debug('Completing process %s',sklItem.id)

		response = self.api.post('scenes', data=json.dumps({'request':{ 'sceneID':sklItem.id,'createdAt':sklItem.timestamp }, 'result':{ 'URI':sklItem.resultURL, 'type':'IMAGE', 'thumbnailURI':sklItem.thumbnailURL }}),headers=self.jsonHeader)
		
		if response.status_code != 201:
			raise Exception('Completing item %s; failed with status code %s' % (sklItem.id,response.status_code))

		logging.debug(response)