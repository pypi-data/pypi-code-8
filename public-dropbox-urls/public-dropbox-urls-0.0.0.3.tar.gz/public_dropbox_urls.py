from urlparse import urlparse
import requests


class DropBoxResource(object):
    """
    Object responsible for representing a remotely accessible 
    DropBox document. Takes an input_url, which should be the
    URL of the document as it can be accessed when one clicks
    "Share" in their web application, but supplies "dl?=1" as
    a querystring parameter. Something like:
    'https://www.dropbox.com/s/xxxxxxxxxxx/My%20document.docx?dl=1'.

    Alternatively, there is a `from_share_url` method that expects
    a URL formatted slighly differently, which redirects to the
    former, and looks something like this:
    'https://www.dropbox.com/l/xxxxxxxxxxxxxxxxxxxxx'

    Finally, there is `from_redirect_url`, which expects the
    same thing as the regular constructor, except the querystring
    parameters are ignored, and "dl?=1" will be added.
    """

    def __init__(self, redirect_url, share_url=None):
        self.redirect_url = redirect_url
        self.share_url = share_url
        self.download_url = None
        self.is_public = None

    @classmethod
    def from_share_url(cls, share_url):
        resp = requests.get(share_url, allow_redirects=False)
        return cls.from_redirect_url(resp.headers.get('location'))

    @classmethod
    def from_redirect_url(cls, redirect_url):
        # The redirect location has querystring parameters
        # that make the page render in a way we don't want;
        # remove them and supply '?dl=1', for downloading.
        parsed_url = urlparse(redirect_url)
        document_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path + '?dl=1'

        # pass along the share url for reference
        return cls(document_url)

    def resolve(self):
        resp = requests.get(self.redirect_url, allow_redirects=False)

        if resp.status_code == 302:
            redirect_location = resp.headers.get('location')
            if self._looks_password_protected(redirect_location):
                self.is_public = False
            else:
                self.download_url = redirect_location
                self.is_public = True

        elif resp.status_code is requests.codes.ok:
            # If we got here, this may signify an expired link
            if self._looks_expired(resp.content):
                self.is_public = False
            else:
                # unknown state
                pass

        else:
            # unknown error
            pass

    @staticmethod
    def _looks_password_protected(url):
        return 'password' in url

    @staticmethod
    def _looks_expired(content):
        return '<title>Link expired - Dropbox</title>' in content

