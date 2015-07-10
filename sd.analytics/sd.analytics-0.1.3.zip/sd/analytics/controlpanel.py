from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.dancing.browser import controlpanel


class ControlPanelView(controlpanel.ControlPanelView):

    contents = ViewPageTemplateFile('controlpanel-links.pt')
