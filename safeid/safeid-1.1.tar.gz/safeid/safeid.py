"""
SafeID interacts with a Pythia PRF service to encrypt and verify passwords.
"""
import json, sys
from common import *
from httpJson import ServiceException, fetch, extract

from pythiacrypto.ecoprf import EcOprf
from pythiacrypto.groups import ec224

queryUrlTemplate = "https://remote-crypto.io/pythia/oquery-ecc?w={}&t={}&m={}"
prf = EcOprf(ec224, serialize=True)


def new(password, clientId=None):
	"""
	Encrypts a new @password by interacting with the Pythia service.
	@clientId: If specified, this value is used. If omitted, a suitable 
	           value is selected.

	@returns a tuple of required values to verify the password: (w,t,z,p) 
	 where:
		@w: client ID (key selector)
		@t: tweak (randomly generated user ID)
		@z: protected passwords
		@p: server public key bound to clientId - used to verify future
		    proofs from this server.
	"""
	# Set the client ID
	if not clientId:
		w = secureRandom()
	else:
		w = clientId

	# Generate a random tweak t
	t = secureRandom()
	z,p = query(password, w, t)
	return w, t, z, p


def check(password, w, t, z, p):
	"""
	Checks an existing @password against the Pythia server using the 
	values (w,t,z,p).
	@returns: True if the password passes authentication; False otherwise.
	"""
	zPrime,_ = query(password, w, t, p)
	return z == zPrime


def query(password, w, t, previousPubkey=None):
	"""
	Queries the a Pythia PRF service and verifies the server's ZKP.
	@returns (z,p) where: @z is the encrypted password and @p is the
		server's pubkey bound to clientId

	Raises an exception if there are any problems interacting with the service
		or if the server's ZKP fails verification.
	"""
	# Blind the password
	r,m = prf.wrapMessage(password)

	# Query the service via HTTP(S) GET
	response = fetch(queryUrlTemplate.format(w,t,m))

	# Grab the required fields from the response.
	p,y,c,u = extract(response, ["p","y","c","u"])

	# Verify ZKP 
	prf.verifyZkp(w, t, m, p, y, c, u, previousPubkey)

	# Deblind the result
	z = prf.unwrapResponse(r,y)

	# Return the important fields.
	return (z,p)


def main():
	"""
	Command line interface to SafeID
	"""
	if len(sys.argv) < 3:
		printUsage()
		return

	# Grab first two arguments
	command, pw = sys.argv[1:3]

	# Run the expected command

	# New password
	if command == "new":
		print json.dumps(new(pw))

	# Check existing password
	elif command == "check" and len(sys.argv) == 4:
		# Parse the encrypted password
		w,t,z,p = json.loads(sys.argv[3])

		# Check the password
		if check(pw, w,t,z,p):
			print  "Password is authentic"
		else:
			print "Invalid password "

	else:
		printUsage()


def printUsage():
	print "Usage: "
	print "safeid new 'passphrase'"
	print "safeid check 'passphrase' '[protected passphrase]'".format(sys.argv[0])
	print
	print "COMMANDS"
	print "new\t Takes a new passphrase and produces a protected passphrase that is a JSON list."
	print "check\t Checks a given passphrase against an existing protected passphase (JSON list)."


# Run!
if __name__ == "__main__":
	main()



