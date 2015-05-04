import requests
import json
import api
import datetime

class APIEndpoint(object):
	def __init__(self, url, auth):
		self.url = url
		self.auth = auth

	def get(self):
		return requests.get(self.url).json()
	
	def post(self, data):
		return requests.post(self.url, json=data.__dict__, auth=self.auth).json()

class Users(APIEndpoint):
	def __init__(self, url, auth):
		super(Users, self).__init__(url + 'users/', auth)

class User(APIEndpoint):

	def __init__(self, username, url, auth):
		self.username = username
		super(User, self).__init__(url + username, auth)

	def projects(self, project_name):
		if project_name:
			return Project(project_name, self.url, self.auth)
		else:
			return Projects(self.url, self.auth)

class Project(APIEndpoint):

	def __init__(self, name, url, auth):
		self.name = name
		super(Project, self).__init__(url + '/' + name, auth)

	def hubs(self, hub_id=None):
		if hub_id:
			return Hub(hub_id, self.url, self.auth)
		else:
			return Hubs(self.url, self.auth)

class Projects(APIEndpoint):

	def __init__(self, url, auth):
		super(Projects, self).__init__(url + '/projects', auth)

class Hub(APIEndpoint):

	def __init__(self, id, url, auth):
		self.id = id
		super(Hub, self).__init__(url + '/hubs/' + id, auth)

	def data_points(self):
		return DataPoints(self.url, self.auth)

class Hubs(APIEndpoint):
	def __init__(self, user, project, url, auth):
		self.user = user
		self.project = project
		super(Hubs, self).__init__(url + '/hubs', auth)

class DataPoint():
	def __init__(self, data, type):
		self.data = data
		self.dataType = type
		self.timeStamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

class DataPoints(APIEndpoint):
	def __init__(self, url, auth):
		super(DataPoints, self).__init__(url + '/datapoints', auth)