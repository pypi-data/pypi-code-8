import re


def match(string, seq_of_strs):
    for regexp in seq_of_strs:
        if re.match(regexp, string):
            return True

