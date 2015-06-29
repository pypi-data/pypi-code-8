__author__ = 'akotian'

'''
Author class
'''
import requests
from bs4 import BeautifulSoup, SoupStrainer
from FanfictionAPI import urls
from FanfictionAPI.fanfic import Fanfic

class Author(object):

  def __init__(self, url=None, html=None):
    """
    Constructor
    """
    self._html = None
    self._fanfics = None
    self._fanfics_urls = [] 
    self._favorite_fanfics = None
    self._favorite_authors = None
    self._beta_reader = None
    self._join_date = None
    self._profile_update_date = None
    self._author_id = None
    self._author_country = None
    if url != None:
      self._url = urls.normalize_url(url)
      if urls.classify_url(self._url) != urls.Author:
        raise ValueError("Invalid url for Author class")

    if self._html:
      self._html = BeautifulSoup(self._html)
    else:
      self._html = BeautifulSoup(requests.get(self._url).text)


  def get_fanfics(self):  
    '''
    Returns:
      Authors fanfics
    '''
    if self._fanfics is None:
      title = self._html.select("#st .mystories .stitle")
      self._get_fanfic_urls(title)
    return (Fanfic(url) for url in self._fanfics_urls)

  def get_favorite_fanfics(self):  
    '''
    Returns:
      Authors favorite fanfics
    '''
    if self._favorite_fanfics is None:
      title = self._html.select("#fs .favstories .stitle")
      self._get_fanfic_urls(title)
    return (Fanfic(url) for url in self._fanfics_urls)

  def get_favorite_authors(self):  
    '''
    Returns:
      Authors favorite authors 
    '''
    if self._favorite_authors is None:
      title = self._html.select("#fa dl a")
      self._get_fanfic_urls(title)
    return (Author(url) for url in self._fanfics_urls)

  def _get_fanfic_urls(self, title):
    '''
      Process titles and links

      Returns:
        JSON stream consisting of title and its corresponding link
    '''
    for i in title:
        self._fanfics_urls.append(urls.fanfiction_base_url + i.attrs['href'])

  def is_beta_reader(self):  
    '''
    Returns:
      Is Beta reader
    '''
    if self._beta_reader is None:
      table = self._html.select('#bio')[0].find_previous_sibling("table")
      profile_type = table.select('tr:nth-of-type(2) td a')[0].get_text()
      if (profile_type == 'Beta Profile'):
        self._beta_reader = True
      else:
        self._beta_reader = False 
    return self._beta_reader  

  def get_join_date(self):  
    '''
    Returns:
      Author join date 
    '''
    if self._join_date is None:
      table = self._html.select('#bio')[0].find_previous_sibling("table")
      self._join_date = table.select('tr:nth-of-type(3) td span')[0].get_text()
    return self._join_date

  def get_last_profile_update(self):  
    '''
    Returns:
      Last profile update date 
    '''
    if self._profile_update_date is None:
      table = self._html.select('#bio')[0].find_previous_sibling("table")
      self._profile_update_date = table.select('tr:nth-of-type(3) td span:nth-of-type(2)')[0].get_text()
    return self._profile_update_date

  def get_id(self):  
    '''
    Returns:
      Author id 
    '''
    if self._author_id is None:
      table = self._html.select('#bio')[0].find_previous_sibling("table")
      data = table.select('tr:nth-of-type(3) td')[0].get_text()
      result = data.split(",") 
      if 'id' in result[1]:
        self._author_id = result[1].split(":")[1].strip()
      else:
        self._author_id = -1  
    return self._author_id 

  def get_country(self):  
    '''
    Returns:
      Author's country 
    '''
    if self._author_country is None:
      table = self._html.select('#bio')[0].find_previous_sibling("table")
      self._author_country = table.select('tr:nth-of-type(3) td img')[0].attrs['title']
    return self._author_country

