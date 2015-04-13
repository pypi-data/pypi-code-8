from sinor import html_content
from nose.tools import assert_equals


def test_parse_empty_string():
    assert_equals(html_content.from_string(''), {'title': '',
                                           'date': '',
                                           'content': ''})


def test_finds_a_post_title_class():
    html = "<div><div id='post-title'>Title</div></div>"
    assert_equals(html_content.from_string(html), {'title': 'Title',
                                             'date': '',
                                             'content': ''})


def test_finds_a_post_date():
    html = "<div><time id='post-date'>2010-01-01</time></div>"
    assert_equals(html_content.from_string(html), {'date': '2010-01-01',
                                             'title': '',
                                             'content': ''})


def test_finds_post_content():
    html = '<div id="post-content"><p>Ulysseus!</p></div>'
    assert_equals(html_content.from_string(html), {'content': html,
                                             'title': '',
                                             'date': ''})


def test_multihtml():
    html = '<div><div id="post-content"><h1 id="post-title">Foo</h1><time id="post-date">2010-01-01</time></div></div>'
    assert_equals(html_content.from_string(html),
                  {'content':
                   '<div id="post-content"><h1 id="post-title">Foo</h1><time id="post-date">2010-01-01</time></div>',
                   'title': 'Foo',
                   'date': '2010-01-01'})
