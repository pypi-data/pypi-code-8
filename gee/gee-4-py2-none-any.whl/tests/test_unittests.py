import os
import pytest
import shutil
import gee.script.gee as gee


def test_make_key():
    k = gee.make_key("hello world")
    t = 'uU0nuZNNPgilLlLX2n2r+sSE7+N6U4DukIj3rOLvzek='
    assert k == t


def test_encrypt_cycle():
    shutil.copyfile("tests/test_source.txt", "tests/test_encrypt_me.txt")

    k = gee.make_key("hello")
    gee.encrypt_file(k, "tests/test_encrypt_me.txt")
    gee.decrypt_file(k, "tests/test_encrypt_me.txt.gee", None)

    with open("tests/test_encrypt_me.txt", "rb") as FILE:
        z = FILE.readline()
        z = FILE.readline()
        assert z == "I'm causing more family feuds than Richard Dawson\n"


def test_incorrect_passphrase():
    shutil.copyfile("tests/test_source.txt", "tests/test_encrypt_me.txt")

    with pytest.raises(Exception) as e:
        k = gee.make_key("hello")
        j = gee.make_key("hello world")
        gee.encrypt_file(k, "tests/test_encrypt_me.txt")
        gee.decrypt_file(j, "tests/test_encrypt_me.txt.gee", None)
    assert str(e.typename) == "InvalidToken"


def test_same_checksums():
    shutil.copyfile("tests/test_source.txt", "tests/test_encrypt_me.txt")

    k = gee.make_key("hello")

    hash_pre = gee.checksum("tests/test_encrypt_me.txt")

    gee.encrypt_file(k, "tests/test_encrypt_me.txt")
    gee.decrypt_file(k, "tests/test_encrypt_me.txt.gee", None)

    hash_post = gee.checksum("tests/test_encrypt_me.txt")
    assert hash_pre == hash_post
