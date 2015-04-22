
from oslo.config import cfg

from neutron.api.v2 import attributes
from neutron.db.loadbalancer import loadbalancer_db
from neutron.db.loadbalancer.loadbalancer_db import Controller
from neutron.openstack.common import log as logging
from neutron.plugins.common import constants
from neutron.services.loadbalancer.drivers import abstract_driver
from neutron.services.loadbalancer.drivers.pardnet import pardnet_client
#from neutron.services.loadbalancer.drivers.netscaler import ncc_client

import sqlalchemy as sa
from neutron.openstack.common import uuidutils
from neutron.db import common_db_mixin as base_db
from neutron.db import model_base
from neutron.db import models_v2

import time

LOG = logging.getLogger(__name__)

"""declare usable config items from 'odl' section"""
ODL_OPTS = [
    cfg.StrOpt(
        'odl_ip',
        help=_('The ip address of the opendaylight controller.'),
    ),
    cfg.StrOpt(
        'odl_uri',
        help=_('The URL to reach the opendaylight controller.'),
    ),
    cfg.StrOpt(
        'odl_username',
        help=_('Username to login to the opendaylight controller.'),
    ),
    cfg.StrOpt(
        'odl_password',
        help=_('Password to login to the opendaylight controller.'),
    ),
    cfg.StrOpt(
        'odl_switch_node_type',
        help=_('node_type of the switch.'),
    ),
    cfg.StrOpt(
        'odl_switch_node_id',
        help=_('node_id of the switch.'),
    )
]
"""Get configurations from section 'odl' of the argument --config-file pardnet.conf """
cfg.CONF.register_opts(ODL_OPTS, 'odl')

"""declare usable config items from 'ha' section"""
HA_OPTS = [
    cfg.StrOpt(
        'vip',
        help=_('vip of the pool.'),
    ),
    cfg.StrOpt(
        'ha_info_entries',
        help=_('information entries of haproxy.'),
    ),
    cfg.StrOpt(
        'sourceip_map',
        help=_('souce ip mapping rules.'),
    )
]
"""Get configurations from section 'ha' of the argument --config-file pardnet.conf """
cfg.CONF.register_opts(HA_OPTS, 'ha')


PARDNET_OPTS = [
    cfg.StrOpt(
        'pardnet_ip',
        help=_('ip of the pardnet loadbalancer.'),
    ),
    cfg.StrOpt(
        'pardnet_port',
        help=_('port of the pardnet loadbalancer.'),
    )
]
"""Get configurations from section 'ha' of the argument --config-file pardnet.conf """
cfg.CONF.register_opts(PARDNET_OPTS, 'pardnet')




"""
VIPS_RESOURCE = 'vips'
VIP_RESOURCE = 'vip'
POOLS_RESOURCE = 'pools'
POOL_RESOURCE = 'pool'
POOLMEMBERS_RESOURCE = 'members'
POOLMEMBER_RESOURCE = 'member'
MONITORS_RESOURCE = 'healthmonitors'
MONITOR_RESOURCE = 'healthmonitor'
POOLSTATS_RESOURCE = 'statistics'
PROV_SEGMT_ID = 'provider:segmentation_id'
PROV_NET_TYPE = 'provider:network_type'
DRIVER_NAME = 'pardnet_driver'
"""

"""pardnet_driver DBs"""

class Haproxy(model_base.BASEV2, models_v2.HasId,
               models_v2.HasTenant, models_v2.HasStatusDescription):
    """Represents an haproxy instance."""
    __tablename__ = 'haproxies'
    name = sa.Column(sa.String(255))
    description = sa.Column(sa.String(255))
    address = sa.Column(sa.String(64), nullable=False)
    mac_address = sa.Column(sa.String(32), nullable=False)
    pool_id = sa.Column(sa.String(36), sa.ForeignKey("pools.id"),
                        nullable=False)
    member_id_list = sa.Column(sa.String(3600), nullable=False)
    admin_state_up = sa.Column(sa.Boolean(), nullable=False)


