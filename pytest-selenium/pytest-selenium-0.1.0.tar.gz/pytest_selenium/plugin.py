# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals

import pytest
import os
import re
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

browsers = {
    'Firefox': webdriver.Firefox,
    'Chrome': webdriver.Chrome,
    'Safari': webdriver.Safari,
    'Opera': webdriver.Opera,
    'IE': webdriver.Ie,
    'PhantomJS': webdriver.PhantomJS,
}


@pytest.fixture(scope='session',
                params=browsers.keys())
def driver(request):
    if 'DISPLAY' not in os.environ:
        pytest.skip('Test requires display server (export DISPLAY)')

    try:
        b = browsers[request.param]()
    except (WebDriverException, Exception) as e:
        msg = "%s: %s" % (request.param, text_type(e))
        pytest.skip(re.sub(' +', ' ', msg))
    else:
        b.set_window_size(1200, 800)
        request.addfinalizer(lambda *args: b.quit())
        return b
