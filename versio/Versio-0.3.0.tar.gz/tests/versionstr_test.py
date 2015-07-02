# coding=utf-8
"""
tests converted from util.VersionStr
"""

from versio.version import Version
from versio.version_scheme import Simple5VersionScheme


# noinspection PyDocstring
class Version5(Version):
    def __init__(self, version_str):
        super(Version5, self).__init__(version_str=version_str, scheme=Simple5VersionScheme)


VersionStr = Version5


# noinspection PyDocstring,PyTypeChecker,PyRedundantParentheses
def testLessThan():
    # assert not VersionStr("3.2.00..") < "3.2.0.0.0"
    # assert not VersionStr("3.2.0.10.") < "3.2.00.."
    assert not "3.2..0." < VersionStr("3.2.0.0.0")
    assert not VersionStr("3.2.01.00") < VersionStr("3.2.0.0.")
    # assert VersionStr("3.2.00.20.00.0") < VersionStr("3.2.00.100.00.00")
    assert not VersionStr("3.2.0.20046") < "3.2.0.846"
    assert not VersionStr("3.2.0.200") < "3.2.0.2"
    # assert VersionStr("3.2.0.0.160") < "3.2.0.1.16."
    # assert not VersionStr("3.2.0.1.160") < "3.2.0.1.16.0"
    assert VersionStr("9") < "10"
    assert VersionStr("3.6.2.3.1") < "3.6.3.0"
    assert VersionStr("3.6.") < "3.6.0.1"
    assert not VersionStr("10.0") < VersionStr("9.6")
    assert not VersionStr("10.0.0") < ("10.0.0")
    assert not ("0.2.10.0.0") < VersionStr("0.0.10.0.0")
    assert ("0.0.1.0.0") < VersionStr("0.0.10.0.0")
    assert "1.9" < VersionStr("1.10")


# noinspection PyDocstring,PyTypeChecker,PyRedundantParentheses
def testLessEqual():
    assert VersionStr("3.2.00..") <= "3.2.0.0.0"
    assert not VersionStr("3.2.0.10.") <= "3.2.00"
    assert "3.2..0." <= VersionStr("3.2.0.0.0")
    assert not VersionStr("3.2.01.00") <= VersionStr("3.2.0.0")
    assert VersionStr("3.2.00.20.00.0") <= VersionStr("3.2.00.100.00.00")
    assert VersionStr("3.2.0.") <= "3.2.0.0.0"
    assert not VersionStr("3.2.0.20046") <= "3.2.0.846"
    assert not VersionStr("3.2.0.200") <= "3.2.0.2"
    assert VersionStr("3.2.0.0.160") <= "3.2.0.1.16."
    assert not VersionStr("3.2.0.1.160") <= "3.2.0.1.16.0"
    assert VersionStr("9") <= VersionStr("10")
    assert VersionStr("3.6.2.3.1") <= "3.6.3.0"
    assert VersionStr("3.6.") <= "3.6.0.1"
    assert not VersionStr("10.0") <= ("9.6")
    assert VersionStr("10.0.0") <= ("10.0.0")
    assert not ("0.2.10.0.0") <= VersionStr("0.0.10.0.0")
    assert ("0.0.1.0.0") <= VersionStr("0.0.10.0.0")
    assert "1.9" <= VersionStr("1.10")


# noinspection PyDocstring,PyTypeChecker,PyRedundantParentheses
def testGreaterThan():
    assert not VersionStr("3.2.00..") > "3.2.0.0.0"
    assert VersionStr("3.2.0.10.") > "3.2.00"
    assert not "3.2..0." > VersionStr("3.2.0.0.0")
    assert VersionStr("3.2.01.00") > VersionStr("3.2.0.0")
    assert not VersionStr("3.2.00.20.00.0") > VersionStr("3.2.00.100.00.00")
    assert VersionStr("3.2.0.20046") > "3.2.0.846"
    assert VersionStr("3.2.0.200") > VersionStr("3.2.0.2")
    assert not VersionStr("3.2.0.0.160") > "3.2.0.1.16."
    assert VersionStr("3.2.0.1.160") > "3.2.0.1.16.0"
    assert not VersionStr("9") > "10"
    assert not VersionStr("3.6.2.3.1") > "3.6.3.0"
    assert not VersionStr("3.6.") > "3.6.0.1"
    assert VersionStr("10.0") > ("9.6")
    assert not VersionStr("10.0.0") > ("10.0.0")
    assert ("0.2.10.0.0") > VersionStr("0.0.10.0.0")
    assert not ("0.0.1.0.0") > VersionStr("0.0.10.0.0")
    assert not "1.9" > VersionStr("1.10")


