#!/usr/bin/env python
import json
import logging
import sys
from jwkest.jwe import JWE

__author__ = 'rohe0002'

import argparse
import requests
from jwkest.jwk import RSAKey, keyrep, jwks_load
from jwkest.jwk import import_rsa_key_from_file
from jwkest.jwk import SYMKey
from jwkest.jws import JWS


def setup_logging(log_file):
    logger = logging.getLogger("")
    hdlr = logging.FileHandler(log_file)
    base_formatter = logging.Formatter(
        "%(asctime)s %(name)s:%(levelname)s %(message)s")
    hdlr.setFormatter(base_formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)


def assign(lst):
    keys = {}
    for typ, key in lst:
        try:
            keys[typ].append(key)
        except KeyError:
            keys[typ] = [key]
    return keys


def lrequest(url, method="GET", **kwargs):
    return requests.request(method, url, **kwargs)


def sign(msg, key, alg):
    _jws = JWS(msg, alg=alg)
    return _jws.sign_compact(key)


def verify(msg, keys):
    _jws = JWS()
    return _jws.verify_compact(msg, keys)


def encrypt(msg, keys, alg, enc):
    _jwe = JWE(msg, alg=alg, enc=enc)
    return _jwe.encrypt(keys)


def decrypt(msg, keys):
    _jwe = JWE()
    return _jwe.decrypt(msg, keys)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest="sign", action='store_true')
    parser.add_argument('-v', dest="verify", action='store_true')
    parser.add_argument('-e', dest="encrypt", action='store_true')
    parser.add_argument('-d', dest="decrypt", action='store_true')
    parser.add_argument('-f', dest="msg_file",
                        help="File containing a message")
    parser.add_argument('-r', dest="rsa_file",
                        help="File containing a RSA key")
    parser.add_argument('-k', dest="hmac_key",
                        help="If using a HMAC algorithm this is the key")
    parser.add_argument('-a', dest="alg",
                        help="The signing algorithm")
    parser.add_argument('-A', dest="encalg",
                        help="The encryption alg algorithm")
    parser.add_argument('-E', dest="encenc",
                        help="The encryption enc algorithm")
    parser.add_argument('-j', dest="jwk", help="JSON Web Key")
    parser.add_argument('-J', dest="jwks", help="JSON Web Keys")
    parser.add_argument('-i', dest="kid", help="key id")
    parser.add_argument('-l', dest="log", help="logfile name")
    parser.add_argument("message", nargs="?", help="The message")

    args = parser.parse_args()

    if args.log:
        setup_logging(args.log)

    _kid = args.kid
    keys = []
    if args.rsa_file:
        keys.append(RSAKey(key=import_rsa_key_from_file(args.rsa_file),
                           kid=_kid))
    if args.hmac_key:
        keys.append(SYMKey(key=args.hmac_key))

    if args.jwk:
        kspec = json.loads(open(args.jwk).read())
        keys.append(keyrep(kspec))

    if args.jwks:
        txt = open(args.jwks).read()
        keys.extend(jwks_load(txt))

    if not keys:
        exit(-1)

    if args.msg_file:
        message = open(args.msg_file).read().strip("\n")
    elif args.message == "-":
        message = sys.stdin.read()
    else:
        message = args.message

    if args.sign:
        _msg = sign(message, keys, args.alg)
        if args.encrypt:
            _msg = encrypt(_msg, keys, args.encalg, args.encenc)
        print _msg
    elif args.encrypt:
        print encrypt(message, keys, args.encalg, args.encenc)
    else:
        if args.decrypt:
            _msg = decrypt(message, keys)
        else:
            _msg = message

        if args.verify:
            print verify(_msg, keys)

# -e -J edmund.jwks -f text.json -E "A128CBC-HS256" -A "RSA1_5" -l ju.log
# -d -r op.key -f edmund.jwe -i a0