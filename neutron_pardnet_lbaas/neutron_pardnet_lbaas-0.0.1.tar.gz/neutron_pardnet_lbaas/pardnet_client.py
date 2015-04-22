
import base64
import requests
import json

from neutron.agent.linux import utils as linux_utils
from neutron.openstack.common import log as logging

"""some version may using this file"""
#from neutron.openstack.common import jsonutils

from oslo.serialization import jsonutils

from math import log


    

CONTENT_TYPE_HEADER = 'Content-type'
ACCEPT_HEADER = 'Accept'
AUTH_HEADER = 'Authorization'
DRIVER_HEADER = 'X-OpenStack-LBaaS'
TENANT_HEADER = 'X-Tenant-ID'
JSON_CONTENT_TYPE = 'application/json'
#DRIVER_HEADER_VALUE = 'netscaler-openstack-lbaas'



import time

LOG = logging.getLogger(__name__)


class PardnetClient(object):
#     def __init__(self, odl_flow_url, odl_username, odl_password, **kw):
    def __init__(self, pardnet_ip, pardnet_port):
        #self.service_uri = service_uri.strip('/')
        self.pardnet_uri = "http://%s:%s" % (pardnet_ip, pardnet_port)
#         self.auth = None
#         
#         response_status, resp_dict = self.retrieve_resource(self.pardnet_uri, "controllers")
#         controller_list = json.loads(resp_dict["body"])["controllers"]
#         #TODO only one controller and one switch for now 
#         controller = controller_list[0]
# 
#         response_status, resp_dict = self.retrieve_resource(self.pardnet_uri, "switches")
#         switch_list = json.loads(resp_dict["body"])["switches"]
#         #TODO only one controller and one switch for now 
#         switch = switch_list[0]
#         
#         
#         response_status, resp_dict = self.retrieve_resource(self.pardnet_uri, "haproxies")
#         self.haproxy_list = json.loads(resp_dict["body"])["haproxies"]
#         
#         
#         
#         self.odl_switch_node_type = switch["node_type"]
#         self.odl_switch_node_id = switch["dpid"]
#         odl_uri = "http://%s:8080" % controller["address"]
#         
#         self.odl_flow_url = "%s/%s/%s/%s/%s" % (odl_uri, "node", self.odl_switch_node_type, self.odl_switch_node_id, "staticFlow")
#         base64string = base64.encodestring("%s:%s" % (controller["username"], controller["password"]))
#         base64string = base64string[:-1]
#         """Authorization Header"""
#         self.auth = 'Basic %s' % base64string
# #         self.vip = kw['vip']
# #         self.ha_info_entries = kw['ha_info_entries']
#         #self.sourceip_map = kw['sourceip_map']
#         """initialize self.ha_info"""
#         self._initialize_ha_info_list()
        
    def create_pool(self, context, pool):
        """nothing to do now"""
        #self._send_file_to_haproxys(pool)
        pass

    def create_vip(self, context, vip):
        """create the flow entries for vip and send to switch """
        #print self.service_uri
        #print self.auth
        
        #response_status, resp_dict = self.update_resource("test", None, '{"priority":"0","hardTimeout":"0","actions":["DROP"],"node":{"id":"00:00:00:19:99:b1:9f:a8","type":"OF"},"installInHw":"true","name":"test"}')
#         time.sleep(15)
        request_vip = {
                       "protocol": vip["protocol"],
                       "description": vip["description"],
                       "address": vip["address"],
                       "protocol_port": vip["protocol_port"],
                       "name": vip["name"],
                       "admin_state_up": vip["admin_state_up"],
                       "subnet_id": vip["subnet_id"],
                       "tenant_id": vip["tenant_id"],
                       "connection_limit": vip["connection_limit"],
                       "pool_id": vip["pool_id"],
                       "session_persistence": vip["session_persistence"],
                       }
        self.create_resource(self.pardnet_uri, "vips", "vip", request_vip)
        


