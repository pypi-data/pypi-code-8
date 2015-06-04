#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib
import urllib2
import uuid


class LinkedInClient(object):
    """
    LinkedIn REST API client.

    authentication is through oauth2.

    https://developer.linkedin.com/docs/oauth2
    """
    ACCESS_TOKEN_URI = 'https://www.linkedin.com/uas/oauth2/accessToken'
    AUTHORIZATION_BASE_URI = 'https://www.linkedin.com/uas/oauth2/authorization'
    PROFILE_URI = 'https://api.linkedin.com/v1/people/~'
    client_id = None
    client_secret = None  # keep it safe.
    redirect_uri = None
    access_token = None

    def __init__(self, client_key, client_secret, redirect_uri):
        self.client_id = client_key
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorization_url(self, scope='r_basicprofile', state=None):
        """
        :param scope: space delimited list of member permissions your application is requesting on behalf of the user.
                      e.g. 'r_basicprofile r_emailaddress'

        :param state: A unique string value of your choice that is hard to guess. Used to prevent CSRF.
                      If not specific this parameter, will use a random string.
                      e.g. state=DCEeFWf45A53sdfKef424

        :return: authorization url.
                 e.g. https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=123456789&redirect_uri=https%3A%2F%2Fwww.example.com%2Foauth2%2Flinkedin&state=987654321&scope=r_basicprofile
        """
        if state is None:
            state = uuid.uuid4().hex
        query = urllib.urlencode({'client_id': self.client_id,
                                  'response_type': 'code',
                                  'redirect_uri': self.redirect_uri,
                                  'state': state,
                                  'scope': scope})
        return '%s?%s' % (self.AUTHORIZATION_BASE_URI, query)

    def get_access_token(self, code):
        """
        :param code: access code get from authorization URL.

        Access Token Response

        A successful Access Token request will return a JSON object containing the following fields:

        access_token — The access token for the user.
                       This value must be kept secure, as per your agreement to the API Terms of Use.

        expires_in — The number of seconds remaining, from the time it was requested, before the token will expire.
                     Currently, all access tokens are issued with a 60 day lifespan.
        """
        body = urllib.urlencode({'grant_type': 'authorization_code',
                                 'code': code,
                                 'redirect_uri': self.redirect_uri,
                                 'client_id': self.client_id,
                                 'client_secret': self.client_secret})
        # request = urllib2.Request(self.access_token_url)
        (status_code, data) = self._request(self.ACCESS_TOKEN_URI, body)
        if status_code == 200:
            self.access_token = data['access_token']
            # self.access_token_expires_at

        return (status_code, data)
        # request.add_header('Content-type', 'application/x-www-form-urlencoded')
        # request.add_header('Accept', 'application/json')
        # request.add_data(body)
        # response = urllib2.urlopen(request)
        #
        # data = response.read()
        #
        # return json.loads(data)

    def get_profile(self, fields=None):
        """
        Return user profile.

        This API need authentication.

        :param fields: A list of profile fields.
                      e.g. ['id', 'first-name', 'last-name', 'email-address']
                      see full list at https://developer.linkedin.com/docs/fields/basic-profile

        curl example:
        PROFILE_URI="https://api.linkedin.com/v1/people/~:(id,first-name,last-name,email-address)"
        curl -H 'x-li-format: json' -H "Authorization: Bearer $ACCESS_TOKEN" "$PROFILE_URI"

        """

        if fields is not None:
            PROFILE_URI = '%s:(%s)' % (self.PROFILE_URI, ','.join(fields))

        return self._request(PROFILE_URI)

    def _request(self, url, data=None, headers=None):
        request = urllib2.Request(url)
        request.add_header('Accept', 'application/json')
        request.add_header('x-li-format', 'json')

        if self.access_token:
            request.add_header('Authorization', 'Bearer %s' % self.access_token)

        if data:
            request.add_data(data)

        try:
            response = urllib2.urlopen(request)
            status_code = response.getcode()

            #
            # >>> r.info().headers
            # ['Server: Oracle-iPlanet-Web-Server/7.0\r\n', 'Date: Thu, 04 Jun 2015 21:43:34 GMT\r\n',
            # 'Content-type: text/html\r\n', 'Last-modified: Wed, 27 Dec 2006 19:44:00 GMT\r\n',
            # 'Content-length: 251\r\n', 'Etag: "fb-4592cd00"\r\n',
            # 'Accept-ranges: bytes\r\n', 'Connection: close\r\n']
            #
            for header in response.info().headers:
                print 'process %s' % type(header)
                (header_name, header_value) = header.strip().split(':', 1)
                if header_name.lower() == 'content-type':
                    content_type = header_value.strip()
                    break

            data = response.read()
        except urllib2.HTTPError, e:
            status_code = e.code
            data = e.fp.read()
            for header_name in e.headers:
                if header_name.lower() == 'content-type':
                    content_type = e.headers[header_name]
                    break

        if content_type and content_type.lower().startswith('application/json'):
            data = json.loads(data)

        return (status_code, data)
