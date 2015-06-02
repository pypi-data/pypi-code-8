import sqlobject

from horse.bridles.base import BridleModel


class MusicFavourite(BridleModel):
    artist = sqlobject.StringCol()
    title = sqlobject.StringCol()
    fav_count = sqlobject.IntCol(default=1)
