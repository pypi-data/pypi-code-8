from django.utils.safestring import mark_safe


def act_menu(request):
    retval = {}
    if hasattr(request, 'act_menu'):
        retval['act_menu'] = request.act_menu
    return retval