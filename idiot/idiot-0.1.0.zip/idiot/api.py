import requests
import json
import resources

class APIClient():
	def __init__(self, auth=None, url='http://idiot-beta.herokuapp.com/api/'):
		self.url = url
		self.auth = auth

		if auth:
			self.me = self.login()

	def users(self, username=None):
		if username:
			# return a user object
			return resources.User(username, self.url, auth=self.auth)
		else:
			# return a users object
			return resources.Users(self.url, auth=self.auth)

	def login(self):
		return self.users('users/' + self.auth[0]).get()

if __name__ == '__main__':
	import sys
	api = API(auth=(sys.argv[1], sys.argv[2]), url=sys.argv[3])
	print('Hello, ' + api.me['username'])