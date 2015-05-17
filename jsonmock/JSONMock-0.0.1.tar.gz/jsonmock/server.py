__author__ = 'anass'

from flask import Flask, make_response, jsonify, request
import json
from JSONtoObject import wrap
from JSONtoObject.wrapper import Wrapper
from database import Database
from utils import path_to_property, dict_to_json
from default import id_tag, SLASH
from message import ERROR, NO_SUCH_RESOURCE, RESOURCE_EXISTS, \
    RESOURCE_NOT_EXISTS, BAD_REQUEST, NOT_FOUND, INFO, DELETED


app = Flask(__name__)
_database = None
_model = None
_CONFIG = None


@app.errorhandler(400)
def bad_request():
    return make_response(jsonify({ERROR: BAD_REQUEST}), 400)


@app.errorhandler(404)
def not_found():
    return make_response(jsonify({ERROR: NOT_FOUND}), 404)


# GET /
# Returns your JSON
@app.route('/', methods=['GET'])
def get_all():
    return jsonify(_model.to_json())


# GET /:resource
# GET /:resource/:id
# GET /:what/:ever/:you/:want
@app.route('/<path:path>', methods=['GET'])
def get(path):
    # No control in path variable, we'll just keep it simple
    # We'll add a regex
    try:
        key, value = path_to_property(_model, path.split(SLASH))
    except:
        return json.dumps({ERROR: NO_SUCH_RESOURCE})

    if isinstance(value, Wrapper):
        return json.dumps(value.to_json())
    if isinstance(value, list):
        return json.dumps([v.to_json() for v in value])
    return json.dumps({key: value})


# POST /:resource
# NEXT POST /  (add table)
@app.route('/<path:path>', methods=['POST'])
def create(path):
    global _database

    # Tests id the element exists
    value = path_to_property(_model, path.split(SLASH))[1]
    if request.form[id_tag] in [obj.get(id_tag) for obj in value]:
        return jsonify({ERROR: RESOURCE_EXISTS}), 201

    # Return response and save state of the database
    res = dict_to_json(request.form)
    value.append(wrap(res))

    _database.save()
    return jsonify(res), 201


# PUT /:resource/:id
@app.route('/<path:path>', methods=['PUT'])
def update(path):
    # tests if the resource exists
    global _database
    try:
        value = path_to_property(_model, path.split(SLASH))[1]
    except:
        return jsonify({ERROR: RESOURCE_NOT_EXISTS}), 201

    res = dict_to_json(request.form)

    # update value
    resources = path_to_property(_model, path.split(SLASH)[:-1])[1]
    resources.remove(value)
    resources.append(wrap(res))

    # save database into file
    _database.save()

    return jsonify(res), 201


# DELETE /:resource/:id
# DELETE /:resource
@app.route('/<path:path>', methods=['DELETE'])
def delete(path):
    # tests if the resource exists
    global _database, _model
    try:
        key, value = path_to_property(_model, path.split(SLASH))
    except:
        return jsonify({ERROR: RESOURCE_NOT_EXISTS}), 201

    if len(path.split(SLASH)) is 1:
        resources = _model
    else:
        resources = path_to_property(_model, path.split(SLASH)[:-1])[1]

    if isinstance(resources, Wrapper):
        resources.__delattr__(key)
        _database.save()
        return jsonify({INFO: DELETED}), 201

    elif isinstance(resources, list):
        resources.remove(value)

        _database.save()
        return jsonify({INFO: DELETED}), 201
    else:
        resources.remove(value)

        _database.save()
        return jsonify({INFO: DELETED}), 201


def serve(json_file, tag_id=None):
    init(json_file, tag_id)
    app.run()


def init(json_file, tag_id=None):
    global _database, _model, id_tag
    if tag_id:
        id_tag = tag_id
    _database = Database(json_file)
    _model = _database.data
