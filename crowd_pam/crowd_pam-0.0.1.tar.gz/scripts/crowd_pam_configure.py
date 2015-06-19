#!/usr/bin/env python
from argparse import ArgumentParser
import json


def write_json_config(config_dict, filename):
    with open(filename, 'w') as f:
        json.dump(config_dict, f)


def main():
    parser = ArgumentParser(
        description='Generates a config for crowd_pam.'
    )
    parser.add_argument('-u', '--crowd_url', required=False,
        help="The Crowd server URL. Ex. http://localhost:8095"
    )
    parser.add_argument('-a', '--crowd_application', required=False,
        help="The Crowd application to authenticate users against"
    )
    parser.add_argument('-p', '--crowd_password', required=False,
        help="The password to authenticate against your Crowd application"
    )
    parser.add_argument('-l', '--logLevel', required=False, default="INFO",
        help="The log level for the PAM authentication module. Default is INFO"
    )
    parser.add_argument('-t', '--crowd_timeout', required=False, default=15,
        help="The timeout for retrieving user data from Crowd"
    )
    parser.add_argument('-f', '--filename', required=False, default="crowd_pam.conf",
        help="The file to write. Defaults to crowd_pam.conf in the current directory."
    )

    adata = vars(parser.parse_args())
    print adata
    if adata['crowd_url'] is None:
        adata['crowd_url'] = raw_input("Crowd URL: ")
    if adata['crowd_application'] is None:
        adata['crowd_application'] = raw_input("Crowd Application Name: ")
    if adata['crowd_password'] is None:
        adata['crowd_password'] = raw_input("Crowd Application Password: ")
    write_json_config(adata, adata.pop('filename'))


if __name__ == '__main__':
    main()
