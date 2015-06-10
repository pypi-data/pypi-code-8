import os
from flask import Flask, Blueprint, request, abort, current_app, jsonify
import redis
from sifr.span import Minute, Day, Month, Year, get_time_spans
from sifr.span import Hour
from sifr.storage import RedisStorage
from sifr.util import normalize_time

bp = Blueprint("sifr", __name__)

def span_from_resolution(resolution):
    return  {
        "minute": Minute,
        "hour": Hour,
        "day": Day,
        "month": Month,
        "year": Year
    }.get(resolution)



@bp.route("/count/<path:path>")
def count(path):
    keys = path.split("/")
    span = span_from_resolution(request.args.get("resolution"))
    if not span:
        abort(400)
    try:
        start = normalize_time(request.args.get("start"))
        end = normalize_time(request.args.get("end"))
    except:
        abort(400)
    time_spans = get_time_spans(start, end, keys, [span])
    return jsonify(
        dict(zip(
            [k.at.isoformat() for k in time_spans],
            [current_app.sifr.count(k) for k in time_spans]
        ))
    )

@bp.route("/cardinality/<path:path>")
def card(path):
    keys = path.split("/")
    span = span_from_resolution(request.args.get("resolution"))
    if not span:
        abort(400)
    try:
        start = normalize_time(request.args.get("start"))
        end = normalize_time(request.args.get("end"))
    except:
        abort(400)
    time_spans = get_time_spans(start, end, keys, [span])
    return jsonify(
        dict(zip(
            [k.at.isoformat() for k in time_spans],
            [current_app.sifr.cardinality(k) for k in time_spans]
        ))
    )


def create_application():
    app = Flask(__name__)
    app.register_blueprint(bp)
    if os.environ.get("SIFR_WS_CONFIG"):
        app.config.from_envvar("SIFR_WS_CONFIG")
    if not app.config.get("REDIS_URL"):
        raise Exception("Unable to start sifr webservice")
    app.sifr = RedisStorage(redis.from_url(app.config.get("REDIS_URL")))
    app.debug = True
    return app


