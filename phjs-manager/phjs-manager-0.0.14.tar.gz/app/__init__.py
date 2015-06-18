__author__ = 'michey'
from flask import Flask
from config_adapter import ConfigAdapter
from container_pool import ContainerPool
import sys

def run():
    app = Flask(__name__)
    
    
    config_path = sys.argv[0]
    config = ConfigAdapter(config_path)
    containers = ContainerPool(config.get_socket_path, config.get_image_path,
        config.get_run_command, config.get_start_port)
    
    @app.route('/run')
    def run_node():
        containers.instantiate_node()
        return "ok;"
    
    @app.route('/list')
    def list_node():
        return containers.get_node_list()
