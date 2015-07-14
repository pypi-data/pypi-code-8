import hashlib
import configparser
import uuid

class HashWrapper:
	def getDefaultHashAlgorithm(self):
		objConfigParser = configparser.ConfigParser()
		objConfigParser.read_file(open(r'hashwrapper.config'))
		return objConfigParser.get('Default Settings','default_hash_Algorithm')	

	def getDefaultSaltGenerator(self):
		objConfigParser = configparser.ConfigParser()
		objConfigParser.read_file(open(r'hashwrapper.config'))
		return objConfigParser.get('Default Settings','default_salt_generator')

	def getHash(self, stringToHash, hashName):
		## Set the encoding for the input string
		toHash = stringToHash.encode('utf-8')			
		## Get Salt
		cur_Salt = self.getSalt().encode('utf-8')
		## Generate the hash after concatenating the plaint text string with the salt string
		if hashName == 'sha1':
			varHash = hashlib.sha1(toHash+cur_Salt).hexdigest()
		elif hashName == 'sha224':
			varHash = hashlib.sha224(toHash+cur_Salt).hexdigest()
		elif hashName == 'sha256':
			varHash = hashlib.sha256(toHash+cur_Salt).hexdigest()
		elif hashName == 'sha384':
			varHash = hashlib.sha384(toHash+cur_Salt).hexdigest()
		elif hashName == 'sha512':
			varHash = hashlib.sha512(toHash+cur_Salt).hexdigest()
		elif hashName == 'md5':
			varHash = hashlib.md5(toHash+cur_Salt).hexdigest()
		else:
			varHash = "Error Generating the hash value."
		## Build the dictionary to return
		resDict = {'hash': varHash, 'salt': cur_Salt.decode("utf-8")}
		return resDict 

	def generateHash(self,toHash, hashAlg):
		## Define a Dict to hold the return value
		hashAndSaltDict = dict
		## Validations for stringToHash
		if toHash is not None:
			## Validations for hashAlg
			if hashAlg is not None:
				if hashAlg in hashlib.algorithms_guaranteed:
					## Use the user provided algorithm for generating the hash for the current pass
					hashAndSaltDict = self.getHash(toHash,hashAlg)
				else:
					## Use the default algorithm for generating the hash for the current pass
					hashAndSaltDict = self.getHash(toHash,self.getDefaultHashAlgorithm())
		return hashAndSaltDict	
						
	def getSalt(self):
		return str(uuid.uuid4())

