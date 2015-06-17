

class Event:
	"""A representation of an event in bangarang."""
	def __init__(self, metric=0.0, host="", service="", sub_service="", occurences=0, tags={}, status=0):
		self.host = host
		self.metric = metric
		self.service = service
		self.sub_service = sub_service
		self.occurences = occurences
		self.tags = tags
		self.status = status

	def json(self):
		import json
		return json.dumps(self.__dict__)
