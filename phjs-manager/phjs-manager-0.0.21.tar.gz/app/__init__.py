__author__ = 'michey'
from flask import Flask
from config_adapter import ConfigAdapter
from container_pool import ContainerPool
from multiprocessing import Pool
import sys

def run():
    pool = Pool(processes=1)
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
        pool.apply_async(containers.instantiate_node, [])
        return 'ok;'

    app.run(port=config.get_bind_port())
