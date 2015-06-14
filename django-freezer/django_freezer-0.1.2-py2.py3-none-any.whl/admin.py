from subprocess import check_output, CalledProcessError

from django.contrib.admin import AdminSite


def _parse(reqs_str):
    """ Parse string of requirements into list """
    return [r.split('==') for r in reqs_str.splitlines()]


class FreezerAdminSite(object):
    index_template = 'djangofreezer/index.html'

    def index(self, request, extra_context=None):
        """ Add pip freeze info to request """
        if extra_context is None:
            extra_context = {}
        try:
            reqs = check_output(['pip', 'freeze'])
        except CalledProcessError:
            # attach error?
            reqs = 'pip freeze call failed'
        extra_context['requirements'] = _parse(reqs)
        return super(FreezerAdminSite, self).index(request, extra_context)


class AdminSiteExtended(FreezerAdminSite, AdminSite):
    """ Admin extended with pip freeze results """
