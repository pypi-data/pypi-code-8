# coding: utf-8

from __future__ import unicode_literals

import re

from .common import InfoExtractor


class JeuxVideoIE(InfoExtractor):
    _VALID_URL = r'http://.*?\.jeuxvideo\.com/.*/(.*?)-\d+\.htm'

    _TEST = {
        'url': 'http://www.jeuxvideo.com/reportages-videos-jeux/0004/00046170/tearaway-playstation-vita-gc-2013-tearaway-nous-presente-ses-papiers-d-identite-00115182.htm',
        'md5': '046e491afb32a8aaac1f44dd4ddd54ee',
        'info_dict': {
            'id': '114765',
            'ext': 'mp4',
            'title': 'Tearaway : GC 2013 : Tearaway nous présente ses papiers d\'identité',
            'description': 'Lorsque les développeurs de LittleBigPlanet proposent un nouveau titre, on ne peut que s\'attendre à un résultat original et fort attrayant.',
        },
    }

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        title = mobj.group(1)
        webpage = self._download_webpage(url, title)
        title = self._html_search_meta('name', webpage)
        config_url = self._html_search_regex(
            r'data-src="(/contenu/medias/video.php.*?)"',
            webpage, 'config URL')
        config_url = 'http://www.jeuxvideo.com' + config_url

        video_id = self._search_regex(
            r'id=(\d+)',
            config_url, 'video ID')

        config = self._download_json(
            config_url, title, 'Downloading JSON config')

        formats = [{
            'url': source['file'],
            'format_id': source['label'],
            'resolution': source['label'],
        } for source in reversed(config['sources'])]

        return {
            'id': video_id,
            'title': title,
            'formats': formats,
            'description': self._og_search_description(webpage),
            'thumbnail': config.get('image'),
        }
