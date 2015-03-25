import re

from flatland import String
from flatland.validation import (
    IsEmail,
    HTTPURLValidator,
    URLCanonicalizer,
    URLValidator,
    )
from flatland.validation.network import _url_parts

from tests._util import eq_, unicode_coercion_allowed


def email(value):
    return String(value, name=u'email', strip=False)


def assert_email_not_valid(value, kw={}):
    validator = IsEmail(**kw)
    el = email(value)
    assert not validator.validate(el, None)
    assert el.errors


def assert_email_valid(value, kw={}):
    validator = IsEmail(**kw)
    el = email(value)
    assert validator.validate(el, None)
    assert not el.errors


def test_email():
    for addr in (u'bob@noob.com', u'bob@noob.frizbit', u'#"$!+,,@noob.c',
                 u'bob@bob-bob.bob'):
        yield assert_email_valid, addr


def test_email_idna():
    with unicode_coercion_allowed():
        assert_email_valid(u'bob@snow\u2603man.com')


def test_email_non_local():
    assert_email_not_valid(u'root@localhost')


def test_email_non_local_ok():
    assert_email_valid(u'root@localhost', {'non_local': False})


def test_email_altlocal():
    override = dict(local_part_pattern=re.compile(u'^bob$'))
    assert_email_valid(u'bob@bob.com', override)
    assert_email_not_valid(u'foo@bar.com', override)


def test_email_bogus():
    c64 = u'x' * 64
    c63 = u'x' * 63
    for addr in (u'bob@zig..', u'bob@', u'@bob.com', u'@', u'snork',
                 u'bob@zig:zag.com', u'bob@zig zag.com', u'bob@zig/zag.com',
                 u' @zig.com', u'\t\t@zag.com',
                 u'bob@%s.com' % c64,
                 u'bob@%s.%s.%s.%s.com' % (c63, c63, c63, c63),
                 u'foo.com', u'bob@bob_bob.com', u''):
        yield assert_email_not_valid, addr


def scalar(value):
    return String(value, name=u'test')


def test_url_validator_default():
    v = URLValidator()
    el = scalar(u'http://me:you@there/path#fragment')
    assert v.validate(el, None)
    assert not el.errors


def test_url_validator_schemes():
    v = URLValidator(allowed_schemes=(), blocked_scheme='X')
    el = scalar(u'http://me:you@there/path#fragment')
    assert not v.validate(el, None)
    eq_(el.errors, [u'X'])

    v = URLValidator(allowed_schemes=('https',), blocked_scheme='X')
    el = scalar(u'http://me:you@there/path#fragment')
    assert not v.validate(el, None)
    eq_(el.errors, [u'X'])


def test_url_validator_parts():
    v = URLValidator(allowed_parts=(), blocked_part='X')
    el = scalar(u'http://me:you@there/path#fragment')
    assert not v.validate(el, None)
    eq_(el.errors, [u'X'])

    v = URLValidator(allowed_parts=_url_parts)
    el = scalar(u'http://me:you@there/path#fragment')
    assert v.validate(el, None)
    assert not el.errors

    v = URLValidator(allowed_parts=('scheme', 'netloc'))
    el = scalar(u'http://blarg')
    assert v.validate(el, None)
    assert not el.errors

    v = URLValidator(allowed_parts=('scheme', 'netloc'), blocked_part='X')
    el = scalar(u'http://blarg/')
    assert not v.validate(el, None)
    eq_(el.errors, [u'X'])


def test_http_validator_default():
    v = HTTPURLValidator(forbidden_part='X')
    el = scalar(u'http://there/path#fragment')
    assert v.validate(el, None)
    assert not el.errors

    el = scalar(u'http://phis:ing@there/path#fragment')
    not v.validate(el, None)
    eq_(el.errors, [u'X'])

    el = scalar('www.example.com')
    not v.validate(el, None)
    eq_(el.errors, ['test is not a valid URL.'])


def test_http_validator_schemes():
    v = HTTPURLValidator()
    el = scalar(u'http://there/path')
    assert v.validate(el, None)
    assert not el.errors

    el = scalar(u'//there/path')
    assert not v.validate(el, None)
    eq_(el.errors, ['test is not a valid URL.'])

    v = HTTPURLValidator(required_parts=dict(scheme=(u'https', u''),
                                             hostname=True))
    el = scalar(u'http://there/path')
    assert not v.validate(el, None)
    eq_(el.errors, [u'test is not a valid URL.'])

    el = scalar(u'https://there/path')
    assert v.validate(el, None)
    assert not el.errors
    el = scalar(u'//there/path')
    assert v.validate(el, None)
    assert not el.errors


def test_url_canonicalizer_default():
    v = URLCanonicalizer()
    el = scalar(u'http://localhost/#foo')
    eq_(el.value, u'http://localhost/#foo')

    assert v.validate(el, None)
    eq_(el.value, u'http://localhost/')
    assert not el.errors


def test_url_canonicalizer_want_none():
    v = URLCanonicalizer(discard_parts=_url_parts)
    el = scalar(u'http://me:you@there/path#fragment')
    eq_(el.value, u'http://me:you@there/path#fragment')

    assert v.validate(el, None)
    eq_(el.value, u'')
    assert not el.errors


def test_url_canonicalizer_want_one():
    v = URLCanonicalizer(discard_parts=_url_parts[1:])
    el = scalar(u'http://me:you@there/path#fragment')
    eq_(el.value, u'http://me:you@there/path#fragment')

    assert v.validate(el, None)
    eq_(el.value, u'http://')
    assert not el.errors


def test_url_canonicalizer_want_all():
    v = URLCanonicalizer(discard_parts=())
    el = scalar(u'http://me:you@there/path#fragment')
    eq_(el.value, u'http://me:you@there/path#fragment')

    assert v.validate(el, None)
    eq_(el.value, u'http://me:you@there/path#fragment')
    assert not el.errors
