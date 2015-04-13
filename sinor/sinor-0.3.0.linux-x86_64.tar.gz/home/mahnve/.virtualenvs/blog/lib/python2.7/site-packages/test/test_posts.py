from nose.tools import assert_equals, assert_list_equal
from sinor import posts
from sinor.config import config
from mock import Mock
from data_builder import PostDataBuilder


def test_draft():
    draft = PostDataBuilder().with_status('draft').build()
    published = PostDataBuilder().with_status('published').build()
    assert_equals(posts.no_drafts([draft, published]), [published])


def test_limit_count():
    a = b = c = d = PostDataBuilder().build()
    plist = [a, b, c, d]
    assert_equals([a, b], posts.limit(plist, 2))


def test_limit_negative_count():
    a = b = c = d = PostDataBuilder().build()
    post_list = [a, b, c, d]
    assert_equals(post_list, posts.limit(post_list, -1))


def test_default_partial_dir():
    config.build_partials_dir = Mock(return_value='')
    assert_equals(posts.partials_dir("/foo/bar.mustache"), "/foo")


def test_selects_config_partial_dir():
    config.build_partials_dir = Mock(return_value="/bar")
    assert_equals(posts.partials_dir("/foo/bar.mustache"), "/bar")


def test_build_tags_list():
    a = PostDataBuilder().with_tags('bar', 'foo').with_title('a').build()
    b = PostDataBuilder().with_tags('foo').with_title('b').build()
    c = PostDataBuilder().with_tags('foo').with_title('c').build()
    d = PostDataBuilder().with_tags().with_title('d').build()
    tag_tree = posts.build_tag_tree([a, b, c, d])

    assert_equals(3,
                  len(posts.get_tag_dict(tag_tree, 'foo')['posts']))

    assert_equals(1,
                  len(posts.get_tag_dict(tag_tree, 'bar')['posts']))


def test_tag_list_is_sorted():
    b = PostDataBuilder().with_tags('foo').with_title('b').build()
    a = PostDataBuilder().with_tags('bar', 'foo').with_title('a').build()
    c = PostDataBuilder().with_tags('foo', 'aaa').with_title('c').build()
    d = PostDataBuilder().with_tags().with_title('d').build()
    tag_tree = posts.build_tag_tree([a, b, c, d])

    assert_equals(tag_tree[0]['name'], 'aaa')
    assert_equals(tag_tree[1]['name'], 'bar')
    assert_equals(tag_tree[2]['name'], 'foo')