# noinspection PyDocstring,PyTypeChecker,PyRedundantParentheses
def testGreaterEqual():
    assert VersionStr("3.2.00..") >= "3.2.0.0.0"
    assert VersionStr("3.2.0.10.") >= "3.2.00.."
    assert "3.2..0." >= VersionStr("3.2.0.0.0")
    assert VersionStr("3.2.01.00") >= VersionStr("3.2.0.0")
    assert not VersionStr("3.2.00.20.00.0") >= VersionStr("3.2.00.100.00.00")
    assert VersionStr("3.2.0.20046") >= "3.2.0.846"
    assert VersionStr("3.2.0.200") >= "3.2.0.2"
    assert not VersionStr("3.2.0.0.160") >= "3.2.0.1.16."
    assert VersionStr("3.2.0.1.160") >= "3.2.0.1.16.0"
    assert not VersionStr("9") >= "10"
    assert not VersionStr("3.6.2.3.1") >= "3.6.3.0"
    assert not VersionStr("3.6.") >= "3.6.0.1"
    assert VersionStr("10.0") >= VersionStr("9.6")
    assert VersionStr("10.0.0") >= ("10.0.0")
    assert ("0.2.10.0.0") >= VersionStr("0.0.10.0.0")
    assert not ("0.0.1.0.0") >= VersionStr("0.0.10.0.0")
    assert not "1.9" >= VersionStr("1.10")


# noinspection PyDocstring,PyTypeChecker,PyRedundantParentheses
def testEqual():
    assert VersionStr("3.2.00..") == "3.2.0.0.0"
    assert not VersionStr("3.2.0.10.") == "3.2.00"
    assert "3.2..0." == VersionStr("3.2.0.0.0")
    assert not VersionStr("3.2.01.00") == VersionStr("3.2.0.0")
    assert not VersionStr("3.2.00.20.00.0") == VersionStr("3.2.00.100.00.00")
    assert not VersionStr("3.2.0.20046") == "3.2.0.846"
    assert not VersionStr("3.2.0.200") == "3.2.0.2"
    assert not VersionStr("3.2.0.0.160") == "3.2.0.1.16."
    assert not VersionStr("3.2.0.1.160") == VersionStr("3.2.0.1.16.0")
    assert not VersionStr("9") == "10"
    assert not VersionStr("3.6.2.3.1") == "3.6.3.0"
    assert not VersionStr("3.6.") == "3.6.0.1"
    assert not VersionStr("10.0") == ("9.6")
    assert VersionStr("10.0.0") == ("10.0.0")
    assert not ("0.2.10.0.0") == VersionStr("0.0.10.0.0")
    assert not ("0.0.1.0.0") == VersionStr("0.0.10.0.0")
    assert not "1.9" == VersionStr("1.10")


# noinspection PyDocstring,PyTypeChecker,PyRedundantParentheses
def testNotEqual():
    assert not VersionStr("3.2.00..") != "3.2.0.0.0"
    assert VersionStr("3.2.0.10.") != "3.2.00"
    assert not "3.2.0." != VersionStr("3.2.0.0.0")
    assert VersionStr("3.2.01.00") != VersionStr("3.2.0.0")
    assert VersionStr("3.2.00.20.00.0") != VersionStr("3.2.00.100.00.00")
    assert VersionStr("3.2.0.20046") != "3.2.0.846"
    assert VersionStr("3.2.0.200") != "3.2.0.2"
    assert VersionStr("3.2.0.0.160") != "3.2.0.1.16."
    assert VersionStr("3.2.0.1.160") != "3.2.0.1.16.0"
    assert VersionStr("9") != "10"
    assert VersionStr("3.6.2.3.1") != "3.6.3.0"
    assert VersionStr("3.6.") != "3.6.0.1"
    assert VersionStr("10.0") != ("9.6")
    assert not VersionStr("10.0.0") != ("10.0.0")
    assert ("0.2.10.0.0") != VersionStr("0.0.10.0.0")
    assert ("0.0.1.0.0") != VersionStr("0.0.10.0.0")
    assert "1.9" != VersionStr("1.10")


# noinspection PyDocstring,PyTypeChecker,PyRedundantParentheses
def testOtherMethods(self):
    assert VersionStr("3.2.6.1823").startswith("3.2.6")
    assert not VersionStr("3.2.5.1823").startswith("3.2.6")
    assert VersionStr("3.2.6.1823").endswith("1823")
    assert not VersionStr("3.2.6.1823").endswith("2223")
