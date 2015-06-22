"""
::PYLOT::

Base config file

"""
import os


CWD = os.path.dirname(__file__)

class Config(object):
    """
    Flask config: http://flask.pocoo.org/docs/0.10/config/
    """
    SERVER_NAME = None
    DEBUG = True
    SECRET_KEY = "PLEASE CHANGE ME"

    # ------

    APP_NAME = ""
    APP_VERSION = "0.0.1"

    #
    ADMIN_EMAIL = "admin@test.com"
    ADMIN_NAME = "Admin Test"

# ------- AWS CREDENTIALS ------------------------------------------------------

    #: AWS Credentials
    # For: S3, SES Mailer, flask s3
    AWS_ACCESS_KEY_ID = "AKIAIJ66SVCZPD4F3P6A"
    AWS_SECRET_ACCESS_KEY = "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"
    AWS_S3_BUCKET_NAME = "yoredis"

# ------- DATABASES ------------------------------------------------------------

    #: SQLAlchemy
    #: format: engine://USERNAME:PASSWORD@HOST:PORT/DB_NAME
    DATABASE_URI = "mysql+pymysql://root:mysqlAdminPass10@db-01.xnode.io:3306/test_pylot" #"sqlite://///Users/mardochee.macxis/Projects/Python/flask-pilot/test/app.db"

    #: REDIS
    #: format: USERNAME:PASSWORD@HOST:PORT
    REDIS_URI = None

# ------------------------------------------------------------------------------
    # WEBASSETS

    # Flask-Assets
    # http://flask-assets.readthedocs.org/
    ASSETS_DEBUG = False
    FLASK_ASSETS_USE_S3 = False

    # Flask-S3
    # https://flask-s3.readthedocs.org/en/v0.1.4/
    USE_S3 = False
    S3_BUCKET_DOMAIN = ""
    S3_BUCKET_NAME = AWS_S3_BUCKET_NAME
    S3_USE_HTTPS = False
    USE_S3_DEBUG = False
    S3_ONLY_MODIFIED = False

# ------------------------------------------------------------------------------

    #: SESSION
    #: Flask-KVSession is used to save the user's session
    #: Set the SESSION_URI to by using these examples below to set KVSession
    #: To use local session, just set SESSION_URI to None
    #:
    #: Redis: redis://username:password@host:6379/db
    #: S3: s3://username:password@s3.aws.amazon.com/bucket
    #: Google Storage: google_storage:username:password@cloud.google.com/bucket
    #: SQL: postgresql://username:password@host:3306/db
    #:      mysql+pysql://username:password@host:3306/db
    #:      sqlite://
    #: Memcached: memcache://host:port
    #:
    SESSION_URI = None

# ------------------------------------------------------------------------------

    #: CLOUDSTORAGE
    #: Flask-CloudStorage is used to save upload on S3, Google Storage,
    #: Cloudfiles, Azure Blobs, and Local storage
    #: When using local storage, they can be accessed via http://yoursite/files

    #: CLOUDSTORAGE_PROVIDER:
    # The provider to use. By default it's 'LOCAL'.
    # You can use:
    # LOCAL, S3, GOOGLE_STORAGE, AZURE_BLOBS, CLOUDFILES
    CLOUDSTORAGE_PROVIDER = "LOCAL"

    #: CLOUDSTORAGE_KEY
    # The storage key. Leave it blank if PROVIDER is LOCAL
    CLOUDSTORAGE_KEY = AWS_ACCESS_KEY_ID

    #: CLOUDSTORAGE_SECRET
    #: The storage secret key. Leave it blank if PROVIDER is LOCAL
    CLOUDSTORAGE_SECRET = AWS_SECRET_ACCESS_KEY

    #: CLOUDSTORAGE_CONTAINER
    #: The Bucket name (for S3, Google storage, Azure, cloudfile)
    #: or the directory name (LOCAL) to access
    CLOUDSTORAGE_CONTAINER = "uploads"

    #: CLOUDSTORAGE_ALLOWED_EXTENSIONS
    #: List of extensions to allow
    CLOUDSTORAGE_ALLOWED_EXTENSIONS = []

    #: CLOUDSTORAGE_LOCAL_PATH
    #: When POVIDER is LOCAL, the directory path where CONTAINER exists
    CLOUDSTORAGE_LOCAL_PATH = "%s/data" % CWD

    #: CLOUDSTORAGE_LOCAL_URL
    #: Url to access LOCAL file
    CLOUDSTORAGE_SERVE_FILES = True

    CLOUDSTORAGE_SERVE_FILES_URL = "files"

    #: CLOUDSTORAGE_SERVE_FILES_URL_SECURE
    #: Bool to serve files via http or https
    CLOUDSTORAGE_SERVE_FILES_URL_SECURE = False

    CLOUDSTORAGE_URI = "s3://{username}:{password}@s3.aws.amazon.com/{bucket}"\
        .format(username=AWS_SECRET_ACCESS_KEY,
                password=AWS_SECRET_ACCESS_KEY,
                bucket=AWS_S3_BUCKET_NAME)

