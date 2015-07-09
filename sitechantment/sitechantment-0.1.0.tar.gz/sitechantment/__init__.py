"""
Sitechantment

A way to use enchant to spellcheck as site as part of a test suite
"""

__author__ = 'Michael Messmore'
__email__ = 'mike@messmore.org'
__version__ = '0.1.0'

import sys
import os
import re

if sys.version_info[0] < 3:
    from urlparse import urljoin, urlparse
else:
    from urllib.parse import urljoin, urlparse

import enchant
from enchant.checker import SpellChecker
from enchant.tokenize import HTMLChunker
import requests
from bs4 import BeautifulSoup


class SiteCheck():
    """
    Our main interface

    :param lang: lang to use to construct the dictionary from
    :param client: anything that has a get() method that accepts a url
    :param verbosity: control console output (<0 is silent)
    :param dictfile: file with additional words not in the system dictionaries
    """

    checked = []
    bad_words = []
    htmlcomments = \
        re.compile('\<![ \r\n\t]*(--([^\-]|[\r\n]|-[^\-])*--[ \r\n\t]*)\>')

    def __init__(self, lang="en_US", client=requests, verbosity=0,
                 dictfile=""):
        """Set up the spellchecker and environment"""
        self.lang = lang
        self.client = requests
        self.verbosity = verbosity
        self.dictfile = dictfile

        self.dic = enchant.Dict(lang)
        if os.path.isfile(self.dictfile):
            with open(self.dictfile) as f:
                for line in f:
                    self.dic.add_to_session(line.strip())
        self.sc = SpellChecker(self.dic, chunkers=(HTMLChunker,))

    def verbose(self, msg, level=0):
        """Control console output
        :param msg: message string
        :param level: minimum level to print at (never less than 0)
        """
        if level >= self.verbosity:
            print(msg)

    def glean_links(self, url, text):
        """Capture link URIs from an HTML page
        :param url: the url of the text being examined (to unravel relative
        links)
        :param text: the html document itself
        :return: a list of URLs
        """

        soup = BeautifulSoup(text, 'html.parser')
        old_res = urlparse(url)
        links = []
        for anchor in soup.find_all('a'):
            new_url = urljoin(url, anchor.get('href'))
            new_res = urlparse(new_url)
            if new_res.netloc == old_res.netloc:
                links.append(new_url)
        return links

    def check(self, url):
        """Recursively check a URL
        :param url: The url to begin checking
        :return: a list of misspelled words
        """

        if url in self.checked:
            return False

        res = requests.get(url)
        # strip html comments before we go nuts
        self.sc.set_text(self.htmlcomments.sub('', res.text))
        for err in self.sc:
            self.verbose("ERROR: " + err.word, 1)
            if err.word not in self.bad_words:
                self.bad_words.append(err.word)
        self.checked.append(url)

        for link in self.glean_links(url, res.text):
            self.check(url)
        return self.bad_words

    def update_pwl(self):
        """Update the personal word list with the "misspelled" words found

        This is made so that internal jargon can be easily added to filter out
        noise on future runs.
        """

        if self.dictfile == "":
            return False
        df = open(self.dictfile, 'a')
        for word in set(self.bad_words):
            self.verbose("Adding {0} to dictionary: {1}".
                         format(word, self.dictfile), 1)
            df.write(word + "\n")
