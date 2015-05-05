from __future__ import absolute_import
from Queue import Queue, Empty
from selenium import webdriver
from datetime import timedelta


class Driver(object):
    def __len__(self):
        return 0

    @property
    def content(self):
        return self.page_source

    @property
    def url(self):
        return self.current_url

    @property
    def elapsed(self):
        return timedelta()


class Remote(webdriver.Remote, Driver):
    pass


class FirefoxDriver(webdriver.Firefox, Driver):
    pass


class ChromeDriver(webdriver.Chrome, Driver):
    pass


class PhantomJSDriver(webdriver.PhantomJS, Driver):
    pass


class Browser(object):
    def get_driver(self):
        return Remote()

    def __init__(self):
        self.browsers = Queue()

    def get_response(self, url, **kwargs):
        try:
            browser = self.browsers.get(block=False)
        except Empty:
            browser = self.get_driver()
        browser.get(url)
        return browser

    def put_response(self, browser):
        self.browsers.put(browser)

    def clear(self):
        while True:
            try:
                browser = self.browsers.get(block=False)
                browser.close()
            except Empty:
                break


class Headless(Browser):
    def __init__(self):
        from xvfbwrapper import Xvfb
        self._vdisplay = Xvfb()
        self._vdisplay.start()
        super(Headless, self).__init__()

    def clear(self):
        super(Headless, self).clear()
        self._vdisplay.stop()


class Chrome(Browser):
    def get_driver(self):
        return ChromeDriver()


class ChromeX(Headless, Chrome):
    pass


class Firefox(Browser):
    def get_driver(self):
        return FirefoxDriver()


class FirefoxX(Headless, Firefox):
    pass


class PhantomJS(Browser):
    def get_driver(self):
        return PhantomJSDriver()
