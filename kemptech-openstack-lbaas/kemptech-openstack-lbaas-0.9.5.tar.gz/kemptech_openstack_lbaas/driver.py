#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from oslo.config import cfg
from oslo_log import log

from neutron_lbaas.services.loadbalancer import constants as lb_constants

import client
import constants as kemp_consts

LOG = log.getLogger(__name__)


class ManagerBase(object):
    def __init__(self, driver, manager):
        self.driver = driver.openstack_driver
        self.client = driver.client
        self.api_helper = driver.api_helper
        self.manager = manager


class LoadBalancerManager(ManagerBase):

    def create(self, context, lb):
        LOG.debug("KEMP driver create lb: %s" % repr(lb))
        self.manager.successful_completion(context, lb)

    def update(self, context, old_lb, lb):
        LOG.debug("KEMP driver update lb: %s" % repr(lb))
        self.driver.plugin.activate_linked_entities(context, lb)

    def delete(self, context, lb):
        LOG.debug("KEMP driver delete lb: %s" % repr(lb))
        self.driver.plugin.db.delete_loadbalancer(context, lb.id)
        self.manager.successful_completion(context, lb, delete=True)

    def refresh(self, context, lb):
        LOG.debug("KEMP driver refresh lb: %s" % repr(lb))
        # TODO(smcgough) Compare to back end and fix inconsistencies.
        self.client.refresh_loadbalancer(lb)

    def stats(self, context, lb):
        LOG.debug("KEMP driver stats of lb: %s" % repr(lb))
        # TODO(smcgough) Return nothing for now.
        stats = {
            lb_constants.STATS_IN_BYTES: 0,
            lb_constants.STATS_OUT_BYTES: 0,
            lb_constants.STATS_ACTIVE_CONNECTIONS: 0,
            lb_constants.STATS_TOTAL_CONNECTIONS: 0,
        }
        return stats


class ListenerManager(ManagerBase):

    def create(self, context, listener):
        LOG.debug("KEMP driver create listener: %s" % repr(listener))
        prep_listener = self.api_helper.prepare_listener(context, listener)
        try:
            self.client.create_virtual_service(prep_listener)
            self.manager.successful_completion(context, listener)
        except client.KempClientRequestError() as ex:
            LOG.error("Error creating listener: %s", ex)
            self.manager.failed_completion(context, listener)

    def update(self, context, old_listener, listener):
        LOG.debug("KEMP driver update listener: %s" % repr(listener))
        old_prep_listener = self.api_helper.prepare_listener(context,
                                                             old_listener)
        prep_listener = self.api_helper.prepare_listener(context, listener)
        try:
            self.client.update_virtual_service(old_prep_listener, prep_listener)
            self.manager.successful_completion(context, listener)
        except client.KempClientRequestError() as ex:
            LOG.error("Error updating listener: %s", ex)
            self.manager.failed_completion(context, listener)

    def delete(self, context, listener):
        LOG.debug("KEMP driver delete listener: %s" % repr(listener))
        prep_listener = self.api_helper.prepare_listener(context, listener)
        try:
            self.client.delete_virtual_service(prep_listener)
            self.manager.successful_completion(context, listener, delete=True)
            self.driver.plugin.db.delete_listener(context, listener.id)
        except client.KempClientRequestError() as ex:
            LOG.error("Error deleting listener: %s", ex)
            self.manager.failed_completion(context, listener)


class PoolManager(ManagerBase):

    def create(self, context, pool):
        LOG.debug("KEMP driver create pool: %s" % repr(pool))
        self.manager.successful_completion(context, pool)

    def update(self, context, old_pool, pool):
        LOG.debug("KEMP driver update pool: %s" % repr(pool))
        if old_pool['lb_method'] != pool['lb_method']:
            prep_pool = self.api_helper.prepare_pool(pool)
            try:
                self.client.update_virtual_service(prep_pool)
                self.manager.successful_completion(context, pool)
            except client.KempClientRequestError() as ex:
                LOG.error("Error updating pool: %s", ex)
                self.manager.failed_completion(context, pool)

    def delete(self, context, pool):
        LOG.debug("KEMP driver delete pool: %s" % repr(pool))
        prep_pool = self.api_helper.prepare_pool(pool)
        try:
            self.client.delete_virtual_service(prep_pool)
            self.driver.plugin.db.delete_pool(context, pool.id)
            self.manager.successful_completion(context, pool, delete=True)
        except client.KempClientRequestError() as ex:
            LOG.error("Error deleting pool: %s", ex)
            self.manager.failed_completion(context, pool)


