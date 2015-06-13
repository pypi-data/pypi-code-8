from rest_framework.renderers import BrowsableAPIRenderer


class DarkBrowsableAPIRenderer(BrowsableAPIRenderer):
    template = 'dark-api.html'
