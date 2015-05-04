from buffpy.api import API
from buffpy.managers.profiles import Profiles


def get_auth_settings():
    """
    Returns all the key/secret settings for Buffer access
    """
    from mezzanine.conf import settings
    settings.use_editable()
    auth_settings = {'client_id': settings.BUFFER_CLIENT_ID,
                     'client_secret': settings.BUFFER_CLIENT_SECRET,
                     'access_token': settings.BUFFER_ACCESS_TOKEN,
                    }
    return auth_settings if all(auth_settings.itervalues()) else None


def get_profiles(auth_settings):
    """
    given auth settings, return all the profiles on the account
    :param auth_settings: output of get_auth_settings or kwargs for buffpy API
    :return: list of profiles
    """
    api = API(**auth_settings)

    profiles = Profiles(api=api)

    return profiles.all()