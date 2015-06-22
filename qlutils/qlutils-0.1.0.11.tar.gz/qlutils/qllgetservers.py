import qllauncher
import json
import time
import sys
import os
import datetime
import argparse

__version__ = '0.1.0.1'

timeout_seconds = 30

def log_at_same_line(text):
    sys.stdout.write("\033[K")
    print(text, end='\r')

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('email', help='QuakeLive account email')
    parser.add_argument('password', help='QuakeLive account password')
    parser.add_argument('-v', nargs='?', default=os.getcwd())
    return parser.parse_args()

def main():
    args = parse_args()
    user = args.email
    password = args.password
    verbose = args.v
    
    if not verbose:
        print('Welcome to qllauncher server lister script ver %s' % __version__)
        print('The script is using qllauncher python library ver %s' % (qllauncher.__version__))
        print('It will show the list of servers spawned by user\n')

        log_at_same_line('Connecting to quakelive service (%s / %s)' % (user, password))
    connection = qllauncher.QLNetwork()
    connection.connect(user, password, False)

    if connection.is_connected:
        if not verbose:
            log_at_same_line('Connected...\n')
        server_data = connection.get_spawned_servers_list()
        if len(server_data):
            print(server_data)
        elif not verbose:
            log_at_same_line('No servers available')
    else:
        print('Not connected. Exiting.')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nStopped script.. Have a good day!')
        print('Please ask for a help the author of this script, Victor Polevoy = contact@vpolevoy.com')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

