# utils_mwclient.py

"""Utility functions to access mwlient_

This will be module __doc__
"""
"""
This is additional docs

Try some testing here:

>>> print(2 * 5)
10

we should be able to the module doc like following:

>>> from leocornus.py.sandbox import utils_mwclient
>>> print(utils_mwclient.__doc__)
Utility functions to access mwlient_
<BLANKLINE>
This will be module __doc__

"""

import os
import re
import subprocess
import mwclient

# Python version 3.0 using all lowercase module name.
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"


# the following functions are rewrite from mwclientBasic.rst

def mw_get_site(mwrc=None):
    """Get MediaWiki site's login info from the given mwrc file.
    The default is ~/.mwrc, if none is specified.

    This function will return a dict objet with the following keys:

    :host: domain name for the MediaWiki site.
    :path: the uri to MediaWiki site.
    :username: MediaWiki site user login.
    :password: MediaWiki site user password.
    """
    """
    Here is a quick test:

    >>> from leocornus.py.sandbox.utils_mwclient import mw_get_site
    >>> print(mw_get_site)
    <function mw_get_site at ...>

    """

    if(mwrc == None):
        # try to get the mw login info from default location:
        # ~/.mwrc 
        home_folder = os.path.expanduser('~')
        mwrc = os.path.join(home_folder, '.mwrc')
    # set the empty dict.
    site = None

    if os.path.exists(mwrc):
        rc = configparser.ConfigParser()
        # the config parser read method will return the filename
        # in a list.
        filename = rc.read(mwrc)
        mwinfo = {}
        mwinfo['host'] = rc.get('mwclient', 'host')
        mwinfo['path'] = rc.get('mwclient', 'path')
        mwinfo['username'] = rc.get('mwclient', 'username')
        mwinfo['password'] = rc.get('mwclient', 'password')
        # TODO: need check if those values are set properly!
        site = mwclient.Site(mwinfo['host'], path=mwinfo['path'])
        site.login(mwinfo['username'], mwinfo['password'])

    return site 

# create a wiki page.
def mw_create_page(title, content):
    """Create a MediaWiki page with the given title and content.
    """

    site = mw_get_site()
    if site == None:
        ret = None
    else:
        thepage = site.Pages[title]
        ret = thepage.save(content, summary="quick test")

    return ret

# check if wiki page exists.
def mw_page_exists(title):
    """Return true if a wiki page with the same title exists.
    """

    site = mw_get_site()
    if site == None:
        return False
    else:
        thepage = site.Pages[title]
        return thepage.exists

# replace a page with new template values.
def mw_replace_page(title, values={}):
    """Replace the page with new values.
    """

    site = mw_get_site()
    if site == None:
        return None
    else:
        thepage = site.Pages[title]
        content = thepage.edit()
        # replace new line with empty string.
        p = re.compile('\\n\|')
        onelineContent = p.sub('|', content)
        # get the template source in one line.
        p = re.compile('{{(.*)}}')
        temps = p.findall(onelineContent)
        oneline = temps[0]
        # replace | to \n as the standard template format.
        p = re.compile('\|')
        lines = p.sub('\\n|', oneline)
        # now for each new value to replace.
        for key, value in values.items():
            p = re.compile("""%s=.*""" % key)
            lines = p.sub("""%s=%s""" % (key, value), lines)
        # make the replaced content in one line too
        p = re.compile('\\n')
        replaced = p.sub('', lines);
        onelineContent = onelineContent.replace(oneline, replaced)
        ret = thepage.save(onelineContent, 'Replace now')
        return ret