# class Controller(model_base.BASEV2, models_v2.HasId,
#                models_v2.HasTenant, models_v2.HasStatusDescription):
#     """Represents a controller instance."""
#     __tablename__ = 'controllers'
#     name = sa.Column(sa.String(255))
#     description = sa.Column(sa.String(255))
#     address = sa.Column(sa.String(64), nullable=False)
#     pool_id = sa.Column(sa.String(36), sa.ForeignKey("pools.id"),
#                         nullable=False)
#     admin_state_up = sa.Column(sa.Boolean(), nullable=False)
    
class Switch(model_base.BASEV2, models_v2.HasId,
               models_v2.HasTenant, models_v2.HasStatusDescription):
    """Represents a switch instance."""
    __tablename__ = 'switches'
    name = sa.Column(sa.String(255))
    description = sa.Column(sa.String(255))
    address = sa.Column(sa.String(64), nullable=False)
    controller_id = sa.Column(sa.String(36), sa.ForeignKey("controllers.id"),
                        nullable=False)
    dpid = sa.Column(sa.String(23), nullable=False)
    pool_id = sa.Column(sa.String(36), sa.ForeignKey("pools.id"),
                        nullable=False)
    admin_state_up = sa.Column(sa.Boolean(), nullable=False)


class PardnetPluginDriver(abstract_driver.LoadBalancerAbstractDriver,
                          base_db.CommonDbMixin):

    """Pardnet LBaaS Plugin driver class."""

    def __init__(self, plugin):
        """constructor"""
        self.plugin = plugin
        """prepare arguments for instantiating PardnetClient object"""
        odl_uri = cfg.CONF.odl.odl_uri
        odl_username = cfg.CONF.odl.odl_username
        odl_password = cfg.CONF.odl.odl_password
        odl_switch_node_type = cfg.CONF.odl.odl_switch_node_type
        odl_switch_node_id = cfg.CONF.odl.odl_switch_node_id
        vip = cfg.CONF.ha.vip
        ha_info_entries = cfg.CONF.ha.ha_info_entries
        sourceip_map = cfg.CONF.ha.sourceip_map
        """combine a string like this"""
        #http://192.168.0.117:8080/controller/nb/v2/flowprogrammer/default/node/{nodeType}/{nodeId}/staticFlow/
#         odl_flow_url = "%s/%s/%s/%s/%s" % (odl_uri, "node", odl_switch_node_type, odl_switch_node_id, "staticFlow")
#         self.client = pardnet_client.PardnetClient(odl_flow_url,
#                                                    odl_username,
#                                                    odl_password,
#                                                    odl_switch_node_type=odl_switch_node_type,
#                                                    odl_switch_node_id=odl_switch_node_id,
#                                                    vip=vip,
#                                                    ha_info_entries=ha_info_entries,
#                                                    sourceip_map=sourceip_map
#                                                    )
        pardnet_ip = cfg.CONF.pardnet.pardnet_ip
        pardnet_port = cfg.CONF.pardnet.pardnet_port
        self.client = pardnet_client.PardnetClient(pardnet_ip, pardnet_port)


    def create_vip(self, context, vip):
        """Create a vip on a Pardnet loadbalancer pool."""
        #for key,value in vip.items():
        #    print key, ":", value
        """call create_vip method of PardnetClient"""
        self.client.create_vip(context, vip)
        
        """update status of vip"""
        status = constants.ACTIVE
        self.plugin.update_status(context, loadbalancer_db.Vip,
                                  vip["id"], status)
        #print context['tenant_name']
        #time.sleep(15)


    def update_vip(self, context, old_vip, vip):
        """Update a vip on a NetScaler device.
        update_vip = self._prepare_vip_for_update(vip)
        resource_path = "%s/%s" % (VIPS_RESOURCE, vip["id"])
        msg = (_("NetScaler driver vip %(vip_id)s update: %(vip_obj)s") %
               {"vip_id": vip["id"], "vip_obj": repr(vip)})
        LOG.debug(msg)
        status = constants.ACTIVE
        try:
            self.client.update_resource(context.tenant_id, resource_path,
                                        VIP_RESOURCE, update_vip)
        except ncc_client.NCCException:
            status = constants.ERROR
        self.plugin.update_status(context, loadbalancer_db.Vip, old_vip["id"],
                                  status)"""
        pass

    def delete_vip(self, context, vip):
        """do nothing but delete records of vip from mysql"""
        self.client.delete_vip(context, vip)
        self.plugin._delete_db_vip(context, vip['id'])
    def create_pool(self, context, pool):
        """Create a pool on a NetScaler device.
        network_info = self._get_pool_network_info(context, pool)
        #allocate a snat port/ipaddress on the subnet if one doesn't exist
        self._create_snatport_for_subnet_if_not_exists(context,
                                                       pool['tenant_id'],
                                                       pool['subnet_id'],
                                                       network_info)
        ncc_pool = self._prepare_pool_for_creation(pool)
        ncc_pool = dict(ncc_pool.items() + network_info.items())
        msg = _("NetScaler driver pool creation: %s") % repr(ncc_pool)
        LOG.debug(msg)
        status = constants.ACTIVE
        try:
            self.client.create_resource(context.tenant_id, POOLS_RESOURCE,
                                        POOL_RESOURCE, ncc_pool)
        except ncc_client.NCCException:
            status = constants.ERROR
        self.plugin.update_status(context, loadbalancer_db.Pool,
                                  ncc_pool["id"], status)"""