class MemberManager(ManagerBase):

    def create(self, context, member):
        LOG.debug("KEMP driver create member: %s" % repr(member))
        prep_member = self.api_helper.prepare_member(context, member)
        try:
            self.client.create_real_server(prep_member)
            self.manager.successful_completion(context, member)
        except client.KempClientRequestError() as ex:
            LOG.error("Error updating pool: %s", ex)
            self.manager.failed_completion(context, member)

    def update(self, context, old_member, member):
        LOG.debug("KEMP driver update member: %s" % repr(member))
        old_prep_member = self.api_helper.prepare_member(context, old_member)
        prep_member = self.api_helper.prepare_member(context, member)
        try:
            self.client.update_real_server(old_prep_member, prep_member)
            self.manager.successful_completion(context, member)
        except client.KempClientRequestError() as ex:
            LOG.error("Error updating member: %s", ex)
            self.driver.plugin.db.delete_member(context, member.id)
            self.manager.failed_completion(context, member)

    def delete(self, context, member):
        LOG.debug("KEMP driver delete member: %s" % repr(member))
        prep_member = self.api_helper.prepare_member(context, member)
        try:
            self.client.delete_real_server(prep_member)
            self.manager.successful_completion(context, member, delete=True)
        except client.KempClientRequestError() as ex:
            LOG.error("Error deleting member: %s", ex)
            self.driver.plugin.db.delete_member(context, member.id)
            self.manager.failed_completion(context, member)


class HealthMonitorManager(ManagerBase):

    def create(self, context, health_monitor):
        LOG.debug("KEMP driver create health_monitor['type']: %s"
                  % health_monitor['type'])
        check_params = self._get_health_check_params(health_monitor)
        if "http" in health_monitor['type']:
            params = self.api_helper.prepare_health_monitor(health_monitor)
            check_params.update(params)
        try:
            self.client.update_health_check(check_params)
            self.manager.successful_completion(context, health_monitor)
        except client.KempClientRequestError() as ex:
            LOG.error("Error creating health monitor: %s", ex)
            self.manager.failed_completion(context, health_monitor)

    def update(self, context, old_health_monitor, health_monitor):
        LOG.debug("KEMP driver update health_monitor: %s" %
                  repr(health_monitor))
        check_params = self._get_health_check_params(health_monitor)
        if "http" in health_monitor['type']:
            params = self.api_helper.prepare_health_monitor(health_monitor)
            check_params.update(params)
        try:
            self.client.update_health_check(check_params)
            self.manager.successful_completion(context, health_monitor)
        except client.KempClientRequestError() as ex:
            LOG.error("Error updating health monitor: %s", ex)
            self.manager.failed_completion(context, health_monitor)

    def delete(self, context, health_monitor):
        LOG.debug("KEMP driver delete health_monitor: %s" %
                  repr(health_monitor))
        check_params = self._get_health_check_params(health_monitor)
        if "http" in health_monitor['type']:
            params = self.api_helper.prepare_health_monitor(health_monitor)
            check_params.update(params)
        try:
            self.client.update_health_check(check_params)
            self.manager.successful_completion(context, health_monitor,
                                               delete=True)
        except client.KempClientRequestError() as ex:
            LOG.error("Error deleting health monitor: %s", ex)
            self.manager.failed_completion(context, health_monitor)
            self.driver.plugin.db.health_monitor(context, health_monitor.id)

    @staticmethod
    def _get_health_check_params(health_monitor):
        """Return health check parameters from a health monitor."""
        check_params = {
            'retryinterval': health_monitor['delay'],
            'timeout': health_monitor['timeout'],
            'retrycount': health_monitor['max_retries'],
        }
        return check_params


