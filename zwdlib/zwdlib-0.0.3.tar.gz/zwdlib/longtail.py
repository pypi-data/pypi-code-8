'''
Created on Mar 31, 2015

@author: winston
'''
import json
import time
import urllib
import urllib2

from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


tool_url = "http://s.tool.chinaz.com/baidu/words.aspx"
task_url = "http://192.168.32.252:8000/keywords/"

def find_kw(driver, until):
    try:
        return WebDriverWait(driver,3).until(until)
    except selenium.common.exceptions.TimeoutException:
        print "could not find element"
    


class Driver(object):
    def __init__(self, debug=True):
        self.debug = debug
        self.driver = None
    
    def html(self):
        e = find_kw(self.driver, EC.element_to_be_clickable((By.TAG_NAME,"html")))
        if e:
            return e.get_attribute('innerHTML')
        
    
    def get(self, url=None):
        if not self.driver:
            if self.debug:
                self.driver = webdriver.Firefox()
            else:
                self.driver = webdriver.PhantomJS(desired_capabilities={'phantomjs.page.settings.resourceTimeout': '5000'})
                self.driver.set_page_load_timeout(30)

        if url:
            self.driver.get(url)
        return self.driver
    
    

# def etao_dig(driver, keyword):
#     pass

    
    
def dig(url = tool_url):
    
    keyword = get_keyword()
    driver = None
    
    while 1:
        if keyword:
            print keyword
            try:
                if not driver:
        #             driver = webdriver.Firefox()
        #             driver = webdriver.PhantomJS()
                    driver = webdriver.PhantomJS(desired_capabilities={'phantomjs.page.settings.resourceTimeout': '5000'})
                    driver.set_page_load_timeout(30)
                    driver.get(url)
            
                
                e = find_kw(driver, EC.element_to_be_clickable((By.ID,"kw")))
                
                if not e:
                    driver.get(tool_url)
                    continue
                            
        #         e = driver.find_element_by_id('kw')
                e.send_keys(keyword)
                e.submit()
                
    #             e = driver.find_element_by_tag_name("html")
    #             e = WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.TAG_NAME,"html")))
                e = find_kw(driver, EC.element_to_be_clickable((By.TAG_NAME,"html")))
                if not e:
                    driver.get(tool_url)
                    continue
                
        #         e = driver.find_element_by_tag_name('html')
                html = e.get_attribute('innerHTML')
                urllib2.urlopen(task_url, data=urllib.urlencode(
                                                      {
                                                       'html':html,
                                                       'keyword':keyword
                                                       }
                                                      )).read()
            except selenium.common.exceptions.TimeoutException:
                print "timeout..."
        else:
            print "no keyword found, snap 60 seconds!"
            time.sleep(60)
            
        keyword = get_keyword()
        time.sleep(5)
    if driver:
        driver.quit()
    
    print "Finished!"
    
def get_keyword():
    return json.loads(urllib2.urlopen(task_url).read()).get('name')
#     print html


if __name__ == '__main__':
    dig()
#     print get_keyword()
    