# encoding: utf-8
'''
Created on Apr 16, 2015

@author: winston
'''
import re

from pyquery.pyquery import PyQuery

from longtail import Driver


url = "http://s.etao.com/search?spm=1002.8.0.0.JUlleR&q=%CE%A8%C6%B7%BB%E1&initiative_id=wwwetao_20150416&usearch=yes&style=list&s=0"
# url = "http://s.etao.com/search?q=%CE%A8%C6%B7%BB%E1&initiative_id=wwwetao_20150416&usearch=yes&style=list&s=0"


ptn_not_digit = re.compile('[^\d]+')

class EtaoDriver(Driver):
    def is_login_view(self):
        return self.get().current_url.startswith("http://login.etao.com/")
    
    def is_search_view(self):
        driver = self.get()
        return driver.current_url.startswith("http://s.etao.com/search?") or driver.current_url.startswith("http://www.etao.com")
    
    def login(self):
        #<input name="TPL_username" id="TPL_username_1" class="login-text J_UserName" value="" maxlength="32" tabindex="1" type="text">
        #<input aria-labelledby="password-label" name="TPL_password" id="TPL_password_1" class="login-text" maxlength="28" tabindex="2" type="password">
        driver = self.get()
        e = driver.find_element_by_xpath("//input[@name='TPL_username']")
        e.send_keys('13558860330')
        e = driver.find_element_by_xpath("//input[@name='TPL_password']")
        e.send_keys('Zcracker12')
        e.submit()
    
    def search(self):
        pass
        #<input aria-expanded="false" title="请输入搜索文字或从搜索历史中选择" aria-label="请输入搜索文字或从搜索历史中选择" x-webkit-grammar="builtin:translate" role="combobox" aria-combobox="list" aria-haspopup="true" id="J_searchIpt" class="search-combobox-input" accesskey="s" autocomplete="off" name="q" value="" placeholder="买什么，问一淘" maxlength="512" type="search">
    
    def get_list(self, html):
        d = PyQuery(html)
        for slot in d('div.slot'):
            slot = PyQuery(slot)
            print slot.find('a.title').text().replace('\n',' '),
#             slot.find('span.price > i.rmb').remove()
            print ptn_not_digit.sub('',slot.find('span.price').text()),
            print ptn_not_digit.sub('',slot.find('div.sales-volume').text()),
            print slot.find('p.shop-name').text()
            

    def test2(self):
        html = open('test.html', 'rb').read()
        self.get_list(html.decode('utf8'))
    
    def test(self):
        print self.get(url)
        if self.is_login_view():
            self.login()
        elif self.is_search_view():
            html = self.html()
            print html 
        

if __name__ == '__main__':
    EtaoDriver().test2()
