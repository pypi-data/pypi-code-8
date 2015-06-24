from django.conf import settings

class ThemeMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        request.ACT_THEME = settings.THEME