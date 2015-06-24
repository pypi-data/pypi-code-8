# -*- coding:utf-8 -*-
import re
import urllib

from pyquery import PyQuery
import lxml.html
from yandex_parser.exceptions import EmptySerp
from yandex_parser.utils import to_unicode, get_full_domain_without_scheme


class YandexParser(object):
    params_regexr = re.U | re.M | re.DOTALL | re.I

    patterns = {
        'pagecount': re.compile(u'.*?found"\:"&mdash;&nbsp;(.*?)отв', params_regexr),
        'infected': re.compile(u'infected[^$]+url=([^&]+)&amp;fmode', params_regexr),
        'captcha': re.compile(u'<img class="image form__captcha".*?src=\"([^\"]+)\"', params_regexr),
    }

    def __init__(self, content, snippet_fileds=('d', 'p', 'u', 't', 's', 'm')):
        self.content = to_unicode(content)
        self.snippet_fileds = snippet_fileds

    def get_serp(self):
        if self.is_not_found():
            return {'pc': 0, 'sn': []}
        
        pagecount = self.get_pagecount()
        snippets = self.get_snippets()
        
        if not snippets:
            raise EmptySerp()
        
        return {'pc': pagecount, 'sn': snippets}

    def get_pagecount(self):
        match = self.patterns['pagecount'].match(self.content)
        if not match:
            return

        pagecount_raw = match.group(1)
        pagecount = int(pagecount_raw.split()[0])
        if u'тыс' in pagecount_raw:
            pagecount *= 1000
        elif u'млн' in pagecount_raw:
            pagecount *= 1000000
        return pagecount

    def is_not_found(self):
        return u'По вашему запросу ничего не нашлось' in self.content

    def get_snippets(self):
        dom = PyQuery(self.content)

        serp = dom('.serp-list').find('.serp-item')

        snippets = []
        position = 0
        for sn in serp:
            
            if 'serp-adv' in sn.attrib['class']:
                #реклама
                continue
            
            sn_div = sn.find('div')
            link = sn_div.find('h2').find('a')
            url = link.attrib['href']

            is_map = False
            if 'serp-item_plain_yes' not in sn.attrib['class']:
                is_map = url.startswith('http://maps.yandex.ru')
                if not is_map:
                    #картинки, видео и прочее, позицию сохраняем
                    position += 1
                    continue
            
            position += 1

            infected = False
            if 'infected' in url:
                match_url_infected = self.patterns['infected'].findall(url)
                if len(match_url_infected) > 0:
                    url = urllib.unquote(match_url_infected[0])
                    infected = True

            try:
                domain = get_full_domain_without_scheme(url)
            except UnicodeError as e:
                raise e
            
            snippet = {
                'd': domain,
                'p': position,
                'u': url, 
                'm': is_map, 
                't': None,  # title snippet
                's': None,  # body snippet
                'i': infected
            }

            if 't' in self.snippet_fileds:
                snippet['t'] = link.text_content()
            if 's' in self.snippet_fileds:
                children = sn_div.getchildren()
                if len(children) == 2:
                    decr_div = children[1] 
                else:
                    decr_div = children[2] 
                snippet['s'] = decr_div.text_content()
            
            snippets.append(snippet)

        return snippets
    
    def get_region_code(self, default=None):
        dom = PyQuery(self.content)
        inputs = dom.find('input[name=rstr]')
        if inputs:
            return int(inputs[0].attrib['value'].lstrip('-'))
        return default

    def get_captcha_data(self):
        if 'checkcaptcha' not in self.content:
            return

        match_captcha = self.patterns['captcha'].findall(self.content)
        url_image = match_captcha[0]
        html = lxml.html.fromstring(self.content)
        form = html.forms[0]
        form_data = dict(form.form_values())

        return {
            'url': url_image,
            'form_data': form_data,
        }

        
        