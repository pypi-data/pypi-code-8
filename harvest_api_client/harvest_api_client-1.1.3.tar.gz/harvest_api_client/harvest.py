import requests
import urllib.request
from base64 import b64encode
from dateutil.parser import parse as parseDate
from xml.dom.minidom import parseString
import json
import datetime
import os, sys

from .tokens_manager import TokensManager

class HarvestError(Exception):
    pass

class HarvestConnectionError(HarvestError):
    pass

instance_classes = []
class HarvestItemGetterable(type):
    def __init__(klass, name, bases, attrs):
        # super(HarvestItemGetterable, klass).__init__(name, bases, attrs)
        super().__init__(name, bases, attrs)
        instance_classes.append(klass)

class HarvestItemBase(object):
    def __init__(self, harvest, data):
        self.harvest = harvest
        for key, value in data.items():
            key = key.replace('-', '_').replace(' ', '_')
            try:
                setattr(self, key, value)
            except AttributeError:
                pass

# class User(HarvestItemBase):
class User(HarvestItemBase, metaclass=HarvestItemGetterable):
    base_url = '/people'
    element_name = 'user'
    plural_name = 'users'

    def __str__(self):
        return 'User: {} {}'.format(self.first_name, self.last_name)

    def entries(self,start,end):
        return self.harvest._time_entries('{}/{}/'.format(self.base_url, self.id), start, end)

class Project(HarvestItemBase, metaclass=HarvestItemGetterable):
    base_url = '/projects'
    element_name = 'project'
    plural_name = 'projects'

    def __str__(self):
        return 'Project: ' + self.name

    def entries(self, start, end):
        return self.harvest._time_entries('{}/{}/'.format(self.base_url, self.id), start, end)

    @property
    def client(self):
        return self.harvest.client(self.client_id)

    @property
    def task_assignments(self):
        url = '{}/{}/task_assignments'.format(self.base_url, self.id)
        for element in self.harvest._get_element_values(url, 'task-assignment'):
            yield TaskAssignment(self.harvest, element)

    @property
    def user_assignments(self):
        url = '{}/{}/user_assignments'.format(self.base_url, self.id)
        for element in self.harvest._get_element_values(url, 'user-assignment'):
            yield UserAssignment(self.harvest, element)

class Client(HarvestItemBase, metaclass=HarvestItemGetterable):
    base_url = '/clients'
    element_name = 'client'
    plural_name = 'clients'

    @property
    def contacts(self):
        url = '{}/{}/contacts'.format(self.base_url, self.id)
        for element in self.harvest._get_element_values(url, 'contact'):
            yield Contact(self.harvest, element)

    def invoices(self):
        url = '{}?client={}'.format(Invoice.base_url, self.id)
        for element in self.harvest._get_element_values(url, Invoice.element_name):
            yield Invoice(self.harvest, element)

    def __str__(self):
        return 'Client: ' + self.name

class Contact(HarvestItemBase, metaclass=HarvestItemGetterable):
    base_url = '/contacts'
    element_name = 'contact'
    plural_name = 'contacts'

    def __str__(self):
        return 'Contact: {} {}'.format(self.first_name, self.last_name)

class Task(HarvestItemBase, metaclass=HarvestItemGetterable):
    base_url = '/tasks'
    element_name = 'task'
    plural_name = 'tasks'

    def __str__(self):
        return 'Task: ' + self.name

class UserAssignment(HarvestItemBase):
    def __str__(self):
        return 'user {} for project {}'.format(self.user_id, self.project_id)

    @property
    def project(self):
        return self.harvest.project(self.project_id)

    @property
    def user(self):
        return self.harvest.user(self.user_id)

class TaskAssignment(HarvestItemBase):
    def __str__(self):
        return 'task {} for project {}'.format(self.task_id, self.project_id)

    @property
    def project(self):
        return self.harvest.project(self.project_id)

    @property
    def task(self):
        return self.harvest.task(self.task_id)


class Entry(HarvestItemBase):
    def __str__(self):
        # return '%0.02f hours for project %d' % (self.hours, self.project_id)
        return '{:0.2f} hours for project {}'.format(self.hours, self.project_id)

    @property
    def project(self):
        return self.harvest.project(self.project_id)

    @property
    def task(self):
        return self.harvest.task(self.task_id)


