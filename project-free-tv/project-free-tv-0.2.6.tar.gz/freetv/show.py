"""
Get information about a show on the Project Free TV site.
"""

import re
import os
import sys
from collections import defaultdict

from util import get_doc_root, get_site_url, YDL_SUPPORTED_SITES
# from . import projectFreeTV

class Show:
    """ A show object represet a tv show on Project Free TV. Its link_dict stores
    the links to watch each episode online. The links need to be converted into
    downloadable links recognized by youtube-dl
    TODO: add season specials into the info. Right now they are ignored.
    """
    def __init__(self, name, link):
        self.name = name
        self.link = link

        self.build_show()

    def build_show(self):
        """build a show and get all the information needed later
        """
        show_doc_root = get_doc_root(self.link)
        seasons = []
        for tbl in show_doc_root.xpath('//table[@cellpadding="4"]'):
            seasons.extend(tbl.xpath('.//tr//td//b//text()'))
        self.season_count = int(seasons[-1].split()[-1])
        self.season_urls = {season: self.link + season.lower().replace(" ", "_") + ".html" for season in seasons}
        self.site_links = {}
        self.season_episode_count = {}
        self.ydl_links = {}
        self.season_doc_roots = {season: get_doc_root(season_url) for season, season_url in self.season_urls.items()}
        for season, season_url in self.season_urls.items():
            try:
                season = int(season.split()[-1])
            except:
                # it's season special. ignore.
                print season, "can't be converted to number"
                continue
            season_link_dict = self._get_site_links(season_url)
            self.season_episode_count[season] = len(season_link_dict)
            self.site_links[season] = season_link_dict
        for season in self.site_links:
            self.ydl_links[season] = {}
            for episode in self.site_links[season]:
                self.ydl_links[season][episode] = self.get_ydl_links_from_site_links(self.site_links[season][episode])

    def get_site_links_for_season(self, season):
        """ get links for a season of a show on project free tv site
        """
        season_key = "Season " + str(season)
        return self.site_links[season]

    def get_ydl_links_for_season(self, season):
        """ get youtube-dl usable links for a whole season of a show as a dictionary
        """
        return self.ydl_links[season]


    def _get_site_links(self, season_url):
        """ get links on project free tv site for a season of a show
        """
        season_doc_root = get_doc_root(season_url)

        site_links = defaultdict(list)

        for tbl in season_doc_root.xpath('//table[@cellpadding="4"]'):
            for el in tbl.xpath('.//tr//td//a'):
                if el.get('href') and not any(text in el.get('href') for text in ['report', 'direct_connect']):
                    episode = int(el.xpath('.//div//text()')[0].split()[-1])
                    link_with_ad = el.get('href')
                    equal_sign_index = link_with_ad.find('=')
                    and_sign_index = link_with_ad.find('&')
                    link = link_with_ad[equal_sign_index+1:and_sign_index]
                    site_links[episode].append("http://www.free-tv-video-online.info/" + el.get('href'))


        # sort the links as there might be mutiply links from the same host site
        for k, v in site_links.items():
            site_links[k] = sorted(v)

        return site_links

    def get_site_links(self, season = 1, episode = 1):
        return self.site_links[season][episode]

    def get_latest_episodes(self, episodes = 3):
        last_season = self.season_count
        last_episode = len(self.ydl_links[last_season])
        if last_episode < episodes:
            return self.ydl_links[last_season].values()
        latest_episodes = []
        for episode in range(last_episode, last_episode-episodes, -1):
            latest_episodes.append(self.ydl_links[last_season][episode])
        return latest_episodes

    def get_ydl_links_in_range(self, season, start_spisode, end_episode):
        if season < 1 or season > self.season_count:
            return []
        result = []
        for episode in range(max(1, start_spisode), min(end_episode, self.season_episode_count[season]) + 1):
            result.append(self.ydl_links[season][episode])
        return result

    def get_ydl_links(self, season = 1, episode = 1):
        return self.ydl_links[season][episode]

    def clean_link(self, link):
        """ the link has changed since the site did the 10 second ads thing.
        """
        link = link.replace('/interstitial2.html?lnk=%2F', '').replace('%3F', '?').replace('%3D', '=').replace('%2F', '/')
        index  = link.find('&')
        link = link[:index]
        return link

    def get_ydl_links_from_site_links(self, links):
        """generate links downloadable via youtube-dl from online links
        """
        ydl_links = []
        pattern = r'http://www\.free-tv-video-online\.info/player/(?P<site>\w+)\.php\?id=(?P<id>[a-z\d]+)'
        for link in links:
            cleaned_link = self.clean_link(link)
            match = re.findall(pattern, cleaned_link)
            if match:
                site, video_id = re.findall(pattern, cleaned_link)[0]
                if site in YDL_SUPPORTED_SITES:
                    ydl_link = get_site_url(site) + video_id
                    ydl_links.append(ydl_link)
        return ydl_links
