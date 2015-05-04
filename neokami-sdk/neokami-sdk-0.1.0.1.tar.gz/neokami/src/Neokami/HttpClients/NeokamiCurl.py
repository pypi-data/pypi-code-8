''' Copyright 2015 Neokami GmbH. '''

import requests


class NeokamiHttpClient():


	def get(self, route, payload):
		r = requests.get(route, params=payload)

		return r

	def post(self, route, payload):
		r = requests.post(route, params=payload)
		return r

	def postBinary(self, route, bytestream, params={}):

		files = {'data':bytestream}
		r = requests.post(
					url=route,
                    data=params,
					files=files)

		return r

