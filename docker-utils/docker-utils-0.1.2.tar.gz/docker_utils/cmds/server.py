import json
import requests

import flask

app = flask.Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return flask.jsonify({})


@app.route('/hook', methods=['POST'])
def hook():
    data = flask.request.json
    response = {'state': 'success'}
    if 'callback_url' in data:
        requests.post(data['callback_url'],
                      data=json.dumps(response),
                      headers={'Content-Type': 'application/json'})
    return flask.jsonify(response)


@app.route('/status', methods=['GET'])
def status():
    return flask.jsonify({'status': 'trying my best'})


if __name__ == '__main__':
    app.run(debug=True)
