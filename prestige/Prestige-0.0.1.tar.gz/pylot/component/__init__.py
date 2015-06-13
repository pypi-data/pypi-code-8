import re
import warnings
import humanize
import jinja2
import mistune
from pylot import (Pylot, utils)
from flask_kvsession import KVSessionExtension
import ses_mailer
import flask_mail
from flask_cloudstorage import Storage
from flask_recaptcha import ReCaptcha
from flask_seasurf import SeaSurf
import flask_cache
from six.moves.urllib.parse import urlparse

class Mailer(object):
    """
    A simple wrapper to switch between SES-Mailer and Flask-Mail based on config
    """
    mail = None
    provider = None
    app = None

    def init_app(self, app):

        self.app = app
        provider = app.config.get("MAILER_PROVIDER", None)

        if provider:
            self.provider = provider.upper()

            if self.provider == "SES":
                class _App(object):
                    config = {
                        "SES_AWS_ACCESS_KEY": app.config.get("MAILER_SES_ACCESS_KEY"),
                        "SES_AWS_SECRET_KEY": app.config.get("MAILER_SES_SECRET_KEY"),
                        "SES_SENDER": app.config.get("MAILER_SENDER"),
                        "SES_REPLY_TO": app.config.get("MAILER_REPLY_TO"),
                        "SES_TEMPLATE": app.config.get("MAILER_TEMPLATE"),
                        "SES_TEMPLATE_CONTEXT": app.config.get("MAILER_TEMPLATE_CONTEXT")
                    }
                _app = _App()
                self.mail = ses_mailer.Mail(app=_app)

            elif self.provider == "SMTP":
                uri = app.config.get("MAILER_SMTP_URI", None)
                if uri is None:
                    raise ValueError("<Pylot:Component:Mailer: MAILER_SMTP_URI is empty'")

                parse_uri = urlparse(uri)
                if "smtp" not in parse_uri.scheme:
                    raise ValueError("<Pylot:Component:Mailer: MAILER_SMTP_URI must start with 'smtp://'")

                class _App(object):
                    config = {
                        "MAIL_SERVER": parse_uri.hostname,
                        "MAIL_USERNAME": parse_uri.username,
                        "MAIL_PASSWORD": parse_uri.password,
                        "MAIL_PORT": parse_uri.port,
                        "MAIL_USE_TLS": True if "tls" in parse_uri.scheme else False,
                        "MAIL_USE_SSL": True if "ssl" in parse_uri.scheme else False,
                        "MAIL_DEFAULT_SENDER": app.config.get("MAILER_SENDER"),
                        "TESTING": app.config.get("TESTING"),
                        "DEBUG": app.config.get("DEBUG")
                    }
                    debug = app.config.get("DEBUG")
                    testing = app.config.get("TESTING")

                _app = _App()
                self.mail = flask_mail.Mail(app=_app)

            else:
                raise warnings.warn("<Pylot:Component:Mailer invalid provider '%s'>" % provider)

    def send(self, to, subject, body, reply_to=None, **kwargs):
        """
        Send simple message
        """
        if self.provider == "SES":
            self.mail.send(to=to,
                           subject=subject,
                           body=body,
                           reply_to=reply_to,
                           **kwargs)

        elif self.provider == "SMTP":
            print body
            msg = flask_mail.Message(recipients=[to] if not isinstance(to, list) else to,
                                     subject=subject,
                                     body=body,
                                     reply_to=reply_to,
                                     sender=self.app.config.get("MAILER_SENDER"))
            self.mail.send(msg)

    def send_template(self, template, to, reply_to=None, **context):
        """
        Send Template message
        """
        if self.provider == "SES":
            self.mail.send_template(template=template,
                                    to=to,
                                    reply_to=reply_to,
                                    **context)

        elif self.provider == "SMTP":
            _template = self.app.config.get("MAILER_TEMPLATE", None)
            template_context = self.app.config.get("MAILER_TEMPLATER_CONTEXT")

            ses_mail = ses_mailer.Mail(template=_template,
                                       template_context=template_context)
            data = ses_mail.parse_template(template=template, **context)

            msg = flask_mail.Message(recipients=[to] if not isinstance(to, list) else to,
                                     subject=data["subject"],
                                     body=data["body"],
                                     reply_to=reply_to,
                                     sender=self.app.config.get("MAILER_SENDER")
                                     )
            self.mail.send(msg)

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

class SocialAuth(object):

    def init_app(self, app):
        pass

mailer = Mailer()
cache = flask_cache.Cache()
storage = Storage()
recaptcha = ReCaptcha()
csrf = SeaSurf()

Pylot.bind(Session)
Pylot.bind(mailer.init_app)
Pylot.bind(storage.init_app)
Pylot.bind(cache.init_app)
Pylot.bind(recaptcha.init_app)
Pylot.bind(csrf.init_app)


# ------------------------------------------------------------------------------

def to_date(dt, format="%m/%d/%Y"):
    return "" if not dt else dt.strftime(format)

def strip_decimal(amount):
    return amount.split(".")[0]

def bool_to_yes(b):
    return "Yes" if b is True else "No"

def bool_to_int(b):
    return 1 if b is True else 0

def nl2br(s):
    """
    {{ s|nl2br }}

    Convert newlines into <p> and <br />s.
    """
    if not isinstance(s, basestring):
        s = str(s)
    s = re.sub(r'\r\n|\r|\n', '\n', s)
    paragraphs = re.split('\n{2,}', s)
    paragraphs = ['<p>%s</p>' % p.strip().replace('\n', '<br />') for p in paragraphs]
    return '\n\n'.join(paragraphs)


jinja2.filters.FILTERS.update({
    "currency": utils.to_currency,
    "strip_decimal": strip_decimal,
    "date": to_date,
    "int": int,
    "slug": utils.slug,
    "intcomma": humanize.intcomma,
    "intword": humanize.intword,
    "naturalday": humanize.naturalday,
    "naturaldate": humanize.naturaldate,
    "naturaltime": humanize.naturaltime,
    "naturalsize": humanize.naturalsize,
    "bool_to_yes": bool_to_yes,
    "bool_to_int": bool_to_int,
    "nl2br": nl2br,
    "markdown": mistune.markdown
})



