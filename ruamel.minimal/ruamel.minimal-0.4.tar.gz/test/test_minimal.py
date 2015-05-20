
import platform

def test_minimal():
    print("\rpython executable is " + platform.architecture()[0])
    assert True
