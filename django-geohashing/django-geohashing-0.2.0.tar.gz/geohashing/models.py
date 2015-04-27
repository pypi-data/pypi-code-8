import md5

from django.db import models

OFFSET_FORMAT = '{:.6f}'

class Day(models.Model):
    geohash_date = models.DateField("date",unique=True)
    djia_open = models.CharField(null=True,blank=True,max_length=9)
    latitude_delta = models.CharField(null=True,blank=True,max_length=30)
    longitude_delta = models.CharField(null=True,blank=True,max_length=30)
    djia_open_30w_adj = models.CharField(null=True,blank=True,max_length=9)
    latitude_delta_30w_adj = models.CharField(null=True,blank=True,max_length=30)
    longitude_delta_30w_adj = models.CharField(null=True,blank=True,max_length=30)

    class Meta:
        ordering = ('geohash_date',)

    def __init__(self, *args, **kwargs):
        """
        Overridden to automatically populate lat/lng offsets.
        """
        geohash_date = kwargs.get('geohash_date')
        djia_open = kwargs.get('djia_open')
        djia_open_30w_adj = kwargs.get('djia_open_30w_adj')
        if djia_open is not None:
            lat, lng = Day.calculate_offsets(geohash_date, djia_open)
            kwargs['latitude_delta'] = lat
            kwargs['longitude_delta'] = lng
        if djia_open_30w_adj is not None:
            lat, lng = Day.calculate_offsets(geohash_date, djia_open_30w_adj)
            kwargs['latitude_delta_30w_adj'] = lat
            kwargs['longitude_delta_30w_adj'] = lng
        super(Day, self).__init__(*args, **kwargs)

    @staticmethod
    def calculate_offsets(date, djia):
        """
        Returns the decimal portion of geohash destination coordinates

        date should be a datetime.date object.
        djia should be a string object

        For example, on the date 2005-05-26, the opening was 10458.68.
        When the algorithm is applied, we end up with a latitude offset
        of 0.857713... and a longitude offset of 0.544543...; this function
        would in that case return the tuple ('857713','544543').
        """
        digest = md5.new(str(date) + '-' + str(djia)).hexdigest()
        lat_hex, lng_hex = '.' + digest[:16], '.' + digest[16:]
        lat_offset = OFFSET_FORMAT.format(float.fromhex(lat_hex)).split('.')[1]
        lng_offset = OFFSET_FORMAT.format(float.fromhex(lng_hex)).split('.')[1]
        return lat_offset, lng_offset