#         for key,value in pool.items():
#             print key, ":", value
#         
#         #print context.session
#         
#         #print pool
#         #v = pool['pool']
# 
#         tenant_id = self._get_tenant_id_for_create(context, pool)
#         
#         with context.session.begin(subtransactions=True):
#             haproxy_ids = []
#             for ha_info in cfg.CONF.ha.ha_info_entries.split(","):
#                 ha_info_list = ha_info.split("|")
#                 haproxy_db = Haproxy(id=uuidutils.generate_uuid(),
#                                tenant_id=tenant_id,
#                                name=ha_info_list[0],
#                                description='description',
#                                address = ha_info_list[1],
#                                mac_address = ha_info_list[2],
#                                pool_id = pool['id'],
#                                member_id_list = '',
#                                admin_state_up = 1,
#                                status=constants.PENDING_CREATE)
#                 context.session.add(haproxy_db)
#                 haproxy_ids.append(haproxy_db.id)
#             
#             controller_db = Controller(id=uuidutils.generate_uuid(),
#                                        tenant_id=tenant_id,
#                                        name='opendaylight',
#                                        description='description',
#                                        address = cfg.CONF.odl.odl_ip,
#                                        pool_id = pool['id'],
#                                        admin_state_up = 1,
#                                        status=constants.PENDING_CREATE)
#             context.session.add(controller_db)
#             
#             query = context.session.query(Controller.id)
#             switch_db = Switch(id=uuidutils.generate_uuid(),
#                                tenant_id=tenant_id,
#                                name=cfg.CONF.odl.odl_switch_node_id,
#                                description='description',
#                                address = '192.168.0.xx',
#                                controller_id = query.all()[0][0],
#                                dpid = cfg.CONF.odl.odl_switch_node_id,
#                                pool_id = pool['id'],
#                                admin_state_up = 1,
#                                status=constants.PENDING_CREATE)
#             context.session.add(switch_db)
#             
        self.client.create_pool(context, pool)
         
        status = constants.ACTIVE
        self.plugin.update_status(context, loadbalancer_db.Pool,
                                  pool["id"], status)
