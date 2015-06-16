from unittest import mock

import six

from motivation import commands

def test_jm():
	res = commands.jm(None, None, "#inane", None, "")
	assert isinstance(res, six.text_type)

def test_schneier():
	res = commands.schneier(None, None, "#inane", None, "foo")
	assert 'foo' in res

@mock.patch('requests.get',
	mock.Mock(
		return_value=mock.Mock(text='<p class="fact">How awesome is BRUCE SCHNEIER!</p>',
	)))
def test_schneier_all_caps():
	"At least one schneier fact features BRUCE SCHNEIER"
	res = commands.schneier(None, None, "#inane", None, "darwin")
	assert res == "How awesome is darwin!"
