from __future__ import print_function
import base64
import getpass


def gen_basic_credentials(username, password):
    return base64.b64encode(username + ":" + password)


def main():
    username = raw_input("username:")
    password = getpass.getpass("password:")
    print(gen_basic_credentials(username, password))