#         for haproxy_id in haproxy_ids:
#             self.plugin.update_status(context, Haproxy, haproxy_id, status)
#         self.plugin.update_status(context, Controller, controller_db.id, status)
#         self.plugin.update_status(context, Switch, switch_db.id, status)
        #print context['tenant_name']

    def update_pool(self, context, old_pool, pool):
        """Update a pool on a NetScaler device.
        ncc_pool = self._prepare_pool_for_update(pool)
        resource_path = "%s/%s" % (POOLS_RESOURCE, old_pool["id"])
        msg = (_("NetScaler driver pool %(pool_id)s update: %(pool_obj)s") %
               {"pool_id": old_pool["id"], "pool_obj": repr(ncc_pool)})
        LOG.debug(msg)
        status = constants.ACTIVE
        try:
            self.client.update_resource(context.tenant_id, resource_path,
                                        POOL_RESOURCE, ncc_pool)
        except ncc_client.NCCException:
            status = constants.ERROR
        self.plugin.update_status(context, loadbalancer_db.Pool,
                                  old_pool["id"], status)"""
        status = constants.ACTIVE
        self.plugin.update_status(context, loadbalancer_db.Pool,
                                  pool["id"], status)
    def delete_pool(self, context, pool):
        """Delete a pool on a NetScaler device.
        resource_path = "%s/%s" % (POOLS_RESOURCE, pool['id'])
        msg = _("NetScaler driver pool removal: %s") % pool["id"]
        LOG.debug(msg)
        try:
            self.client.remove_resource(context.tenant_id, resource_path)
        except ncc_client.NCCException:
            self.plugin.update_status(context, loadbalancer_db.Pool,
                                      pool["id"],
                                      constants.ERROR)
        else:
            self.plugin._delete_db_pool(context, pool['id'])
            self._remove_snatport_for_subnet_if_not_used(context,
                                                         pool['tenant_id'],
                                                         pool['subnet_id'])"""
        
#         session = context.session
#         with session.begin(subtransactions=True):
#             
#             
#             query = session.query(Switch.id).filter(Switch.pool_id == pool['id'])
#             switch_db = self._get_by_id(context, Switch, query.all()[0][0])
#             session.delete(switch_db)
#             
#             query = session.query(Controller.id).filter(Controller.pool_id == pool['id'])
#             controller_db = self._get_by_id(context, Controller, query.all()[0][0])
#             session.delete(controller_db)
#             
#             query = session.query(Haproxy.id).filter(Haproxy.pool_id == pool['id'])
#             for haproxy_id in query.all():
#                 print haproxy_id[0]
#                 haproxy_db = self._get_by_id(context, Haproxy, haproxy_id[0])
#                 session.delete(haproxy_db)
            #haproxy_db = self._get_by_id(context, Haproxy, id)
            #session.delete(haproxy_db)
            
            #session.delete
        
        
        self.plugin._delete_db_pool(context, pool['id'])