#         """create the flow entries for vip"""
#         flow_dict = self._sourceip_flow_dict()
#         """send to switch"""
#         for key in flow_dict.keys():
#             self.update_resource(self.odl_flow_url, key, None, json.dumps(flow_dict[key]))



    def delete_vip(self, context, vip):
        self.remove_resource(self.pardnet_uri, "vips/%s" % vip["address"].replace(".", "_"))
    
    def create_test(self, context, test):
        ip = "192.168.0.11"
        cmd = ['arp', '-n', ip]
        
        print '---------------', linux_utils.execute(cmd)
    
    def _send_file_to_haproxys(self, pool):
        """test of executing commands"""
        cmd = ['ifconfig', 'eth0']
        linux_utils.execute(cmd)
        
    
    def _sourceip_flow_dict(self):
        """return the flow dictionary with key of flow_name and value of flow_config dictionary"""
        return_dict = {}
        
        haproxy_num = len(self.ha_info_entries.split(","))
        cidr_suffix = int(log(haproxy_num, 2)) + 1
        subnet_num = 2 ** (cidr_suffix)
        
        for i in range(subnet_num):
            index = i % haproxy_num
            actions = []
            set_dl_dst = "SET_DL_DST=%s" % self.ha_info[index]["ha_mac"]
            output = "OUTPUT=%s" % self.ha_info[index]["ha_ofport"]
            actions.append(set_dl_dst)
            actions.append(output)
            
            if subnet_num <= 256:
                """if i == 0 , set address to 0"""
                source_ip = "%s.0.0.0/%s" % (str(i * (2 ** (8 - cidr_suffix))), cidr_suffix)
            
            flow_name = source_ip.replace("/", "_")
            return_dict[flow_name] = self._create_flow_dict(flow_name,
                                                            self.odl_switch_node_type,
                                                            self.odl_switch_node_id,
                                                            "500",
                                                            actions,
                                                            True,
                                                            nwSrc=source_ip,
                                                            nwDst=self.vip,
                                                            etherType="0x800"
                                                            )
            
            
        
#         for ip_host in self._sourceip_map_to_list():xxxxxxx
#             actions = []
#             set_dl_dst = "SET_DL_DST=%s" % self.ha_info[ip_host["dst_ha_name"]]["ha_mac"]
#             output = "OUTPUT=%s" % self.ha_info[ip_host["dst_ha_name"]]["ha_ofport"]
#             actions.append(set_dl_dst)
#             actions.append(output)
#              
#             flow_name = ip_host["source_ip"].replace("/", "_")
#             return_dict[flow_name] = self._create_flow_dict(flow_name,
#                                                             self.odl_switch_node_type,
#                                                             self.odl_switch_node_id,
#                                                             "500",
#                                                             actions,
#                                                             True,
#                                                             nwSrc=ip_host["source_ip"],
#                                                             nwDst=self.vip,
#                                                             etherType="0x800"
#                                                             )
        return return_dict
    
