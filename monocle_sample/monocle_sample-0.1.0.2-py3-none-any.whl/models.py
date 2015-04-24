import urllib.request, json, re
from django.db import models

class Video(models.Model):

    channel_id = models.SlugField(verbose_name='ID пользователя Youtube', help_text= 'Скопируйте часть ххх из ссылки http://www.youtube.com/user/ххх Вашего канала')

    def get_video_json(self):
        url = 'http://gdata.youtube.com/feeds/users/' + self.channel_id + '/uploads?alt=json'
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode())
        videos = []
        for v in data['feed']['entry']:

            videos.append({
                'title': v['title']['$t'],
                'id': re.findall(r'[^/]*$',v['id']['$t'])[0],
                'thumnails': v['media$group']['media$thumbnail']
            })

        return videos






