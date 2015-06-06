

import time

__author__ = 'epi10'


class PyngdomDriver(object):

    base_url = 'https://my.pingdom.com'

    def __init__(self, username, password, implicit_wait=30, base_driver='PhantomJS'):
        """

:param username: your pingdom username (email)
:param password: your pingdom password
:param implicit_wait: how much to wait (in seconds) for elements to show into the page.
:param base_driver: Pick your selenium driver, dafault=PhantonJS.

        """
        self.username, self.password = username, password
        self.implicit_wait = implicit_wait
        self.base_driver = base_driver
        self._driver = None

    @property
    def driver(self):
        try:
            from selenium import webdriver
        except Exception, e:
            raise ImportError("There was a error importing selenium, you can install it with pip install selenium")

        if self._driver is None:
            self._driver = getattr(webdriver, self.base_driver, None)()
        return self._driver

    # mockup selenium methods

    def get(self, url, force_base=False):
        call_url = ""
        if force_base:
            call_url = self.base_url
            if url[0] != '/':
                call_url += '/'
        call_url += url

        self.driver.get(call_url)

    @property
    def wait(self):
        return self.Wait(self.implicit_wait)

    def Wait(self, implicit_wait):
        from selenium.webdriver.support.ui import WebDriverWait
        return WebDriverWait(self.driver, implicit_wait)

    def start(self):
        self.login()

    def quit(self):
        self.driver.quit()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def login(self, username=None, password=None):
        """ Log in into pingdom, if you can specify the username and/or password, if you don't then it will use the one
you pass at this driver creation.

        """
        username = username or self.username
        password = password or self.password

        self.get('/', force_base='True')
        org_url = self.driver.current_url
        self.driver.find_element_by_id("frm_email").send_keys(username)
        self.driver.find_element_by_id("frm_password").send_keys(password)
        self.driver.find_element_by_xpath("//form//input[@value='LOG IN']").click()

        self.wait.until(lambda x: org_url != x.current_url, message="Could not login")

    def realtime_rum(self, checkid, sample_interval=60):
        "get the realtime rum"
        self.get("/rum/%s#datefilter=realtime&filter&timetype=median" % checkid, force_base=True)
        time.sleep(sample_interval)
        return self.driver.execute_script("return Pingdom.rum.realtimeData")

    def iter_realtime_rum(self, checkid, sample_interval=60, iterations=5):
        self.get("/rum/%s#datefilter=realtime&filter&timetype=median" % checkid, force_base=True)
        for i in range(iterations):
            time.sleep(sample_interval)
            yield self.driver.execute_script("return Pingdom.rum.realtimeData")

    def today_rum(self, checkid):
        self.get("/rum/%s#datefilter=today&filter&timetype=median" % checkid, force_base=True)
        return self.driver.execute_script("return Pingdom.rum.aggregatedData")
