# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
"""
Selenium user-interface-based tests for Asset Cloud uploads.
"""
from .utils import LoggedInSeleniumTestCase, LONG_PAGE_TIMEOUT_SECONDS
from assetcloud import random_utils
from assetcloud.models import Asset
from django.db import transaction
from django.http import SimpleCookie
import os
import re
import tempfile
import urllib2


class SeleniumUploadTests(LoggedInSeleniumTestCase):

    def download(self, element):
        """
        We can't easily check files that are directly downloaded
        using selenium, so instead we download files directly using urllib2.
        """
        link = element.attributes['href']

        opener = urllib2.build_opener()
        cookie_header = self._cookie_header_value()
        opener.addheaders.append(('Cookie', cookie_header))
        response = opener.open(self.live_server_url + link)

        class DownloadedFileResponse(object):
            def __init__(self, response):
                # NB For Content-Disposition details, see:
                # http://tools.ietf.org/html/rfc2616#section-19.5.1
                disposition = response.info().getheader('Content-Disposition')
                if disposition:
                    regex = re.search('filename="([^"]*)"', disposition)
                    self.filename = regex.groups()[0]
                else:
                    self.filename = None
                self.status_code = response.code
                self.content = response.read()

        return DownloadedFileResponse(response)

    def _cookie_header_value(self):
        """
        Get cookie header that will allow a request to share the Django session
        with the web browser being driven by Selenium.
        """

        result = ''
        for c in self.browser.get_cookies():
            if result:
                result += '; '
            encoded_value = SimpleCookie().value_encode(c['value'])[1]
            result += '%s=%s' % (c['name'], encoded_value)
        return result

    def upload_files(self, filepath):
        """
        Upload a file to AssetCloud via the upload page.

        ``filepath`` should be the path on the machine
        on which selenium is running, (not the local filepath if a Selenium Server is being used).
        """
        sel = self.browser

        if sel.current_url != self.reverse('asset-upload'):
            self.find_and_wait(id='id_nav_upload').click()

        # Ok, multiple file upload doesn't actually work with selenium:
        # See: http://bit.ly/mWcZlj http://bit.ly/oDi29Z
        #
        # If filepath is not a list, then add all filepaths.
        #if not isinstance(filepath, basestring):
        #    filepath = ", ".join(filepath)

        # Do the upload
        file_upload_element = self.find_and_wait(id='upload-file')
        # It's hidden if JS is enabled, and WebDriver throws an
        # ElementNotVisibleException if we try to interact with hidden elements,
        # so show no-script elements:
        self.show_no_script()
        file_upload_element.send_keys(filepath)

        sel.find(id='upload-submit').click()

    def wait_for_same_page_upload_to_finish(self):
        self.wait_for_display(id='view_uploaded_files',
                              timeout=LONG_PAGE_TIMEOUT_SECONDS)

    def test_upload_asset(self):
        """
        Selenium test to ensure that you can upload an asset.
        Verifies the asset by checking it is in the asset list,
        and then downloading it.
        """
        # Add the asset
        memfile = random_utils.random_image_file()
        with tempfile.NamedTemporaryFile() as file:
            filename = os.path.basename(file.name)
            file.write(memfile.read())
            file.flush()
            file.seek(0)
            self.upload_files(file.name)

        # Okay, now go to the asset-list page
        self.find_and_wait(id='id_nav_asset_list').click()

        # Okay, and verify that it was created correctly.
        self.find_and_wait(css='.asset-instance a').click()  # go to view asset page
        element = self.find_and_wait(id='id_download_link')

        download = self.download(element)
        self.assertEquals(download.status_code, 200)
        self.assertEquals(download.filename, filename)
        self.assertEquals(download.content, memfile.getvalue())

    def test_upload_assets_with_identical_filenames(self):
        """
        Selenium test to ensure that you can upload an more than one asset
        with the same name.  Verifies the assets by checking they are both
        in the asset list, with the correct (identical) name.
        """
        # Add the assets
        memfile = random_utils.random_image_file()
        with tempfile.NamedTemporaryFile() as file:
            filename = os.path.basename(file.name)
            file.write(memfile.read())
            file.flush()
            file.seek(0)
            self.upload_files(file.name)
            self.find_and_wait(id='id_nav_upload').click()
            self.upload_files(file.name)

        # Okay, now go to the asset-list page.
        self.find_and_wait(id='id_nav_asset_list').click()

        # And verify that they were created correctly.
        first_css_selector = '.asset-list li:nth-child(1) span.filename'
        # wait for page to load
        self.find_and_wait(css=first_css_selector)

        self.assertEqual(filename, self.find_hidden_text(css=first_css_selector))
        self.assertEquals(filename, self.find_hidden_text(css='.asset-list li:nth-child(2) span.filename'))
        self.assertEqual(0, len(self.browser.find(css='.asset-list li:nth-child(3)')))

    #def test_basic_navigation(self):
    #    """
    #    """
    #    sel = self.browser
    #    sel.open('')
    #
    #    sel.click("css=.nav .asset-list a")
    #    sel.wait_for_page_to_load(PAGE_TIMEOUT)
    #    sel.click("css=.nav .asset-list a")
    #    sel.wait_for_page_to_load(PAGE_TIMEOUT)

    def test_editing_assets(self):
        # Add the asset
        memfile = random_utils.random_image_file()
        filename = ''
        with tempfile.NamedTemporaryFile() as file:
            file.write(memfile.read())
            file.flush()
            file.seek(0)
            filename = self._extract_filename_from_path(file)
            self.upload_files(file.name)

        # Go to the asset list page
        self.find_and_wait(id='id_nav_asset_list').click()

        # Find its ID
        asset_css_id = self.find_and_wait(css='.asset-instance').attributes['id']
        asset_id = int(asset_css_id.replace('asset-', ''))

        # Look in the DB and verify that the title has defaulted the filename without the extension.
        transaction.commit()
        self.assertEqual(filename, Asset.unrestricted_objects.get(id=asset_id).title)

        # Check the default title in the front end.
        # We only check the input field (not the span, i.e. "css=.asset-list
        # span.title-text") because it the span text will be set to something
        # like "Click to add a title..."
        self.assertEqual(filename, self.find_and_wait(css='.asset-list input.title-field').value)

        # Fill in the title
        self.browser.find(css='.asset-list a.title-text').click()
        element = self.browser.find(css='.asset-list input.title-field')
        element.send_keys('123\n')
        # Blur the title field
        self.find_and_wait(id='header').click()

        # Refresh the page and check the title in the front end
        self.find_and_wait(css='.nav .asset-list a').click()
        self.assertEqual('123', self.find_and_wait(css='.asset-list a.title-text').text)
        self.assertEqual('123', self.browser.find(css='.asset-list input.title-field').value)

        # Check the title in the DB
        transaction.commit()
        self.assertEqual(u'123', Asset.unrestricted_objects.get(id=asset_id).title)

    def _extract_filename_from_path(self, file):
        return file.name.rsplit('/', 1)[1]