#     def _initialize_ha_info_list(self):
#         """initialize self.ha_info"""
#         self.ha_info = []
#         for ha_info_entry in self.ha_info_entries.split(","):
#             ha_info = ha_info_entry.split("|")
#             #self.ha_info[ha_info[0]] = (ha_info[1],ha_info[2],ha_info[3])
#             self.ha_info.append({"ha_ip": ha_info[1],
#                                         "ha_mac": ha_info[2],
#                                         "ha_ofport": ha_info[3]
#                                         })
        #return return_list
        
        
    def _get_mac_by_ip(self, ip):
        return "00:00:00:00:00:00"
    
    def _get_ofport(self):
        return "1"
    
        
    def _initialize_ha_info_list(self):
        """initialize self.ha_info"""
        self.ha_info = []
        for haproxy in self.haproxy_list:
            self.ha_info.append({"ha_ip": haproxy["address"],
                                 "ha_mac": self._get_mac_by_ip(haproxy["address"]),
                                 "ha_ofport": self._get_ofport()})
    
        
    
    def _sourceip_map_to_list(self):
        """return a list of source_ip,dst_ha_name pair"""
        return_list = []
        for sourceip in self.sourceip_map.split(","):
            ip_host = sourceip.split("|")
            return_list.append({
                                "source_ip": ip_host[0],
                                "dst_ha_name": ip_host[1]
                                })
            #ip = ip_host[0]
            #host= ip_host[1]
        return return_list
    
    def _create_flow_dict(self, name, node_type, node_id, priority, actions, installInHw=True, **kw):
        """return a flow_config dictionary"""
        #return '{"priority":"0","hardTimeout":"0","actions":["DROP"],"node":{"id":"00:00:00:0c:29:d2:16:cf","type":"OF"},"installInHw":"true","name":"test"}'
        return_dict = {"priority": priority,
                       "actions": actions,
                       "node": {"id": node_id, "type": node_type},
                       "installInHw": installInHw,
                       "name": name
                       }
        if kw["nwSrc"]:
            return_dict["nwSrc"] = kw["nwSrc"]
        if kw["nwDst"]:
            return_dict["nwDst"] = kw["nwDst"]
        if kw["etherType"]:
            return_dict["etherType"] = kw["etherType"]
        return return_dict
        
    def create_resource(self, service_uri, resource_path, object_name,
                        object_data):
        """Create a resource of flow entry"""
        return self._resource_operation(service_uri,
                                        'POST',
                                        resource_path,
                                        object_name=object_name,
                                        object_data=object_data)

    def retrieve_resource(self, service_uri, resource_path, parse_response=True):
        """Retrieve a resource of NetScaler Control Center."""
        return self._resource_operation(service_uri, 'GET', resource_path)

    def update_resource(self, service_uri, resource_path, object_name,
                        object_data):
        """Update a resource of the NetScaler Control Center."""
        return self._resource_operation(service_uri,
                                        'PUT',
                                        resource_path,
                                        object_name=object_name,
                                        object_data=object_data)

    def remove_resource(self, service_uri, resource_path, parse_response=True):
        """Remove a resource of NetScaler Control Center."""
        return self._resource_operation(service_uri, 'DELETE', resource_path)

    def _resource_operation(self, service_uri, method, resource_path,
                            object_name=None, object_data=None):
        resource_uri = "%s/%s" % (service_uri, resource_path)
        headers = self._setup_req_headers()
        request_body = None
        if object_data:
            if isinstance(object_data, str):
                request_body = object_data
            else:
                obj_dict = {object_name: object_data}
                request_body = jsonutils.dumps(obj_dict)

        response_status, resp_dict = self._execute_request(method,
                                                           resource_uri,
                                                           headers,
                                                           body=request_body)
        return response_status, resp_dict

    def _is_valid_response(self, response_status):
        # when status is less than 400, the response is fine
        return response_status < requests.codes.bad_request

    def _setup_req_headers(self):
        headers = {ACCEPT_HEADER: JSON_CONTENT_TYPE,
                   CONTENT_TYPE_HEADER: JSON_CONTENT_TYPE,
                   #DRIVER_HEADER: DRIVER_HEADER_VALUE,
                   #TENANT_HEADER: tenant_id,
                   #AUTH_HEADER: self.auth
                   }
        return headers

    def _get_response_dict(self, response):
        response_dict = {'status': response.status_code,
                         'body': response.text,
                         'headers': response.headers}
        if self._is_valid_response(response.status_code):
            if response.text:
                #response_dict['dict'] = response.json()
                response_dict['dict'] = response
        return response_dict

    def _execute_request(self, method, resource_uri, headers, body=None):
        response = requests.request(method, url=resource_uri, headers=headers,
                                    data=body)
        #print "response : %s" % response
        #time.sleep(15)
        """
        try:
            response = requests.request(method, url=resource_uri,
                                        headers=headers, data=body)
        except requests.exceptions.ConnectionError:
            msg = (_("Connection error occurred while connecting to %s") %
                   self.service_uri)
            LOG.exception(msg)
            raise NCCException(NCCException.CONNECTION_ERROR)
        except requests.exceptions.SSLError:
            msg = (_("SSL error occurred while connecting to %s") %
                   self.service_uri)
            LOG.exception(msg)
            raise NCCException(NCCException.CONNECTION_ERROR)
        except requests.exceptions.Timeout:
            msg = _("Request to %s timed out") % self.service_uri
            LOG.exception(msg)
            raise NCCException(NCCException.CONNECTION_ERROR)
        except (requests.exceptions.URLRequired,
                requests.exceptions.InvalidURL,
                requests.exceptions.MissingSchema,
                requests.exceptions.InvalidSchema):
            msg = _("Request did not specify a valid URL")
            LOG.exception(msg)
            raise NCCException(NCCException.REQUEST_ERROR)
        except requests.exceptions.TooManyRedirects:
            msg = _("Too many redirects occurred for request to %s")
            LOG.exception(msg)
            raise NCCException(NCCException.REQUEST_ERROR)
        except requests.exceptions.RequestException:
            msg = (_("A request error while connecting to %s") %
                   self.service_uri)
            LOG.exception(msg)
            raise NCCException(NCCException.REQUEST_ERROR)
        except Exception:
            msg = (_("A unknown error occurred during request to %s") %
                   self.service_uri)
            LOG.exception(msg)
            raise NCCException(NCCException.UNKNOWN_ERROR)"""
        resp_dict = self._get_response_dict(response)
        LOG.debug(_("Response: %s"), resp_dict['body'])
        response_status = resp_dict['status']
        """
        if response_status == requests.codes.unauthorized:
            LOG.exception(_("Unable to login. Invalid credentials passed."
                          "for: %s"), self.service_uri)
            raise NCCException(NCCException.RESPONSE_ERROR)
        if not self._is_valid_response(response_status):
            msg = (_("Failed %(method)s operation on %(url)s "
                   "status code: %(response_status)s") %
                   {"method": method,
                    "url": resource_uri,
                    "response_status": response_status})
            LOG.exception(msg)
            raise NCCException(NCCException.RESPONSE_ERROR)
        """
        return response_status, resp_dict
