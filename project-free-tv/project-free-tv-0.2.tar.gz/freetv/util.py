"""
All utility functions
"""
import requests
from lxml.html.clean import Cleaner
import lxml.html

YDL_SUPPORTED_SITES = {
    "novamov", "vidspot", "allmyvideos", "movshare", "nowvideo",
    "videoweed", "mooshare" # "divxstage"
}


def get_site_url_from_base(base):
    return "http://www." + base + ".com/"

def get_site_url(site):
    base_to_url = {
    "novamov":"http://www.novamov.com/video/",
    "vidspot": "http://www.vidspot.net/",
    "allmyvideos": "http://allmyvideos.net/",
    "videoweed": "http://www.videoweed.es/file/",
    "movshare": "http://www.movshare.net/video/",
    "nowvideo": "http://www.nowvideo.ch/video/",
    # "divxstage": "http://www.cloudtime.to/video/",
    "mooshare": "http://www.mooshare.biz/"
    }
    return base_to_url[site]

def get_doc_root(url):
    html = requests.get(url).content
    cleaner = Cleaner(page_structure=False)
    cleaned_html = cleaner.clean_html(html)
    root = lxml.html.fromstring(cleaned_html)
    return root

def get_formated_title(title):
    exceptions = {'the', 'a', 'an'}
    title = " ".join([item.capitalize() if item not in exceptions else item for item in title.split()])
    return title
