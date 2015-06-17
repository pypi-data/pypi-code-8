from datetime import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from hashlib import sha1
from plone.app.users.browser.register import RegistrationForm as OriginalRegistrationForm
try:
    from collective.registrationcaptcha.registrationform import CaptchaRegistrationForm as BaseRegistrationForm  # noqa
except:
    BaseRegistrationForm = OriginalRegistrationForm
try:
    HAS_CRC = True
    from collective.registrationcaptcha.registrationform import CaptchaRegistrationFormExtender as BaseCaptchaRegistrationFormExtender  # noqa
except:
    HAS_CRC = False
import random
from time import time
from validate_email import validate_email
from zope import schema

from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import adapts

from zope.interface import Interface

from AccessControl import Unauthorized
from BTrees.OOBTree import OOBTree
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone.z3cform.fieldsets import extensible
from z3c.form import interfaces
from collective.emailconfirmationregistration.interfaces import ILayer
from z3c.form.field import Fields
from zope.event import notify
from z3c.form.action import ActionErrorOccurred
from z3c.form.interfaces import WidgetActionExecutionError
from zope.interface import Invalid


def makeRandomCode(length=255):
    return sha1(sha1(str(
        random.random())).hexdigest()[:5] + str(
        datetime.now().microsecond)).hexdigest()[:length]


class IHiddenVerifiedEmail(Interface):

    confirmed_email = schema.TextLine()
    confirmed_code = schema.TextLine()


class Storage(object):

    def __init__(self, context):
        self.context = context
        try:
            self._data = context._registration_confirmations
        except AttributeError:
            self._data = context._registration_confirmations = OOBTree()

    def add(self, email):
        self.clean()
        email = email.lower()
        data = {
            'created': time(),
            'code': makeRandomCode(100)
        }
        self._data[email] = data
        return data

    def get(self, email):
        return self._data.get(email.lower())

    def clean(self):
        now = time()
        delete = []
        for email, item in self._data.items():
            if not item:
                delete.append(email)
                continue
            created = item['created']
            # delete all older than 1 hour
            if int((now - created) / 60 / 60) > 1:
                delete.append(email)
        for code in delete:
            del self._data[code]


class EmailConfirmation(BrowserView):

    sent = False

    def send_mail(self, item):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Email Confirmation"
        msg['From'] = getUtility(ISiteRoot).email_from_address
        msg['To'] = self.get_email()
        url = '%s/@@register?confirmed_email=%s&confirmed_code=%s' % (
            self.context.absolute_url(), self.get_email(), item['code'])
        text = """
Copy and paste this url into your web browser to confirm your address: %s
""" % url
        html = """
<p>You have requested registration, please
<a href="%s">confirm your email address by clicking on this link</a>.
</p>
<p>
If that does not work, copy and paste this urls into your web browser: %s
</p>""" % (url, url)
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        mailhost = getToolByName(self.context, 'MailHost')
        mailhost.send(msg.as_string())

    def get_email(self):
        return self.request.form.get('form.email')

    def __call__(self):
        req = self.request
        if req.REQUEST_METHOD == 'POST':
            auth = getMultiAdapter((self.context, req), name=u"authenticator")
            if not auth.verify():
                raise Unauthorized

            email = self.get_email()
            registration = getToolByName(self.context, 'portal_registration')
            if not email:
                IStatusMessage(self.request).addStatusMessage(
                    'Must provide email address', type='warning')
            elif not registration.isValidEmail(email):
                IStatusMessage(self.request).addStatusMessage(
                    'Must provide valid email address', type='warning')
            elif not validate_email(email, verify=True):
                IStatusMessage(self.request).addStatusMessage(
                    'Could not verify email address you have provided', type='warning')
            else:
                storage = Storage(self.context)
                item = storage.add(email)
                self.send_mail(item)
                self.sent = True
                IStatusMessage(self.request).addStatusMessage(
                    'Verification email has been sent to your email.', type='info')
        return self.index()


class RegistrationForm(BaseRegistrationForm):

    def get_confirmed_email(self):
        req = self.request
        return req.form.get('confirmed_email', req.form.get('form.widgets.confirmed_email', ''))

    def get_confirmed_code(self):
        req = self.request
        return req.form.get(
            'confirmed_code', req.form.get('form.widgets.confirmed_code', ''))

    def verify(self):
        email = self.get_confirmed_email()
        code = self.get_confirmed_code()
        if not email or not code:
            return False
        storage = Storage(self.context)
        entry = storage.get(email)
        if entry is None:
            return False
        if entry['code'] == code:
            return True
        return False

    def updateWidgets(self):
        super(RegistrationForm, self).updateWidgets()
        self.widgets['confirmed_email'].value = self.get_confirmed_email()
        self.widgets['confirmed_code'].value = self.get_confirmed_code()

    def validate_registration(self, action, data):
        if 'captcha' in data:
            super(RegistrationForm, self).validate_registration(action, data)
        else:
            # just because it's there, does not mean it's configured
            OriginalRegistrationForm.validate_registration(self, action, data)
        if data['email'].lower() != self.get_confirmed_email().lower():
            err_str = u'Email address you have entered does not match email used in verification'
            notify(
                ActionErrorOccurred(
                    action, WidgetActionExecutionError('email', Invalid(err_str))
                )
            )
        del data['confirmed_email']
        del data['confirmed_code']

    def __call__(self):
        if not self.verify():
            return self.request.response.redirect('%s/@@register-confirm-email' % (
                self.context.absolute_url()))

        return super(RegistrationForm, self).__call__()


class EmailConfirmationFormExtender(extensible.FormExtender):
    """Registrationform extender to extend it with the captcha schema.
    """
    adapts(Interface, ILayer, RegistrationForm)
    fields = Fields(IHiddenVerifiedEmail)

    def __init__(self, context, request, form):
        self.context = context
        self.request = request
        self.form = form

    def update(self):
        self.add(IHiddenVerifiedEmail, prefix="")
        self.form.fields['confirmed_email'].mode = interfaces.HIDDEN_MODE
        self.form.fields['confirmed_code'].mode = interfaces.HIDDEN_MODE


if HAS_CRC:
    class CaptchaRegistrationFormExtender(BaseCaptchaRegistrationFormExtender):
        adapts(Interface, ILayer, RegistrationForm)
