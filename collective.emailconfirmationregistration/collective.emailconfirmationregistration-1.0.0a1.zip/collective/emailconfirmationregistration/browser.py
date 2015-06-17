from Products.CMFCore.interfaces import ISiteRoot
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from BTrees.OOBTree import OOBTree
from zope.component import getMultiAdapter
from AccessControl import Unauthorized
from Products.Five import BrowserView
from plone.app.users.browser.register import RegistrationForm as BaseRegistrationForm
from zope.formlib import form
from zope import schema
from zope.interface import Interface
from time import time
import random
from hashlib import sha1
from datetime import datetime
from Products.statusmessages.interfaces import IStatusMessage
from zope.formlib.interfaces import WidgetInputError
from validate_email import validate_email


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
        return req.form.get('confirmed_email', req.form.get('form.confirmed_email', ''))

    def get_confirmed_code(self):
        req = self.request
        return req.form.get(
            'confirmed_code', req.form.get('form.confirmed_code', ''))

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

    @property
    def form_fields(self):
        if not self.showForm:
            # We do not want to spend time calculating fields that
            # will never get displayed.
            return []

        fields = super(RegistrationForm, self).form_fields
        return fields + form.Fields(IHiddenVerifiedEmail)

    def setUpWidgets(self):
        super(RegistrationForm, self).setUpWidgets()
        self.widgets['confirmed_email'].style = 'display:none'
        self.widgets['confirmed_code'].style = 'display:none'

    def update(self):
        super(RegistrationForm, self).update()
        self.widgets['confirmed_email']._missing = self.get_confirmed_email()
        self.widgets['confirmed_code']._missing = self.get_confirmed_code()

    def validate_registration(self, action, data):
        errors = super(RegistrationForm, self).validate_registration(action, data)
        if data['email'].lower() != self.get_confirmed_email().lower():
            err_str = u'Email address you have entered does not match email used in verification'
            errors.append(WidgetInputError(
                'email', u'label_email', err_str))
            self.widgets['email'].error = err_str
        return errors

    def __call__(self):
        if not self.verify():
            return self.request.response.redirect('%s/@@register-confirm-email' % (
                self.context.absolute_url()))

        return super(RegistrationForm, self).__call__()