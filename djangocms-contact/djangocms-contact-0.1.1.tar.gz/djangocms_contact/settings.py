from django.conf import settings


def get_setting(name):
    defaults = {
        'CMSCONTACT_FROM_EMAIL': getattr(settings, 'CMSCONTACT_FROM_EMAIL',
                                         None),
        'CMSCONTACT_TO_EMAIL': getattr(settings, 'CMSCONTACT_TO_EMAIL', None)
    }
    return defaults[name]