# ------------------------------------------------------------------------------

    #: MAILER
    #: To send mail using AWS SES or SMTP
    #: You can send raw email, or templated email for convenience

    #: MAILER_PROVIDER
    #: The mailer provider SES or SMTP
    MAILER_PROVIDER = "SMTP"

    #: MAILER_SES_ACCESS_KEY
    #: For SES The AWS_ACCESS_KEY_ID
    MAILER_SES_ACCESS_KEY = AWS_ACCESS_KEY_ID

    #: MAILER_SES_SECRET_KEY
    #: For SES The AWS_SECRET_ACCESS_KEY
    MAILER_SES_SECRET_KEY = AWS_SECRET_ACCESS_KEY

    #: MAILER_SENDER - The sender of the email by default
    #: For SES, this email must be authorized
    MAILER_SENDER = "mcx2082@gmail.com"

    #: MAILER_REPLY_TO
    #: The email to reply to by default
    MAILER_REPLY_TO = "mcx2082@gmail.com"

    #: MAILER_TEMPLATE
    #: a directory that contains the email template or a dict
    MAILER_TEMPLATE = "%s/var/ses-mailer" % CWD

    #: MAILER_TEMPLATE_CONTEXT
    #: a dict of all context to pass to the email by default
    MAILER_TEMPLATE_CONTEXT = {
        "site_name": "MyTestSite.com",
        "site_url": "http://mytestsite.com"
    }

    #: MAILER_SMTP_URI
    #: The uri for the smtp connection. It will use Flask-Mail
    #: format: smtp://USERNAME:PASSWORD@HOST:PORT
    #: with sll -> smtp+ssl://USERNAME:PASSWORD@HOST:PORT
    #: with ssl and tls -> smtp+ssl+tls://USERNAME:PASSWORD@HOST:PORT
    MAILER_SMTP_URI = "smtp+ssl://{username}:{password}@{host}:{port}"\
        .format(username="",
                password="",
                host="smtp.gmail.com",
                port=465)

    #: PAGINATION_PER_PAGE : Total entries to display per page
    PAGINATION_PER_PAGE = 25

# ------------------------------------------------------------------------------

    #: CACHE
    #: Flask-Cache is used to caching

    #: CACHE_TYPE
    #: The type of cache to use
    #: null, simple, redis, filesystem,
    CACHE_TYPE = "simple"

    #: CACHE_REDIS_URL
    #: If CHACHE_TYPE is 'redis', set the redis uri
    #: redis://username:password@host:port/db
    CACHE_REDIS_URL = ""

    #: CACHE_DIR
    #: Directory to store cache if CACHE_TYPE is filesystem, it will
    CACHE_DIR = ""

# ------------------------------------------------------------------------------

    #: RECAPTCHA
    #: Flask-Recaptcha
    #: Register your application at https://www.google.com/recaptcha/admin

    #: RECAPTCHA_SITE_KEY
    RECAPTCHA_SITE_KEY = "6LchGgITAAAAAG-5mgaxR-5QFwtxt1OByvdOkQJV"

    #: RECAPTCHA_SECRET_KEY
    RECAPTCHA_SECRET_KEY = "6LchGgITAAAAAIHo1JDof2SFOaqD9YEFzwMb5w77"

# ------------------------------------------------------------------------------

    #: GOOGLE ANALYTICS ID
    GOOGLE_ANALYTICS_ID = ""


# ------------------------------------------------------------------------------

    USER_ACCOUNT_ENABLE_EMAIL_LOGIN = True
    USER_ACCOUNT_ENABLE_SIGNUP = True
    USER_ACCOUNT_RESET_PASSWORD_METHOD = "TOKEN"  # TOKEN | PASSWORD
    USER_ACCOUNT_ENABLE_AUTH_LOGIN = True
    USER_ACCOUNT_AUTH_CREDENTIALS = {
        "Facebook": {
            "consumer_key": "441928245975060",
            "consumer_secret": "7a071eb42c644ac4e764159717d230ef",
            'scope': ['profile', 'email']
        },
        "Google": {
            "consumer_key": "850751426566-0k11f44lno1ll2oirg9kaocnjerjeun2.apps.googleusercontent.com",
            "consumer_secret": "ycWttGng5FfcMjs1-GYJs2L4",
            'scope': ['profile', 'email']
        },

        "Twitter": {
            "consumer_key": "Gcha5nakjnKIWhKMHYDaolsFL",
            "consumer_secret": "liGXaiz7w9igDetd7aBzwUn1XjVxjeqCQLSWWVvrdT9vYWAf9O"
        },

        "WindowsLive": {
            "consumer_key": "402239969943888",
            "consumer_secret": ""
        },

        "UbuntuOne": {
            "consumer_key": "402239969943888",
            "consumer_secret": ""
        }
    }


# ----- LOGIN -----

    LOGIN_RESET_PASSWORD_METHOD = "TOKEN"  # PASSWORD | TOKEN

    LOGIN_EMAIL_ENABLE = True
    LOGIN_OAUTH_ENABLE = True
    LOGIN_SIGNUP_ENABLE = True
    LOGIN_OAUTH_CREDENTIALS = {
        "FACEBOOK": {
            "ENABLE": True,
            "CLIENT_ID": ""
        },
        "GOOGLE": {
            "ENABLE": True,
            "CLIENT_ID": ""
        },
        "TWITTER": {
            "ENABLE": False,
            "CLIENT_ID": ""
        }
    }

    # Maintenance
    # Turn maintenance page ON and OFF
    MAINTENANCE_ON = False

    # Contact
    # Email address for the contact page receipient
    CONTACT_PAGE_EMAIL_RECIPIENT = "mcx2082@gmail.com"


    COMPONENT_USER_ACCOUNT = {
        "email_login": True,

        "auth_login": True,

        "auth": {
            "Facebook": {

            }
        }
    }
class Development(Config):
    pass

class Production(Config):
    SECRET_KEY = None
