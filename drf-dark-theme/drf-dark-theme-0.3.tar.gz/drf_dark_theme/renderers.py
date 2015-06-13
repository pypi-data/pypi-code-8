from rest_framework.renderers import BrowsableAPIRenderer


class StellarBrowsableAPIRenderer(BrowsableAPIRenderer):
    template = 'stellar-api.html'


class MoonshineBrowsableAPIRenderer(BrowsableAPIRenderer):
    template = 'moonshine-api.html'