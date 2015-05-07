# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from django.http import StreamingHttpResponse
import email.utils
import mimetypes
import os


# I *think* that it's valid to use mail.util.quote to quote filenames in
# Content-Disposition headers, since the header originated in the MIME
# specification which is used for email, but I'm not sure so I create the
# alias quote_content_disposition_filename which can be defined as a
# different function if mail.util.quote turns out to be the wrong thing to
# use.
quote = email.utils.quote


def set_download_headers_for_asset(response, asset):
    """
    Sets HTTP headers in a response for an asset.
    """

    # The filename parameter in Content-Disposition header must be quoted
    # according to http://tools.ietf.org/html/rfc2616#section-19.5.1.
    # http://greenbytes.de/tech/tc2231/#attwithasciifilenamenqws confirms
    # that quoting is necessary in practice (if an unquoted filename
    # contains spaces then some browsers, including Firefox 5, will
    # ignore anything after the space in the filename).
    response['Content-Disposition'] = \
        'attachment; filename="' + quote(asset.basename) + '"'

    # We set the Content-Type and Content-Encoding here even though
    # django.static.serve() has already done so because
    # django.static.serve() sets the content type based on the full path
    # of the file being served, and for filenames like '$.png' the full
    # path will be .../media/.png which isn't handled well by
    # mimetypes.guess_type().
    # If you delete this code then
    # test_download_mimetype_with_dollar_and_extension_filename and
    # test_download_content_encoding_with_dollar_and_extension_filename
    # should break
    mimetype, encoding = mimetypes.guess_type(asset.filename)
    mimetype = mimetype or 'application/octet-stream'
    response['Content-Type'] = mimetype
    if encoding:
        response['Content-Encoding'] = encoding
    elif 'Content-Encoding' in response:
        del response['Cache-Encoding']


class DeleteAfterwardsFileResponse(StreamingHttpResponse):
    def __init__(self, *args, **kwargs):
        self.path = kwargs.pop('path', None)
        self.filename = kwargs.pop('filename', None) or "assets.zip"
        if self.path:
            kwargs['streaming_content'] = open(self.path)

        super(DeleteAfterwardsFileResponse, self).__init__(*args, **kwargs)

        mimetype, encoding = mimetypes.guess_type(self.filename)
        mimetype = mimetype or 'application/zip'
        self['Content-Type'] = mimetype
        if encoding:
            self['Content-Encoding'] = encoding
        else:
            self['Content-Disposition'] = 'attachment; filename="%s"' % quote(
                self.filename)

    def close(self):
        super(DeleteAfterwardsFileResponse, self).close()
        os.remove(self.path)
