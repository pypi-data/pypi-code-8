
from flask_kvsession import KVSessionExtension
from six.moves.urllib.parse import urlparse

class Session(object):
    """
    Use KVSession
    """
    def __init__(self, app):
        store = None
        uri = app.config.get("SESSION_URI")
        if uri:
            parse_uri = urlparse(uri)
            scheme = parse_uri.scheme
            username = parse_uri.username
            password = parse_uri.password
            hostname = parse_uri.hostname
            port = parse_uri.port
            bucket = parse_uri.path.strip("/")

            if "redis" in scheme:
                import redis
                from simplekv.memory.redisstore import RedisStore
                conn = redis.StrictRedis.from_url(url=uri)
                store = RedisStore(conn)
            elif "s3" in scheme or "google_storage" in scheme:
                from simplekv.net.botostore import BotoStore
                import boto
                if "s3" in scheme:
                    _con_fn = boto.connect_s3
                else:
                    _con_fn = boto.connect_gs
                conn = _con_fn(username, password)
                _bucket = conn.create_bucket(bucket)
                store = BotoStore(_bucket)
            elif "memcache" in scheme:
                import memcache
                from simplekv.memory.memcachestore import MemcacheStore
                host_port = "%s:%s" % (hostname, port)
                conn = memcache.Client(servers=[host_port])
                store = MemcacheStore(conn)
            elif "sql" in scheme:
                from simplekv.db.sql import SQLAlchemyStore
                from sqlalchemy import create_engine, MetaData
                engine = create_engine(uri)
                metadata = MetaData(bind=engine)
                store = SQLAlchemyStore(engine, metadata, 'kvstore')
                metadata.create_all()
            else:
                raise ValueError("Invalid Session Store")
        if store:
            KVSessionExtension(store, app)