class Invoice(HarvestItemBase, metaclass=HarvestItemGetterable):
    base_url = '/invoices'
    element_name = 'invoice'
    plural_name = 'invoices'

    def __str__(self):
        return 'invoice {} for client {}'.format(self.id, self.client_id)

    @property
    def csv_line_items(self):
        '''
        Invoices from lists omit csv-line-items

        '''
        if not hasattr(self, '_csv_line_items'):
            url = '{}/{}'.format(self.base_url, self.id)
            self._csv_line_items = self.harvest._get_element_values(url, self.element_name).next().get('csv-line-items', '')
        return self._csv_line_items

    @csv_line_items.setter
    def csv_line_items(self, val):
        self._csv_line_items = val

    def line_items(self):
        import csv
        return csv.DictReader(self.csv_line_items.split('\n'))

class Harvest(object):
    def __init__(self, client_id, client_secret, tokens_file_name):
        self.headers = {}
        self.tokens_file_name = tokens_file_name
        self.tokens_man = TokensManager(client_id, client_secret, tokens_file_name)
        self.access_token = self.tokens_man.load_tokens()['access_token']['value']
        self.uri = 'https://api.harvestapp.com'
        self.headers['Accept'] = 'application/xml'
        self.headers['Content-Type'] = 'application/xml'
        self.headers['User-Agent'] = 'py-harvest.py'
        for klass in instance_classes:
            self._create_getters(klass)

    def _create_getters(self, klass):
        '''
        This method creates both the singular and plural getters for various
        Harvest object classes.

        '''
        flag_name = '_got_' + klass.element_name
        cache_name = '_' + klass.element_name
        setattr(self, cache_name, {})
        setattr(self, flag_name, False)
        cache = getattr(self, cache_name)

        def _get_item(id):
            if id in cache:
                return cache[id]
            else:
                url = '{}/{}'.format(klass.base_url, id)
                item = self._get_element_values(url, klass.element_name).next()
                item = klass(self, item)
                cache[id] = item
                return item

        setattr(self, klass.element_name, _get_item)

        def _get_items():
            if getattr(self, flag_name):
                for item in cache.values():
                    yield item
            else:
                for element in self._get_element_values(klass.base_url, klass.element_name):
                    item = klass(self, element)
                    cache[item.id] = item
                    yield item

                setattr(self, flag_name, True)

        setattr(self, klass.plural_name, _get_items)

    def find_user(self, first_name, last_name):
        for person in self.users():
            if first_name.lower() in person.first_name.lower() and last_name.lower() in person.last_name.lower():
                return person

        return None

    def _time_entries(self, root, start, end):
        url = '{}entries?from={}&to={}'.format(root, start.strftime('%Y%m%d'), end.strftime('%Y%m%d'))
        for element in self._get_element_values(url, 'day-entry'):
            yield Entry(self, element)

    def _request(self, url):
        full_url = self.uri + url
        if '?' in url:
            separator = '&'
        else:
            separator = '?'

        full_url +='{}access_token={}'.format(separator, self.access_token)
        request = urllib.request.Request(url=full_url, headers=self.headers)
        try:
            # if refresh_token is fresh then the access token can be refreshed 
            # by sending a GET request to a specific url according to the spec of OAuth2
            # but if isn't fresh then an user must re-authenticate to obtain the new access and refresh tokens
            if self.tokens_man.is_refresh_token_fresh():
                self.tokens_man.refresh_access_token_by_demand()
            else:
                raise HarvestError('You must re-authenticate')
              
            r = urllib.request.urlopen(request)
            xml = r.read()
            return parseString(xml)
        
        except urllib.error.URLError as e:
            raise HarvestConnectionError(e)

    def _get_element_values(self, url, tagname):
        def get_element(element):
            text = ''.join(n.data for n in element.childNodes if n.nodeType == n.TEXT_NODE)
            try:
                entry_type = element.getAttribute('type')
                if entry_type == 'integer':
                    try:
                        return int(text)
                    except ValueError:
                        return 0
                elif entry_type in ('date', 'datetime', 'dateTime'):
                    return parseDate(text)
                elif entry_type == 'boolean':
                    try:
                        return text.strip().lower() in ('true', '1')
                    except ValueError:
                        return False
                elif entry_type == 'decimal':
                    try:
                        return float(text)
                    except ValueError:
                        return 0.0
                else:
                    return text
            except:
                return text

        xml = self._request(url)
        for entry in xml.getElementsByTagName(tagname):
            value = {}
            for attr in entry.childNodes:
                if attr.nodeType == attr.ELEMENT_NODE:
                    tag = attr.tagName
                    value[tag] = get_element(attr)

            if value:
                yield value