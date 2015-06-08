#!flask/bin/python
from flask import Flask, jsonify, request
from test import *


app = Flask(__name__)


@app.route('/lang_id', methods=['POST'])
def identifyLanguage():
    if not request.json or not 'text' in request.json:
        abort(400)
    ID = getLangID(request.json['text'])
    return jsonify({'lang': ID}), 201


if __name__ == '__main__':
    app.run(debug=True)

"""
curl -i -H "Content-Type: application/json" -X POST -d '{"text":""}' http://localhost:5000/lang_id
"""