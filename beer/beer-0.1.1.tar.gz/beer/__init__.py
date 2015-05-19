import time

class SinTaxError(Exception):
	def __init__(self,message,errors=None):
		super().__init__(message)
		self.errors = errors

if time.localtime().tm_hour < 17:
	raise SinTaxError("It is not even 5 o'clock")
