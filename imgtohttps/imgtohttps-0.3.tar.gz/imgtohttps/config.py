class Config:
    DEBUG = False
    TESTING = False
    REDIS_URL = None
    IMGUR_CLIENT_ID = ''
    IMGUR_CLIENT_SECRET = ''


class Development(Config):
    DEBUG = True
    JSONIFY_PRETTYPRINT_REGULAR = True
    REDIS_URL = 'redis://localhost:6379/0'


class Production(Config):
    JSONIFY_PRETTYPRINT_REGULAR = False
    REDIS_URL = 'redis://localhost:6379/1'
