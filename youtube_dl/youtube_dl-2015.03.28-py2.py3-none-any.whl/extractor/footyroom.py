# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class FootyRoomIE(InfoExtractor):
    _VALID_URL = r'http://footyroom\.com/(?P<id>[^/]+)'
    _TEST = {
        'url': 'http://footyroom.com/schalke-04-0-2-real-madrid-2015-02/',
        'info_dict': {
            'id': 'schalke-04-0-2-real-madrid-2015-02',
            'title': 'Schalke 04 0 – 2 Real Madrid',
        },
        'playlist_count': 3,
    }

    def _real_extract(self, url):
        playlist_id = self._match_id(url)

        webpage = self._download_webpage(url, playlist_id)

        playlist = self._parse_json(
            self._search_regex(
                r'VideoSelector\.load\((\[.+?\])\);', webpage, 'video selector'),
            playlist_id)

        playlist_title = self._og_search_title(webpage)

        entries = []
        for video in playlist:
            payload = video.get('payload')
            if not payload:
                continue
            playwire_url = self._search_regex(
                r'data-config="([^"]+)"', payload,
                'playwire url', default=None)
            if playwire_url:
                entries.append(self.url_result(playwire_url, 'Playwire'))

        return self.playlist_result(entries, playlist_id, playlist_title)
