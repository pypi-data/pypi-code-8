import sqlobject

from horse import models


class MusicFavourite(models.Model):
    artist = sqlobject.StringCol()
    title = sqlobject.StringCol()
    fav_count = sqlobject.IntCol(default=1)
