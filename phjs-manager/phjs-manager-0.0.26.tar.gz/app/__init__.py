__author__ = 'michey'
from flask import Flask
from config_adapter import ConfigAdapter
from container_pool import ContainerPool
from multiprocessing import Process
import sys

def ok():
    print("ok")

def run():
    app = Flask(__name__)
    config_path = sys.argv[1]
    config = ConfigAdapter(config_path)
    containers = ContainerPool(config.get_socket_path(), config.get_container(),
        config.get_run_command(), config.get_start_port())

    @app.route('/check')
    def check():
        return 'ok;'

    @app.route('/add_node')
    def add_node():
        p = Process(target=containers.instantiate_node)
        p.start()
        return 'ok;'

    app.run(port=config.get_bind_port())
