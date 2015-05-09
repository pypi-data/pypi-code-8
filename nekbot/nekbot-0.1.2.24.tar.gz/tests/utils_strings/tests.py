from nekbot.utils.strings import split_arguments

__author__ = 'nekmo'


def test_split_args_quote():
    """.
    """
    assert split_arguments('nobody\'s specs the spanish inquisition') == ['nobody\'s', 'specs', 'the',
                                                                          'spanish', 'inquisition']