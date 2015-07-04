from __future__ import unicode_literals


class AppSettings(object):

    def __init__(self):
        pass

    def _setting(self, name, dflt):
        from django.conf import settings
        getter = getattr(settings,
                         'SPONSOR_SETTING_GETTER',
                         lambda name, dflt: getattr(settings, name, dflt))
        return getter(name, dflt)


    @property
    def SPONSOR_EXPIRATES(self):
        """
        Do sponsorships expire? True or False.
        """
        return self._setting('SPONSOR_EXPIRATES', False)

    @property
    def SPONSOR_EXPIRE_ON_MONTHS(self):
        """
        Default number of months that a sponsor's expiration date is set from now.
        """
        return self._setting('SPONSOR_EXPIRE_ON_MONTHS', 12)

    @property
    def SPONSOR_LOGO_WIDTH(self):
        """
        Default logo width used when creating a sponsor object, then image will be dinamically resized
        using this property. Also you can change it for any sponsor in the admin.
        """
        return self._setting('settings.SPONSOR_LOGO_WIDTH', 200)

    @property
    def SPONSOR_LOGO_HEIGHT(self):
        """
        Default logo height used when creating a sponsor object, then image will be dinamically resized
        using this property. Also you can change it for any sponsor in the admin.
        Better set it to None, and in case a special logo needs to be resized vertically,
        do it in the admin independently to it.
        """
        return self._setting('settings.SPONSOR_LOGO_WIDTH', None)


# Ugly? Guido recommends this himself ...
# http://mail.python.org/pipermail/python-ideas/2012-May/014969.html
import sys
app_settings = AppSettings()
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