# my MediaWiki site.
class MwrcSite(object):
    """The MediaWiki site reading site info from a resouce file.

    The default resource file is located at ~/.mwrc.
    """

    def __init__(self, rcfile=None):
        """Construct a site from the given resource file.
        """

        self.rcfile = rcfile
        if rcfile == None:
            # will try the default resource file location:
            # ~/.mwrc
            homeFolder = os.path.expanduser("~")
            self.rcfile = os.path.join(homeFolder, '.mwrc')

        self.site = None
        self.headers_info = None
        self.headers_default = None
        self.template_info = None
        self.template_fields = []

        # try to read the rcfile and create a site instance.
        if os.path.exists(self.rcfile):
            # read wiki site information from the resource file.
            rc = configparser.ConfigParser()
            filename = rc.read(self.rcfile)
            self.headers_info = rc.items('headers')
            self.headers_default = dict(rc.items('headers default'))
            self.templates = dict(rc.items('template', True))
            self.template_fields = rc.items('template fields', True)
            mwinfo = dict(rc.items('mwclient'))
            # TODO: need check if those values are set properly!
            if mwinfo.has_key('host'):
                self.site = mwclient.Site(mwinfo['host'], 
                                          path=mwinfo['path'])
                self.site.login(mwinfo['username'], 
                                mwinfo['password'])
        else:
            # need set up the default values for header info.
            # only need version for minimium requirment.
            # WordPress file header for Version is the default
            # pattern.
            self.headers_info = [('latest_version', 'Version:.*')]

    def page_exists(self, title):
        """return true if a wiki page with the same title exists
        """

        if self.site == None:
            return False
        else:
            thepage = self.site.Pages[title]
            return thepage.exists

    def create_page(self, title, content, comment):
        """Create a new page with the given title, 
        content and comment
        """

        ret = None
        if self.site == None:
            ret = None
        else:
            thepage = self.site.Pages[title]
            ret = thepage.save(content, summary=comment)

        return ret

    def replace_page(self, title, values={}, comment=""):
        """Replace the page with new values.
        """

        if self.site == None:
            return None
        else:
            thepage = self.site.Pages[title]
            content = thepage.edit()
            # replace new line with empty string.
            p = re.compile('\\n\|')
            onelineContent = p.sub('|', content)
            # get the template source in one line.
            p = re.compile('{{(.*)}}')
            temps = p.findall(onelineContent)
            oneline = temps[0]
            # replace | to \n as the standard template format.
            p = re.compile('\|')
            lines = p.sub('\\n|', oneline)
            # now for each new value to replace.
            for key, value in values.items():
                p = re.compile("""%s=.*""" % key)
                lines = p.sub("""%s=%s""" % (key, value), lines)
            # make the replaced content in one line too
            p = re.compile('\\n\|')
            replaced = p.sub('|', lines);
            onelineContent = onelineContent.replace(oneline, 
                                                    replaced)
            ret = thepage.save(onelineContent, summary=comment)
            return ret

    def template_values(self, filepath, pkg_name):
        """get ready all need values for the wiki template.
        """

        if self.headers_info == None:
            return None

        headers = self.extract_wp_headers(filepath)
        # adding the package name.
        headers['package_name'] = pkg_name
        for field_name, template in self.template_fields:
            field_value = template % headers
            headers[field_name] = field_value

        return headers

    def extract_wp_headers(self, filepath):
        """extract all WordPress file header fields from the given
        file. headers are configured in mw resource file,
        under [headers] section.
        """

        if self.headers_info == None:
            return None

        # return as a dict objet.
        ret = {}
        for field_name, pattern in self.headers_info:
            grep_pat = """grep -oE '%s' %s""" % (pattern, filepath)

            try:
                value = subprocess.check_output(grep_pat, shell=True)
                # we will only get the first line of the reuslt.
                # this is for some package has more than one 
                # header in a file.
                value = value.splitlines()[0]
                # only split the first ":"
                value = value.strip().split(b":", 1)
                ret[field_name] = value[1].strip()
            except subprocess.CalledProcessError:
                # could NOT find the pattern.
                if self.headers_default.has_key(field_name):
                    ret[field_name] = self.headers_default[field_name]
                else:
                    # empty string as the default.
                    ret[field_name] = ""

        return ret
