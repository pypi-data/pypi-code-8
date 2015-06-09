import os
import json
import logging

import requests

from django.conf import settings

logger = logging.getLogger('mgsub')


class MailgunError(Exception):
    def __init__(self, code, reason=None, json=None):
        self.code = code
        self.reason = reason
        self.json = json

    def __str__(self):
        if self.json is not None:
            return repr(self.code) + ' ' + repr(self.json)
        return repr(self.code) + ' ' + repr(self.reason)


class MailgunList(object):
    list_url = "https://api.mailgun.net/v2/lists/{0}/members"

    def __init__(self, list_email=None):
        if list_email is None:
            self.list_email = settings.MGSUB_DEFAULT_MAILINGLIST
        elif 'MGSUB_DEFAULT_MAILINGLIST' in os.environ:
            self.list_email = os.environ.get('MGSUB_DEFAULT_MAILINGLIST')
        else:
            self.list_email = list_email

        if hasattr(settings, 'MAILGUN_API_KEY'):
            self.api_key = settings.MAILGUN_API_KEY
        else:
            self.api_key = os.environ.get('MAILGUN_API_KEY')

    def get_list_url(self):
        return self.list_url.format(self.list_email)

    def get_member_url(self, email):
        return os.path.join(self.get_list_url(), email)

    def _parse_error_response(self, response):
        content = None
        if all([response.headers['content-length'] != '0',
                response.headers['content-type'] == 'application/json']):
            content = response.json()

        return [response.status_code, response.reason, content]

    def subscribe(self, email, name=None, description=None,
                  recipient_vars=None):
        res = requests.post(self.get_list_url(),
                            auth=('api', self.api_key),
                            data={'subscribed': True,
                                  'address': email,
                                  'name': name,
                                  'description': description,
                                  'vars': json.dumps(recipient_vars)},
                            )

        log = {"email": email,
               "list": self.list_email,
               }

        if res.status_code != 200:
            if res.status_code == 400:
                try:
                    jsonres = res.json()

                    # Signing up again is not worth an exception
                    if 'Address already exists' in jsonres['message']:
                        jsonres['member'] = {'address': email}

                        logger.warning(
                            'Duplicate subscription "{email}" to list "{list}".'.format(**log))
                        return jsonres
                except:
                    pass

            logger.info('Error subscribing "{email}" to list "{list}".\n'.format(**log))
            raise MailgunError(*(self._parse_error_response(res)))

        logger.info('Subscribed "{email}" to list "{list}".')
        return res.json()

    def unsubscribe(self, email):
        res = requests.delete(self.get_member_url(email),
                              auth=('api', self.api_key))

        log = {"email": email,
               "list": self.list_email,
               }

        if res.status_code != 200:
            logger.info('Error unsubscribing "{email}" from list "{list}".\n'.format(**log))
            raise MailgunError(*(self._parse_error_response(res)))

        return res.json()
