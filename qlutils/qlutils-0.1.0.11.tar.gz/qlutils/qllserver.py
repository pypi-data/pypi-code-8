import qllauncher
import json
import time
import sys
import os
import datetime
import argparse

__version__ = '0.1.0.9'

print('Welcome to qllauncher server observer script ver %s' % __version__)
print('The script is using qllauncher python library ver %s' % (qllauncher.__version__))
print('It will try to spawn and keep alive a quakelive server with settings from specified file\nPress CTRL-C to exit\n')

timeout_seconds = 30

def log_at_same_line(text):
    sys.stdout.write("\033[K")
    print(text, end='\r')

def timer_progress(word):
    starttime=time.time()
    seconds_spent = 0
    while True:
        progress_str = '[%s%s] next %s in %d seconds'
        seconds_spent += 1
        seconds_remaining = timeout_seconds - seconds_spent
        progress_str = progress_str % ('#' * seconds_spent, ' ' * seconds_remaining, word, seconds_remaining)
        log_at_same_line(progress_str)
        time.sleep(1.0 - ((time.time() - starttime) % 1.0))
        if seconds_spent >= timeout_seconds:
            break
    sys.stdout.write("\033[K")

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('email', help='QuakeLive account email')
    parser.add_argument('password', help='QuakeLive account password')
    parser.add_argument('settings_file', help='QuakeLive json server settings file')
    return parser.parse_args()

def main():
    args = parse_args()
    user = args.email
    password = args.password
    server_settings_file_name = args.settings_file
    if not os.path.exists(server_settings_file_name):
        print('Settings file does not exists: %s' % server_settings_file_name)
        sys.exit(1)

    log_at_same_line('Connecting to quakelive service (%s / %s)' % (user, password))
    connection = qllauncher.QLNetwork()
    connection.connect(user, password, False)

    if connection.is_connected:
        log_at_same_line('Connected...')
        while True:
            server_data = connection.get_spawned_servers_list()
            if not server_data:
                try:
                    with open(server_settings_file_name) as server_settings_file:
                        print('Server does not exists, spawning new one')
                        server_json = json.load(server_settings_file)
                        if server_json:
                            try:
                                print(connection.spawn_server_with_settings(server_json))
                            except KeyError as e:
                                print('QuakeLive service error: %s.' % str(e))
                                timer_progress('spawn attempt')
                        else:
                            print('Server file does not exists or empty')
                except FileNotFoundError as e:
                    print('File open error: %s' % str(e))
            else:
                st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                print('[%s] Server is up. Players: %d/%d' % (st, server_data[0]['num_players'], server_data[0]['max_clients']))
            timer_progress('check')
    else:
        print('Not connected')

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

