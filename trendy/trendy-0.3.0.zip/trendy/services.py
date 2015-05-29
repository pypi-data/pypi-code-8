"""
Services provide access to the SOAP web methods for each object class in a slightly more pythonic manner.

These are intended to be added to the Connection as attributes and not to be instantiated directly.
"""

from inspect import getcallargs
import json
import logging
from time import clock
from functools import wraps
import requests


def log_with_time(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        start = clock()
        result = func(*args, **kwargs)
        end = clock() - start
        obj = getcallargs(func, *args, **kwargs)
        obj['self'].logger.debug("called {} with {} took {} secs".format(func.__name__, args, end))
        return result

    return wrap


class ServiceBase(object):
    """
    Provide a simple, consistent, pythonic API to a Trend object collection.

    This class takes advantage of the fact that the Trend API is actually very consistent to dynamically call the
    required SOAP methods based on a prefix that identifies the type of object to retrieve.
    """

    def __init__(self, trend, prefix):
        self.trend = trend
        self._prefix = prefix
        self.logger = logging.getLogger(__name__)

    @log_with_time
    def all(self):
        """
        Get all the objects from Trend
        """
        return getattr(self.trend, self._prefix + 'RetrieveAll')()

    @log_with_time
    def by_id(self, id):
        """
        Get a single object from Trend by numeric ID
        """
        return getattr(self.trend, self._prefix + 'Retrieve')(id)

    @log_with_time
    def by_name(self, name):
        """
        Get a single object from Trend by name
        """
        return getattr(self.trend, self._prefix + 'RetrieveByName')(name)

    @log_with_time
    def by_ids(self, ids):
        """
        Get an enumerable of objects from Trend from an enumerable of IDs
        """
        return map(self.by_id, ids)

    @log_with_time
    def by_names(self, names):
        """
        Get an enumerable of objects from Trend from an enumerable of names
        """
        return map(self.by_name, names)

    @log_with_time
    def delete(self, obj_or_id):
        """
        Delete an object from Trend

        obj_or_id may be a numeric id or a Transport object
        """
        # All Transport objects have an ID attr, otherwise assume it is the id itself
        id = getattr(obj_or_id, 'ID', obj_or_id)
        return getattr(self.trend, self._prefix + 'Delete')([id])

    @log_with_time
    def update(self, transport):
        """
        Update an object in trend
        """
        return getattr(self.trend, self._prefix + 'Save')(transport)

    def default(self):
        return self.trend.client.factory.create(self._prefix + 'Transport')

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return self.__class__.__name__


class SecurityProfilesService(ServiceBase):
    """
    Service for interacting with Security Profiles
    """

    def __init__(self, trend):
        super(SecurityProfilesService, self).__init__(trend, 'securityProfile')

    def default(self):
        default = self.trend.client.factory.create('SecurityProfileTransport')
        default.description = ''
        default.name = ''
        default.parentSecurityProfileID = 0
        default.DPIRuleIDs = None
        default.DPIState = "INHERITED"
        default.antiMalwareManualID = None
        default.antiMalwareManualInherit = True
        default.antiMalwareRealTimeID = None
        default.antiMalwareRealTimeInherit = True
        default.antiMalwareRealTimeScheduleID = None
        default.antiMalwareScheduledID = None
        default.antiMalwareScheduledInherit = True
        default.antiMalwareState = "INHERITED"
        default.applicationTypeIDs = None
        default.firewallRuleIDs = None
        default.firewallState = "INHERITED"
        default.integrityRuleIDs = None
        default.integrityState = "INHERITED"
        default.logInspectionRuleIDs = None
        default.logInspectionState = "INHERITED"
        default.recommendationState = None
        default.scheduleID = None
        default.statefulConfigurationID = None
        return default


class FirewallRulesService(ServiceBase):
    """
    Service for interacting with Firewall Rules
    """

    def __init__(self, trend):
        super(FirewallRulesService, self).__init__(trend, 'firewallRule')


class IpListsService(ServiceBase):
    """
    Service for interacting with IP Lists
    """

    def __init__(self, trend):
        super(IpListsService, self).__init__(trend, 'IPList')


class PortsService(ServiceBase):
    """
    Service for interacting with Ports
    """

    def __init__(self, trend):
        super(PortsService, self).__init__(trend, 'portList')


class GroupsService(ServiceBase):
    """
    Service for interacting with Host Groups
    """

    def __init__(self, trend):
        super(GroupsService, self).__init__(trend, 'hostGroup')


class MacsService(ServiceBase):
    """
    Service for interacting with MACs
    """

    def __init__(self, trend):
        super(MacsService, self).__init__(trend, 'MACList')


class HostsService(ServiceBase):
    """
    Service for interacting with MACs
    """

    def __init__(self, trend):
        super(HostsService, self).__init__(trend, 'host')


class HostDetailsService(ServiceBase):
    """
    Service for interacting with Host Details
    """

    def __init__(self, trend):
        super(HostDetailsService, self).__init__(trend, 'hostDetail')

    def all(self):
        host_filter = self.trend.client.factory.create('HostFilterTransport')
        host_filter.type = 'ALL_HOSTS'
        return getattr(self.trend, self._prefix + 'Retrieve')(host_filter, 'LOW')

    # Nothing else is implemented at this stage

    def by_id(self, id):
        raise NotImplemented()

    def by_name(self, name):
        raise NotImplemented()

    def delete(self, obj_or_id):
        raise NotImplemented()

    def update(self, transport):
        raise NotImplemented()

    def default(self):
        raise NotImplemented()


class CloudAccountsService(ServiceBase):
    """
    Cloud Accounts are only available via the REST interface.

    The REST interface will honour the existing SOAP session.
    """

    def __init__(self, trend):
        super(CloudAccountsService, self).__init__(trend, 'cloudaccounts')
        self.session = requests.Session()

        # Deep Security installs are generally self-signed.
        self.session.verify = False

        # the REST interface defaults to XML.  These headers will force it to JSON which is a bit nicer to
        # get the data out of in Python
        self.session.headers = {'Content-Type': "application/json", "Accept": "application/json"}

        self.session.params = {'sID': self.trend.sid}
        self.baseUrl = self.trend.url.replace('/webservice/Manager?WSDL', '/rest/')

    def all(self):
        response = self.session.get(self.baseUrl + 'cloudaccounts')
        if response.status_code == 200:
            data = json.loads(response.content)
            return data['cloudAccountListing']['cloudAccounts']
        else:
            raise "oops"


