from __future__ import unicode_literals
from builtins import bytes, str

# Annoying warning at startup:
# https://github.com/pyca/pynacl/issues/62
# Fixed June 18th 2014.
from nacl.secret import SecretBox

# FIXME: doesn't look like the nacl.utils import is being used.
import nacl.utils
from random import randint
from os import urandom

from pbkdf2_ctypes import pbkdf2_bin

# A wrapper for NaCl's Secret Box, taking a user-supplied passphrase
# and deriving a secret key, rather than using a (far more secure)
# randomly generated secret key.
#
# NaCl Secret Box provides a high level interface for authenticated
# symmetric encryption.  When creating the box, you must supply a key.
# When using the box to encrypt, you must supply a random nonce.  Nonces
# must never be re-used.
#
# Secret Box decryption requires the ciphertext and the nonce used to
# create it.
#
# The PassphraseBox class takes a passphrase, rather than a randomly
# generated key. It uses PBKDF2 to generate a key that, while not random,
# is somewhat resistant to brute force attacks.  Great care should still
# be taken to avoid passphrases that are subject to dictionary attacks.

class PassphraseBox(object):

    ITERATIONS = 90000

    # Given passphrase and plaintext as strings, returns a dict
    # containing the ciphertext and other values needed for later
    # decryption.  Binary values are encoded as hexadecimal strings.
    @classmethod
    def encrypt(cls, passphrase, plaintext):
        box = cls(passphrase)
        return box._encrypt(plaintext)

    # encrypted = dict(salt=salt, nonce=nonce, ciphertext=ciphertext)
    # PassphraseBox.decrypt("my great password", encrypted)
    @classmethod
    def decrypt(cls, passphrase, encrypted):
        salt = encrypted['salt']
        iterations = encrypted['iterations']

        return cls(passphrase, salt, iterations)._decrypt(
            encrypted['ciphertext'], encrypted['nonce'])

    # Initialize with an existing salt and iterations to allow
    # decryption.  Otherwise, creates new values for these, meaning
    # it creates an entirely new secret box.
    def __init__(self, passphrase, salt=None, iterations=None):
        passphrase = passphrase.encode('utf-8')
        self.salt = salt.decode('hex') if salt else urandom(16)
        if iterations:
            self.iterations = iterations
        else:
            # per OWASP, use a random number of iterations between 90k and 110k
            self.iterations = self.ITERATIONS + randint(0,20000)

        key = pbkdf2_bin(passphrase,
                         salt=self.salt,
                         iterations=self.iterations,
                         keylen=32)

        self.box = SecretBox(key)


    def _encrypt(self, plaintext):
        plaintext = plaintext.encode('utf-8')
        nonce = urandom(SecretBox.NONCE_SIZE)
        encrypted = self.box.encrypt(plaintext, nonce)
        ciphertext = encrypted.ciphertext
        return dict(
            salt=self.salt.encode('hex'), iterations=self.iterations,
            nonce=nonce.encode('hex'), ciphertext=ciphertext.encode('hex')
        )

    def _decrypt(self, ciphertext, nonce):
        return self.box.decrypt(ciphertext.decode('hex'), nonce.decode('hex'))
