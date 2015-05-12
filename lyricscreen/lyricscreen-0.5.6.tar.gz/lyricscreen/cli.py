import optparse, sys, os, threading, signal, asyncio, time, argparse

from queue import Queue

from .wsserver import WebSocketServer
from .httpserver import WebClientServer
from .playlist import Playlist, playlists_dir
from .settings import Settings, default_settings_file

import lyricscreen

parser = argparse.ArgumentParser(description="A lyrics management and display web app and server")

parser.add_argument("-v", "--version", action="version", version="%(prog)s v" + lyricscreen.__version__)
parser.add_argument("-vv", "--verbose", help="show all available program output", action="store_true")
parser.add_argument("--default-config", help="display the default config file", action="store_true")
parser.add_argument("--show-config", help="print the values of the given or default config file", action="store_true")
parser.add_argument("--create-config", help="create the default config file", action="store_true")
parser.add_argument("CONFIG", help="the .json file to load config variables from", nargs="?", default=default_settings_file)

def main():
    # Handle some cli flags
    args = parser.parse_args()

    # Show default config contents
    if args.default_config:
        settings = Settings('')
        print(settings.settings_json())
        sys.exit(0)

    # Create default config
    if args.create_config:
        settings = Settings('')
        settings.save(default_settings_file)
        print("Created config file at %s" % settings.file)
        sys.exit(0)

    settings = Settings(args.CONFIG)

    # Show current config settings
    if args.show_config:
        print(settings.settings_json())
        sys.exit(0)

    # Get event loop for websocket server
    loop = asyncio.get_event_loop()

    # Create server objects
    websocket_server = WebSocketServer(settings, loop=loop)
    http_server = WebClientServer(settings)

    # Create server threads
    websocket_server_thread = threading.Thread(target=websocket_server.start)
    http_server_thread = threading.Thread(target=http_server.start)
    websocket_server_thread.daemon = True
    http_server_thread.daemon = True

    # Start threads
    websocket_server_thread.start()
    http_server_thread.start()

    # Create thread queue
    q = Queue()

    # Put threads in queue
    q.put(websocket_server_thread)
    q.put(http_server_thread)

    # Run async event loop
    time.sleep(0.1)
    loop.run_until_complete(websocket_server.sock)
    loop.run_forever()

    # Halt program until threads have run
    q.join()

