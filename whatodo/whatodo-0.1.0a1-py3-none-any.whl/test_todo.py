import pytest
from src.todo import *

test_a = """TODO testing 
		 lots of testing #testing 
		 #moretesting
		 #andmore testing"""

test_b = """#TODO testing"""

test_c = """       #TODO testing"""

test_d = """testing"""

test_E = """* TODO  This is a new todo
        *       With a body too!
"""


def test_todo_create():
	test_a_todo = TODO(test_a, "", 1, ["TODO"])

	assert test_a_todo.title == "testing"
	assert len(test_a_todo.tags) == 3

	test_b_todo = TODO(test_b, '', 1, ["TODO"])

	assert len(test_b_todo.body) == 0

	test_c_todo = TODO(test_c, '', 1, ["TODO"])

	assert test_c_todo.title == "testing"

	with pytest.raises(Exception) as e:
		test_d_todo = TODO(test_d, '', 1, ["TODO"])

	test_E_todo = TODO(test_E, '', 1, ["TODO"])

	assert test_E_todo.body == "With a body too!"