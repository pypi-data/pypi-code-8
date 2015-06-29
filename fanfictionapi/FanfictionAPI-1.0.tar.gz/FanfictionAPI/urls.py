__author__ = 'jwsm'

'''
This file contains utility functions for validating and
manipulating urls. For internal use only. Not part of the
public API.
'''

import re

# like an enum
Fanfic = "Fanfic"
Author = "Author"
Beta = "Beta"
Category = "CategoryListing"

fanfiction_base_url = "http://www.fanfiction.net"

fanfiction_base_regex = '^https?://(www|m)\.fanfiction\.net'
story_partial_regex = '/s/\d+/\d+/.'
user_partial_regex = '/u/\d+/.'
beta_partial_regex = '/betareaders/.'

compiled_fanfic_regex = re.compile(fanfiction_base_regex + story_partial_regex)
compiled_user_regex = re.compile(fanfiction_base_regex + user_partial_regex)
compiled_beta_regex = re.compile(fanfiction_base_regex + beta_partial_regex)
other_regex = re.compile(fanfiction_base_regex + '/.+/.')


def remove_params(url):
    return url.split('?')[0]


def parameters(url):
    try:
        params = url.split('?')[1].split('&')
        return [param for param in params if param != '']

    except IndexError:
        return []


def is_url(string):
    return re.compile('^https?://').match(string)


def classify_url(url):
    """
    Determines the sort of page the input url links to. It is assumed that
    the user is on fanfiction.net.

    Arg:
        url (str): The url to classify

    Returns:
        str: a string (defined in urls.py) representing the type of page the url is linking to

        Possible results:
        Fanfic: An actual fanfic
        Author: Author/user of the site
    """

    if compiled_fanfic_regex.match(url):
        return Fanfic
    if compiled_user_regex.match(url):
        return Author
    if compiled_beta_regex.match(url):
        return Beta
    if other_regex.match(url):
        return Category
    return None


def normalize_url(url):
    """
    Convert a url into a standard format. Https will be converted to http,
    and mobile links will be converted to regular links.

    Arg:
        url (str): The url to normalize

    Returns:
        str: the resultant url
    """

    https_regex = re.compile('^https://.')
    mobile_url_regex = re.compile('^https?://m\..')

    if mobile_url_regex.match(url):
        url = url.replace('://m.', '://www.', 1)
    if https_regex.match(url):
        url = url.replace('https://', 'http://', 1)
    return url


def extract_page_number(url, key):
        params = parameters(url)

        if len(params) == 0:
            return '1'

        for param in params:
            if param and param[0] == 'p':
                return str(param[len(key) + 1:].replace(',', ''))

        # just in case...
        return '1'
