__author__ = 'michey'
from flask import Flask
from config_adapter import ConfigAdapter
from container_pool import ContainerPool
import sys

def run():
    app = Flask(__name__)


    config_path = sys.argv[1]
    config = ConfigAdapter(config_path)
    containers = ContainerPool(config.get_socket_path(), config.get_container(),
        config.get_run_command(), config.get_start_port())

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    @app.route('/check')
    def check():
        return 'ok;'

    @app.route('/add_node')
    def add_node():
        containers.instantiate_node()
        return 'ok;'

    @app.route('/list_node')
    def list_node():
        return containers.get_node_list()

    app.run(port=config.get_bind_port())