class MapNeutronToKemp(object):

    MAP_NEUTRON_MODEL_TO_VS = {
        'vip_address': 'vs',
        'protocol_port': 'port',
        'protocol': 'prot',
        'lb_method': 'schedule',
        'type': 'checktype',
        'http_method': 'checkuseget',
        'url_path': 'checkurl',
    }

    MAP_NEUTRON_MODEL_TO_RS = {
        'address': 'rs',
        'protocol_port': 'rsport',
        'weight': 'weight',
    }

    def __init__(self, plugin):
        self.plugin = plugin

    def prepare_load_balancer(self, context, loadbalancer):
        pass

    def prepare_listener(self, context, listener):
        pass

    def prepare_pool(self, context, pool):
        health_monitor = pool.healthmonitor or None
        listener = pool.listener
        loadbalancer = pool.root_loadbalancer
        vs_params = {}
        for model in [listener, loadbalancer, pool, health_monitor]:
            for key in dir(model):
                if not key.startswith('__') and not callable(getattr(model, key)):
                    vs_key = self.MAP_NEUTRON_MODEL_TO_VS.get(key)
                    value = model.key
                    if key == "lb_algorithm":
                        vs_params[vs_key] = kemp_consts.LB_METHODS.get(value)
                    elif key == "http_method":
                        if model.http_method == "GET":
                            vs_params[vs_key] = 1
                        else:
                            vs_params[vs_key] = 0
                    elif vs_key is not None:
                        vs_params[vs_key] = value

        # Need to explicitly set vstype if port and
        # protocol do not meet default requirements
        if (("HTTP" in vs_params['prot']) and
                    vs_params['port'] != 80 and
                    vs_params['port'] != 443):
            vs_params['vstype'] = 'http'

        if pool.session_persistence is not None:
            for session_persist in lb_constants.SUPPORTED_SP_TYPES:
                if session_persist == pool.session_persistence.type:
                    persistence = kemp_consts.PERSIST_OPTS[session_persist]
                    vs_params['persist'] = persistence
                    if persistence == kemp_consts.PERS_ACT_COOKIE:
                        cookie = pool.session_persistence.cookie_name
                        vs_params['cookie'] = cookie
        return vs_params

    def prepare_member(self, member):
        rs_params = {}
        for key in dir(member):
            if not key.startswith('__') and not callable(getattr(member, key)):
                api_param = self.MAP_NEUTRON_MODEL_TO_RS.get(key)
                if api_param is not None:
                    rs_params[api_param] = member.key
        for key in dir(member.pool.listener):
            if key in kemp_consts.VS_ID:
                api_param = self.MAP_NEUTRON_MODEL_TO_VS.get(key)
                if api_param is not None:
                    rs_params[api_param] = member.key
        return rs_params

    def prepare_health_monitor(self, health_monitor):
        """Return prepare_pool to update the VS."""
        prep_hm = self.prepare_pool(health_monitor.pool)
        return prep_hm


class KempLoadMasterDriver(object):
    """KEMPtechnologies LBaaS driver."""

    def __init__(self, driver, config):
        try:
            self.address = config.lm_address
            self.username = config.lm_username
            self.password = config.lm_password
            self.check_interval = config.check_interval
            self.connect_timeout = config.connect_timeout
            self.retry_count = config.retry_count
            self.client = client.KempClient(self.address, self.username,
                                            self.password)
        except (cfg.NoSuchOptError, client.KempClientRequestError) as error:
            LOG.error(error)
        self.openstack_driver = driver
        self.plugin = self.openstack_driver.plugin
        self.api_helper = MapNeutronToKemp(self.plugin)

    @property
    def load_balancer(self):
        return LoadBalancerManager(self, self.openstack_driver.load_balancer)

    @property
    def listener(self):
        return ListenerManager(self, self.openstack_driver.listener)

    @property
    def pool(self):
        return PoolManager(self, self.openstack_driver.pool)

    @property
    def member(self):
        return MemberManager(self, self.openstack_driver.member)

    @property
    def health_monitor(self):
        return HealthMonitorManager(self, self.openstack_driver.health_monitor)

    def default_checker_settings(self):
        """Return default health check parameters."""
        return {
            'retryinterval': self.check_interval,
            'timeout': self.connect_timeout,
            'retrycount': self.retry_count,
        }