#     def create_test(self, context, test):
#         
#         self.client.create_test(context, test)
#         
#         status = constants.ACTIVE
#         self.plugin.update_status(context, loadbalancer_db.Test,
#                                   test["id"], status)


    def create_member(self, context, member):
        """Create a pool member on a NetScaler device.
        ncc_member = self._prepare_member_for_creation(member)
        msg = (_("NetScaler driver poolmember creation: %s") %
               repr(ncc_member))
        LOG.info(msg)
        status = constants.ACTIVE
        try:
            self.client.create_resource(context.tenant_id,
                                        POOLMEMBERS_RESOURCE,
                                        POOLMEMBER_RESOURCE,
                                        ncc_member)
        except ncc_client.NCCException:
            status = constants.ERROR
        self.plugin.update_status(context, loadbalancer_db.Member,
                                  member["id"], status)"""
        pass
    def update_member(self, context, old_member, member):
        """Update a pool member on a NetScaler device.
        ncc_member = self._prepare_member_for_update(member)
        resource_path = "%s/%s" % (POOLMEMBERS_RESOURCE, old_member["id"])
        msg = (_("NetScaler driver poolmember %(member_id)s update:"
                 " %(member_obj)s") %
               {"member_id": old_member["id"],
                "member_obj": repr(ncc_member)})
        LOG.debug(msg)
        status = constants.ACTIVE
        try:
            self.client.update_resource(context.tenant_id, resource_path,
                                        POOLMEMBER_RESOURCE, ncc_member)
        except ncc_client.NCCException:
            status = constants.ERROR
        self.plugin.update_status(context, loadbalancer_db.Member,
                                  old_member["id"], status)"""
        pass
    def delete_member(self, context, member):
        """Delete a pool member on a NetScaler device.
        resource_path = "%s/%s" % (POOLMEMBERS_RESOURCE, member['id'])
        msg = (_("NetScaler driver poolmember removal: %s") %
               member["id"])
        LOG.debug(msg)
        try:
            self.client.remove_resource(context.tenant_id, resource_path)
        except ncc_client.NCCException:
            self.plugin.update_status(context, loadbalancer_db.Member,
                                      member["id"],
                                      constants.ERROR)
        else:
            self.plugin._delete_db_member(context, member['id'])"""
        pass
    def create_pool_health_monitor(self, context, health_monitor, pool_id):
        """Create a pool health monitor on a NetScaler device.
        ncc_hm = self._prepare_healthmonitor_for_creation(health_monitor,
                                                          pool_id)
        resource_path = "%s/%s/%s" % (POOLS_RESOURCE, pool_id,
                                      MONITORS_RESOURCE)
        msg = (_("NetScaler driver healthmonitor creation for pool %(pool_id)s"
                 ": %(monitor_obj)s") %
               {"pool_id": pool_id,
                "monitor_obj": repr(ncc_hm)})
        LOG.debug(msg)
        status = constants.ACTIVE
        try:
            self.client.create_resource(context.tenant_id, resource_path,
                                        MONITOR_RESOURCE,
                                        ncc_hm)
        except ncc_client.NCCException:
            status = constants.ERROR
        self.plugin.update_pool_health_monitor(context,
                                               health_monitor['id'],
                                               pool_id,
                                               status, "")"""
        pass
    def update_pool_health_monitor(self, context, old_health_monitor,
                                   health_monitor, pool_id):
        """Update a pool health monitor on a NetScaler device.
        ncc_hm = self._prepare_healthmonitor_for_update(health_monitor)
        resource_path = "%s/%s" % (MONITORS_RESOURCE,
                                   old_health_monitor["id"])
        msg = (_("NetScaler driver healthmonitor %(monitor_id)s update: "
                 "%(monitor_obj)s") %
               {"monitor_id": old_health_monitor["id"],
                "monitor_obj": repr(ncc_hm)})
        LOG.debug(msg)
        status = constants.ACTIVE
        try:
            self.client.update_resource(context.tenant_id, resource_path,
                                        MONITOR_RESOURCE, ncc_hm)
        except ncc_client.NCCException:
            status = constants.ERROR
        self.plugin.update_pool_health_monitor(context,
                                               old_health_monitor['id'],
                                               pool_id,
                                               status, "")"""
        pass
    def delete_pool_health_monitor(self, context, health_monitor, pool_id):
        """Delete a pool health monitor on a NetScaler device.
        resource_path = "%s/%s/%s/%s" % (POOLS_RESOURCE, pool_id,
                                         MONITORS_RESOURCE,
                                         health_monitor["id"])
        msg = (_("NetScaler driver healthmonitor %(monitor_id)s"
                 "removal for pool %(pool_id)s") %
               {"monitor_id": health_monitor["id"],
                "pool_id": pool_id})
        LOG.debug(msg)
        try:
            self.client.remove_resource(context.tenant_id, resource_path)
        except ncc_client.NCCException:
            self.plugin.update_pool_health_monitor(context,
                                                   health_monitor['id'],
                                                   pool_id,
                                                   constants.ERROR, "")
        else:
            self.plugin._delete_db_pool_health_monitor(context,
                                                       health_monitor['id'],
                                                       pool_id)"""
        pass
    def stats(self, context, pool_id):
        """Retrieve pool statistics from the NetScaler device.
        resource_path = "%s/%s" % (POOLSTATS_RESOURCE, pool_id)
        msg = _("NetScaler driver pool stats retrieval: %s") % pool_id
        LOG.debug(msg)
        try:
            stats = self.client.retrieve_resource(context.tenant_id,
                                                  resource_path)[1]
        except ncc_client.NCCException:
            self.plugin.update_status(context, loadbalancer_db.Pool,
                                      pool_id, constants.ERROR)
        else:
            return stats"""
        pass
