
import ses_mailer
import flask_mail

from portfolio.component import mailer, cache, storage

def test_mailer_none():
    assert mailer.mail is None

def test_mailer_ses():
    class FakeFlask(object):
        config = {
            "MAILER_PROVIDER": "SES",
            "MAILER_SES_ACCESS_KEY": "",
            "MAILER_SES_SECRET_KEY": ""
        }
    app = FakeFlask
    mailer.init_app(app)

    assert isinstance(mailer.mail, ses_mailer.Mail)

def test_mailer_smtp():
    class FakeFlask(object):
        config = {
            "MAILER_PROVIDER": "SMTP",
            "MAILER_SMTP_URI": "smtp://user:pass@mail.google.com:25",
            "DEBUG": False,
            "TESTING": False
        }
    app = FakeFlask()
    mailer.init_app(app)

    assert isinstance(mailer.mail, flask_mail.Mail)