from .models import Content
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.template import loader, RequestContext, Template
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect


DEFAULT_TEMPLATE = 'content/page.html'

# This view is called from FlatpageFallbackMiddleware.process_response
# when a 404 is raised, which often means CsrfViewMiddleware.process_view
# has not been called even if CsrfViewMiddleware is installed. So we need
# to use @csrf_protect, in case the template needs {% csrf_token %}.
# However, we can't just wrap this view; if no matching flatpage exists,
# or a redirect is required for authentication, the 404 needs to be returned
# without any CSRF checks. Therefore, we only
# CSRF protect the internal implementation.


def page(request):
    """
    Public interface to the flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or :template:`flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """
    url = request.path[3:]
    if not url.startswith('/'):
        url = '/' + url
    try:
        p = Content.objects.language(request.LANGUAGE_CODE).get(is_page=True, url__exact=url)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    return render_page(request, p)


@csrf_protect
def render_page(request, page):
    """
    Internal interface to the flat page view.
    """
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if page.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    if page.template_name:
        t = loader.select_template((page.template_name, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    page.title = mark_safe(page.title) 
    t2 = Template(mark_safe(page.text))
    c2 = RequestContext(request)
    page.text = t2.render(c2)

    c = RequestContext(request, {
        'page': page
    })

    response = HttpResponse(t.render(c))

    return response
