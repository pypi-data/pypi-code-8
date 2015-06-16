import qllauncher
import json
import time
import sys
import os
import datetime

__version__ = '0.1.0.7'

print('Welcome to qllauncher server observer script ver %s' % __version__)
print('It will check for server.json file in current directory and will spawn a server with these settings\nPress CTRL-C to exit\n')

user = ''
password = ''
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

def main():
    log_at_same_line('Connecting to quakelive service (%s / %s)' % (user, password))
    connection = qllauncher.QLNetwork()
    connection.connect(user, password, False)

    if connection.is_connected:
        log_at_same_line('Connected...')
        while True:
            server_data = connection.get_spawned_servers_list()
            if not server_data:
                with open('server.json') as server_settings_file:
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

