from .models import Menu
from django.core.urlresolvers import reverse as rev, NoReverseMatch


def reverse(viewname, urlconf=None, args=None, kwargs=None, prefix=None, current_app=None):
    url = None
    try:
        ### Try static url first
        url = rev(viewname=viewname, args=args, kwargs=kwargs, prefix=prefix, current_app=current_app)
    except NoReverseMatch:
        urlconf = kwargs.pop('urlconf', '') ## If the urlconf is explicitly setted, then try that first
        if urlconf:
            urlconfs = [urlconf] + list(Menu.objects.exclude(urlconf=urlconf).values_list("urlconf", flat=True).distinct())
        else:
            urlconfs = Menu.objects.all().values_list("urlconf", flat=True).distinct()

        for uconf in urlconfs:
            try:
                url = rev(viewname, uconf, args, kwargs, prefix, current_app)
                break
            except NoReverseMatch:
                pass
    if not url:
        raise NoReverseMatch()
    return url
