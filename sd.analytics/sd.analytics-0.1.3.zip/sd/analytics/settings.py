from collective.dancing import channel
from collective.dancing.browser.channel import ChannelAdministrationView
from collective.dancing.utils import switch_on
from interfaces import IAnalytics
from persistent.dict import PersistentDict
from sd.analytics import MessageFactory as _
from zope import component
from zope import interface
from zope.annotation.interfaces import IAnnotations

import z3c.form


class AnalyticsForm(z3c.form.form.EditForm):

    @property
    def fields(self):
        fields = z3c.form.field.Fields(IAnalytics)
#         fields['enabled'].widgetFactory[z3c.form.interfaces.INPUT_MODE] = (
#            singlecheckboxwidget_factory)
        return fields

    def getContent(self):
        return dict(IAnalytics(self.context))

    @z3c.form.button.buttonAndHandler(_('Save'), name='save')
    def handle_save(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = z3c.form.form.EditForm.formErrorsMessage
            return
        IAnalytics(self.context).update(data)
        self.status = z3c.form.form.EditForm.successMessage
        self.context._p_changed = True


class AnalyticsView(ChannelAdministrationView):

    label = _("Google Analytics setup")

    def contents(self):
        switch_on(self)
        return AnalyticsForm(self.context, self.request)()

defaults = {'enabled': False,
            'utm_source': 'newsletter',
            'utm_medium': 'email',
            'utm_term': '',
            'utm_content': '',
            'utm_campaign': ''}


@interface.implementer(IAnalytics)
@component.adapter(channel.IPortalNewsletters)
def analytics_settings_for_newsletters(context):
    annotations = IAnnotations(context)
    if 'sd.analytics' not in annotations:
        annotations['sd.analytics'] = PersistentDict(defaults)
    return annotations['sd.analytics']
