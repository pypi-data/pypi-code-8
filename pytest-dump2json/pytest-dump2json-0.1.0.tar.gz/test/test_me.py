import pytest

def test_me():
    pass


def test_me2():
    assert False == True

def test_me3(tmpdir):
    assert False == True

@pytest.mark.skipif(True, reason=":P")
def test_me4():
    assert False == True
