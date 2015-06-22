"""
Load and setup Flask extensions
"""

from portfolio import Portfolio
from flask_cloudstorage import Storage
from flask_recaptcha import ReCaptcha
from flask_seasurf import SeaSurf
import flask_cache
import session
import mailer

# Session
Portfolio.bind(session.Session)

# Cache
cache = flask_cache.Cache()
Portfolio.bind(cache.init_app)

# Storage
storage = Storage()
Portfolio.bind(storage.init_app)

# Mailer
mailer = mailer.Mailer()
Portfolio.bind(mailer.init_app)

# Recaptcha
recaptcha = ReCaptcha()
Portfolio.bind(recaptcha.init_app)

# CSRF
csrf = SeaSurf()
Portfolio.bind(csrf.init_app)



