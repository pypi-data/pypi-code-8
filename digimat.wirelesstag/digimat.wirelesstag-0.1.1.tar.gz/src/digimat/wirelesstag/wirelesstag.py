import json
import requests
import time
import pprint

# http://wirelesstag.net/media/mytaglist.com/apidoc.html

WIRELESSTAG_API_URL='https://www.mytaglist.com'

class Tag(object):
	def __init__(self, channel, data):
		self._channel=channel
		self._data={}
		self._stamp=0
		self.update(data)

	@property
	def channel(self):
	    return self._channel

	def update(self, data):
		if data:
			try:
				uuid=data['uuid']
				if uuid and (self.uuid is None or self.uuid==uuid):
					self._data=data
					self._stamp=time.time()
			except:
				pass

	def get(self, name, default=None):
		try:
			return self._data[name]
		except:
			return default

	def __getitem__(self, name):
		return self.get(name)

	@property
	def uuid(self):
	    return self.get('uuid')

	@property
	def name(self):
	    return self.get('name')

	@property
	def comment(self):
	    return self.get('comment')

	@property
	def battery(self):
	    return max(self.get('batteryRemaining', 0.0), 1.0)

	@property
	def temperature(self):
	    return self.get('temperature', 0.0)

	@property
	def hygrometry(self):
	    return self.get('cap', 0.0)

	def age(self):
		return time.time()-self._stamp

	def isAlive(self):
		if self.get('alive') and not self.get('OutOfRange') and self.age()<15*60:
			return True

	def dump(self):
		pprint.pprint(self._data)

	def __repr__(self):
		return 'Tag(%s/%s/%s) %s' % (self.uuid, self.name, self.comment, str(self._data))
		

class Channel(object):
	def __init__(self, authCode):
		self._authCode=authCode
		self._tags={}
		self._tagsIndexByName={}

	def api(self, service, method):
		if service and method:
			return '%s/%s' % (service, method)

	def apiEthClient(self, method):
		return self.api('ethClient.asmx', method)

	def do(self, api, data=None):
		if api and self._authCode:
			try:
				if not data:
					data={}

				headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % self._authCode}

				url='%s/%s' % (WIRELESSTAG_API_URL, api)
				# print url

				r=requests.post(url, headers=headers, data=json.dumps(data))
				if r:
					response=r.json()
					return response
			except:
				pass

	def doAndGetData(self, api, data=None):
		try:
			return self.do(api, data)['d']
		except:
			pass

	def getTagList(self):
		# http://wirelesstag.net/media/mytaglist.com/ethClient.asmx@op=GetTagList.html
		return self.doAndGetData(self.apiEthClient('GetTagList'))

	def tags(self):
		try:
			return self._tags.values()
		except:
			pass

	def tag(self, uuid):
		try:
			return self._tags[uuid.lower()]
		except:
			pass

	def tagFromName(self, name):
		try:
			return self._tagsIndexByName[name.lower()]
		except:
			pass

	def __getitem__(self, name):
		return self.tagFromName(name)

	def tagStore(self, data):
		try:
			uuid=data['uuid']
			if uuid:
				tag=self.tag(uuid)
				if tag:
					tag.update(data)
				else:
					tag=Tag(self, data)
					self._tags[tag.uuid]=tag
					if tag.name:
						self._tagsIndexByName[tag.name]=tag
				return tag
		except:
			pass

	def read(self):
		tags=self.getTagList()
		if tags:
			for data in tags:
				self.tagStore(data)


if __name__ == "__main__":
	pass


