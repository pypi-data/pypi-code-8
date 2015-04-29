from flask import send_from_directory
from os import path


__dot = path.dirname(path.realpath(__file__))
__asset_dir = path.join(__dot, '../../../assets')


def register_routes(blueprint):
    @blueprint.route('/assets/<path:path>')
    def serve_assets(path):
        return send_from_directory(__asset_dir, path)
