# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock
import webob.exc

from neutron import context
from oslo.config import cfg

from gbpservice.neutron.extensions import group_policy as gpolicy
from gbpservice.neutron.tests.unit.db.grouppolicy import (
    test_group_policy_db as tgpdb)
from gbpservice.neutron.tests.unit.db.grouppolicy import (
    test_group_policy_mapping_db as tgpmdb)


cfg.CONF.import_opt('policy_drivers',
                    'gbpservice.neutron.services.grouppolicy.config',
                    group='group_policy')
GP_PLUGIN_KLASS = (
    "gbpservice.neutron.services.grouppolicy.plugin.GroupPolicyPlugin"
)


class FakeDriver(object):

    def _fill_order(self, context):
        context.call_order.append(self)

    def __getattr__(self, item):
        return self._fill_order


class GroupPolicyPluginTestCase(tgpmdb.GroupPolicyMappingDbTestCase):

    def setUp(self, core_plugin=None, gp_plugin=None):
        if not gp_plugin:
            gp_plugin = GP_PLUGIN_KLASS
        super(GroupPolicyPluginTestCase, self).setUp(core_plugin=core_plugin,
                                                     gp_plugin=gp_plugin)

    def test_reverse_on_delete(self):
        manager = self.plugin.policy_driver_manager
        ctx = context.get_admin_context()
        drivers = manager.ordered_policy_drivers
        first, second = mock.Mock(), mock.Mock()
        first.obj, second.obj = FakeDriver(), FakeDriver()
        try:
            manager.ordered_policy_drivers = [first, second]
            manager.reverse_ordered_policy_drivers = [second, first]
            ordered_obj = [first.obj, second.obj]
            ctx.call_order = []
            manager._call_on_drivers('nodelete', ctx)
            self.assertEqual(ordered_obj, ctx.call_order)
            ctx.call_order = []
            manager._call_on_drivers('delete', ctx)
            self.assertEqual(ordered_obj[::-1], ctx.call_order)
        finally:
            manager.ordered_policy_drivers = drivers

    def _create_l2_policy_on_shared(self, **kwargs):
        l3p = self.create_l3_policy(shared=True)['l3_policy']
        return self.create_l2_policy(l3_policy_id=l3p['id'],
                                     **kwargs)['l2_policy']

    def _create_ptg_on_shared(self, **kwargs):
        l2p = self._create_l2_policy_on_shared(shared=True)
        return self.create_policy_target_group(l2_policy_id=l2p['id'],
                                               **kwargs)

    def _create_rule_on_shared(self, **kwargs):
        pa = self.create_policy_action(action_type='allow',
                                       shared=True)['policy_action']
        cl_attr = {'protocol': 'tcp', 'port_range': 80}
        pc = self.create_policy_classifier(direction='in',
                                           shared=True,
                                           **cl_attr)['policy_classifier']
        return self.create_policy_rule(
            policy_classifier_id=pc['id'],
            policy_actions=[pa['id']], **kwargs)['policy_rule']

    def _create_policy_rule_set_on_shared(self, **kwargs):
        pr = self._create_rule_on_shared(shared=True)
        return self.create_policy_rule_set(policy_rules=[pr['id']],
                                           **kwargs)['policy_rule_set']

    def _create_external_policy_on_shared(self, **kwargs):
        es = self.create_external_segment(shared=True)
        return self.create_external_policy(
            external_segments=[es['external_segment']['id']],
            **kwargs)['external_policy']

    def _create_nat_pool_on_shared(self, **kwargs):
        es = self.create_external_segment(shared=True)
        return self.create_nat_pool(
            external_segment_id=es['external_segment']['id'],
            **kwargs)['nat_pool']


class TestL3Policy(GroupPolicyPluginTestCase):

    def _get_es_dict(self, es, addr=None):
        return {es['external_segment']['id']: addr or []}

    def test_shared_l3_policy_create(self):
        # Verify default is False
        l3p = self.create_l3_policy()
        self.assertEqual(False, l3p['l3_policy']['shared'])
        # Verify shared True created without errors
        l3p = self.create_l3_policy(shared=True)
        self.assertEqual(True, l3p['l3_policy']['shared'])

    def test_shared_l3p_create_with_es(self):
        def combination(l3p, es):
            return {'l3p': l3p, 'es': es}
        allowed = [combination(False, False), combination(True, True),
                   combination(False, True)]
        for shared in allowed:
            es = self.create_external_segment(
                cidr='172.0.0.0/8', shared=shared['es'])
            es_dict = self._get_es_dict(es, ['172.0.0.2', '172.0.0.3'])
            l3p = self.create_l3_policy(
                external_segments=es_dict, shared=shared['l3p'],
                expected_res_status=201)['l3_policy']
            # Verify create successful
            self.assertEqual(es_dict, l3p['external_segments'])

    def test_shared_l3p_create_with_es_negative(self):
        # Not allowed: Unshared ES with shared L3P
        es = self.create_external_segment(cidr='172.0.0.0/8')
        es_dict = self._get_es_dict(es, ['172.0.0.2', '172.0.0.3'])
        res = self.create_l3_policy(external_segments=es_dict,
                                    shared=True,
                                    expected_res_status=400)
        self.assertEqual('SharedResourceReferenceError',
                         res['NeutronError']['type'])

    def test_shared_l3_policy_update(self):
        l3p = self.create_l3_policy()['l3_policy']
        # Accept share if nothing referenced
        self.update_l3_policy(l3p['id'], expected_res_status=200, shared=True)

        # Verify unshare when referenced by private L2P
        self.create_l2_policy(l3_policy_id=l3p['id'])
        self.update_l3_policy(l3p['id'], expected_res_status=200, shared=False)
        es = self.create_external_segment(cidr='172.0.0.0/8')
        es_dict = self._get_es_dict(es, ['172.0.0.2', '172.0.0.3'])
        # Set ES
        l3p = self.update_l3_policy(l3p['id'], expected_res_status=200,
                                    external_segments=es_dict)['l3_policy']
        self.assertEqual(es_dict, l3p['external_segments'])

        # Share ES
        self.update_external_segment(
            es['external_segment']['id'], expected_res_status=200, shared=True)

        # Verify sharing/unsharing successful
        for shared in [True, False]:
            self.update_l3_policy(l3p['id'],
                                  expected_res_status=200, shared=shared)

        # Remove ES
        l3p = self.update_l3_policy(l3p['id'], expected_res_status=200,
                                    external_segments={})['l3_policy']
        self.assertEqual({}, l3p['external_segments'])
        # Verify ES update with sharing successful
        l3p = self.update_l3_policy(
            l3p['id'], expected_res_status=200, external_segments=es_dict,
            shared=True)['l3_policy']
        # Verify ES correctly set
        self.assertEqual(es_dict, l3p['external_segments'])

    def test_shared_l3_policy_update_negative(self):
        l3p = self.create_l3_policy(shared=True)['l3_policy']
        self.create_l2_policy(l3_policy_id=l3p['id'], shared=True)
        # Unshare not possible when reference by shared resource
        self.update_l3_policy(l3p['id'], expected_res_status=400, shared=False)

        l3p = self.create_l3_policy(shared=True)['l3_policy']
        self.create_l2_policy(l3_policy_id=l3p['id'], shared=False,
                              tenant_id='other')
        # Unshare not possible when referenced by other tenant's
        # private resource
        self.update_l3_policy(l3p['id'], expected_res_status=400, shared=False)

        es = self.create_external_segment(cidr='172.0.0.0/8')
        es_dict = self._get_es_dict(es, ['172.0.0.2', '172.0.0.3'])
        res = self.update_l3_policy(
            l3p['id'], expected_res_status=400,
            external_segments=es_dict, shared=True)
        self.assertEqual('SharedResourceReferenceError',
                         res['NeutronError']['type'])

    def test_create_with_es_negative(self):
        attrs = {'external_routes': [{'destination': '10.160.0.0/16',
                                     'nexthop': '172.1.1.1'}],
                 'cidr': '172.1.1.0/24'}
        es = self.create_external_segment(**attrs)['external_segment']
        # Overlapping pool
        attrs = {'ip_pool': '172.1.1.0/20',
                 'external_segments': {es['id']: ['172.1.1.2']}}
        res = self.create_l3_policy(expected_res_status=400, **attrs)
        self.assertEqual('ExternalSegmentSubnetOverlapsWithL3PIpPool',
                         res['NeutronError']['type'])
        # Overlapping route
        attrs['ip_pool'] = '10.160.1.0/24'
        res = self.create_l3_policy(expected_res_status=400, **attrs)
        self.assertEqual('ExternalRouteOverlapsWithL3PIpPool',
                         res['NeutronError']['type'])
        # Allocated address not in pool
        attrs = {'ip_pool': '192.168.0.0/24',
                 'external_segments': {es['id']: ['172.1.2.2']}}
        res = self.create_l3_policy(expected_res_status=400, **attrs)
        self.assertEqual('InvalidL3PExternalIPAddress',
                         res['NeutronError']['type'])

    def test_update_with_es_negative(self):
        attrs = {'external_routes': [{'destination': '10.160.0.0/16',
                                     'nexthop': '172.1.1.1'}],
                 'cidr': '172.1.1.0/24'}
        es = self.create_external_segment(**attrs)['external_segment']

        # Overlapping pool
        l3p = self.create_l3_policy(ip_pool='172.1.1.0/20')['l3_policy']
        attrs = {'external_segments': {es['id']: ['172.1.1.2']}}
        res = self.update_l3_policy(
            l3p['id'], expected_res_status=400, **attrs)
        self.assertEqual('ExternalSegmentSubnetOverlapsWithL3PIpPool',
                         res['NeutronError']['type'])

        # Overlapping route
        l3p = self.create_l3_policy(ip_pool='10.160.1.0/24')['l3_policy']
        res = self.update_l3_policy(
            l3p['id'], expected_res_status=400, **attrs)
        self.assertEqual('ExternalRouteOverlapsWithL3PIpPool',
                         res['NeutronError']['type'])

        # Allocated address not in pool
        l3p = self.create_l3_policy(ip_pool='192.168.0.0/24')['l3_policy']
        attrs = {'external_segments': {es['id']: ['172.1.2.2']}}
        res = self.update_l3_policy(
            l3p['id'], expected_res_status=400, **attrs)
        self.assertEqual('InvalidL3PExternalIPAddress',
                         res['NeutronError']['type'])


class TestL2Policy(GroupPolicyPluginTestCase):

    def test_shared_l2_policy_create(self):
        l3p = self.create_l3_policy(shared=True)['l3_policy']
        # Verify Default False
        l2p = self.create_l2_policy(l3_policy_id=l3p['id'])
        self.assertEqual(False, l2p['l2_policy']['shared'])
        # Verify shared True created without errors
        l2p = self.create_l2_policy(l3_policy_id=l3p['id'], shared=True)
        self.assertEqual(True, l2p['l2_policy']['shared'])

    def test_shared_l2_policy_update(self):
        l2p = self._create_l2_policy_on_shared()
        self.update_l2_policy(l2p['id'], expected_res_status=200, shared=True)

        self.create_policy_target_group(l2_policy_id=l2p['id'])
        self.update_l2_policy(l2p['id'], expected_res_status=200, shared=False)

        # Verify l2p can be moved across shared l3p
        l2p = self._create_l2_policy_on_shared(
            shared=True)
        l3p = self.create_l3_policy(
            shared=True)['l3_policy']
        self.update_l2_policy(l2p['id'], expected_res_status=200,
                              l3_policy_id=l3p['id'])

    def test_shared_l2_policy_create_negative(self):
        l3p = self.create_l3_policy()['l3_policy']
        self.create_l2_policy(l3_policy_id=l3p['id'], shared=True,
                              expected_res_status=400)

        # Verify shared L2p can't be moved to a non shared L3p
        l2p = self._create_l2_policy_on_shared(shared=True)
        l3p = self.create_l3_policy()['l3_policy']
        self.update_l2_policy(l2p['id'], expected_res_status=400,
                              l3_policy_id=l3p['id'])

    def test_shared_l2_policy_update_negative(self):
        l2p = self._create_l2_policy_on_shared(shared=True)
        self.create_policy_target_group(l2_policy_id=l2p['id'], shared=True)
        self.update_l2_policy(l2p['id'], expected_res_status=400, shared=False)

        l2p = self._create_l2_policy_on_shared(shared=True)
        self.create_policy_target_group(
            l2_policy_id=l2p['id'], shared=False, tenant_id='other')
        self.update_l2_policy(l2p['id'], expected_res_status=400, shared=False)

    def test_l2p_create_among_tenants(self):
        # L2P on shared L3P:
        self._create_l2_policy_on_shared(
            tenant_id='other', expected_res_status=201)


class TestPolicyRuleSet(GroupPolicyPluginTestCase):

    def test_shared_policy_rule_set_create(self):
        # Verify shared policy_rule_set created with shared rules
        prs = self._create_policy_rule_set_on_shared(
            shared=True, expected_res_status=201)
        self.assertEqual(True, prs['shared'])

        # Verify non shared policy_rule_set created with shared rules
        prs = self._create_policy_rule_set_on_shared(expected_res_status=201)
        self.assertEqual(False, prs['shared'])

    def test_shared_policy_rule_set_update(self):
        prs = self._create_policy_rule_set_on_shared()
        self.update_policy_rule_set(prs['id'],
                                    expected_res_status=200, shared=True)

        self.create_policy_target_group(
            provided_policy_rule_sets={prs['id']: None})
        self.update_policy_rule_set(
            prs['id'], expected_res_status=200, shared=False)

    def test_shared_policy_rule_set_create_negative(self):
        # Verify shared policy_rule_set fails with non shared rules
        prns = self._create_rule_on_shared()
        pr = self._create_rule_on_shared(shared=True)
        self.create_policy_rule_set(expected_res_status=400,
                                    shared=True,
                                    policy_rules=[pr['id'], prns['id']])

    def test_shared_policy_rule_set_update_negative(self):
        prs = self._create_policy_rule_set_on_shared(shared=True)
        self.create_policy_target_group(
            provided_policy_rule_sets={prs['id']: None}, shared=True)
        self.update_policy_rule_set(
            prs['id'], expected_res_status=400, shared=False)

        prs = self._create_policy_rule_set_on_shared(shared=True)
        self.create_policy_target_group(
            provided_policy_rule_sets={prs['id']: None},
            shared=False, tenant_id='other')
        self.update_policy_rule_set(
            prs['id'], expected_res_status=400, shared=False)
        # Verify non shared rules can't be set on non shared prs
        nsr = self._create_rule_on_shared()
        self.update_policy_rule_set(prs['id'], expected_res_status=400,
                                    policy_rules=[nsr['id']])

    def test_policy_rule_set_create_among_tenants(self):
        self._create_policy_rule_set_on_shared(tenant_id='other',
                                               expected_res_status=201)


class TestPolicyRule(GroupPolicyPluginTestCase):

    def test_shared_rule_create(self):
        # Verify shared rule created with shared actions and classifier
        pr = self._create_rule_on_shared(shared=True,
                                         expected_res_status=201)
        self.assertEqual(True, pr['shared'])

        # Verify non shared rule create with shared actions and classifier
        pr = self._create_rule_on_shared(expected_res_status=201)
        self.assertEqual(False, pr['shared'])

    def test_shared_rule_update(self):
        pr = self._create_rule_on_shared()
        self.update_policy_rule(pr['id'], expected_res_status=200, shared=True)

        self.create_policy_rule_set(policy_rules=[pr['id']])
        self.update_policy_rule(
            pr['id'], expected_res_status=200, shared=False)

    def test_shared_rule_create_negative(self):
        # Verify shared rule fails with non shared classifier
        pans = self.create_policy_action(action_type='allow')['policy_action']
        cl_attr = {'protocol': 'tcp', 'port_range': 80}
        pcns = self.create_policy_classifier(
            direction='in', **cl_attr)['policy_classifier']
        pc = self.create_policy_classifier(
            direction='in', shared=True,
            **cl_attr)['policy_classifier']
        self.create_policy_rule(
            policy_classifier_id=pcns['id'], expected_res_status=400,
            shared=True)

        # Verify shared rule fails with non shared action
        self.create_policy_rule(
            policy_classifier_id=pc['id'], policy_actions=[pans['id']],
            expected_res_status=400, shared=True)

    def test_shared_rule_update_negative(self):
        pr = self._create_rule_on_shared(shared=True)
        self.create_policy_rule_set(policy_rules=[pr['id']], shared=True,
                                    tenant_id='another')
        self.update_policy_rule(pr['id'],
                                expected_res_status=400, shared=False)

        pr = self._create_rule_on_shared(shared=True)
        self.create_policy_rule_set(policy_rules=[pr['id']], shared=False,
                                    tenant_id='other')
        self.update_policy_rule(pr['id'],
                                expected_res_status=400, shared=False)

    def test_rule_create_among_tenants(self):
        self._create_rule_on_shared(tenant_id='other',
                                    expected_res_status=201)


class TestPolicyClassifier(GroupPolicyPluginTestCase):
    def test_shared_policy_classifier_update(self):
        cl_attr = {'protocol': 'tcp', 'port_range': 80}
        pc = self.create_policy_classifier(**cl_attr)['policy_classifier']
        pa = self.create_policy_action(action_type='allow')['policy_action']
        self.update_policy_classifier(
            pc['id'], expected_res_status=200, shared=True)

        self.create_policy_rule(policy_classifier_id=pc['id'],
                                policy_actions=[pa['id']])
        self.update_policy_classifier(pc['id'],
                                      expected_res_status=200, shared=False)

    def test_shared_policy_classifier_update_negative(self):
        cl_attr = {'protocol': 'tcp', 'port_range': 80}
        pc = self.create_policy_classifier(shared=True,
                                           **cl_attr)['policy_classifier']
        pa = self.create_policy_action(
            action_type='allow', shared=True)['policy_action']
        self.create_policy_rule(
            policy_classifier_id=pc['id'], policy_actions=[pa['id']],
            shared=True)
        self.update_policy_classifier(pc['id'],
                                      expected_res_status=400, shared=False)

        self.create_policy_rule(policy_classifier_id=pc['id'],
                                policy_actions=[pa['id']], shared=False,
                                tenant_id='other')
        self.update_policy_classifier(pc['id'],
                                      expected_res_status=400, shared=False)


class TestPolicyTargetGroup(GroupPolicyPluginTestCase):

    def test_delete_ptg_with_unused_pt(self):
        ctx = context.get_admin_context()
        ptg = self.create_policy_target_group()['policy_target_group']
        self.create_policy_target(policy_target_group_id=ptg['id'])
        req = self.new_delete_request('policy_target_groups', ptg['id'],
                                      self.fmt)
        res = req.get_response(self.ext_api)
        self.assertEqual(res.status_int, webob.exc.HTTPNoContent.code)
        self.assertRaises(gpolicy.PolicyTargetGroupNotFound,
                          self.plugin.get_policy_target_group, ctx, ptg['id'])

    def test_delete_fails_on_used_ptg(self):
        with self.port() as port:
            port_id = port['port']['id']
            ptg = self.create_policy_target_group()['policy_target_group']
            self.create_policy_target(policy_target_group_id=ptg['id'],
                                      port_id=port_id)
            req = self.new_delete_request('policy_target_groups', ptg['id'],
                                          self.fmt)
            res = req.get_response(self.ext_api)
            self.assertEqual(res.status_int, 400)

    def test_shared_ptg_create(self):
        l2p = self._create_l2_policy_on_shared(
            shared=True)
        l2pns = self._create_l2_policy_on_shared()

        prs = self._create_policy_rule_set_on_shared(
            shared=True)
        ctns = self._create_policy_rule_set_on_shared()

        nsp = self.create_network_service_policy(
            shared=True)['network_service_policy']
        nspns = self.create_network_service_policy()['network_service_policy']
        # Verify non-shared ptg providing and consuming shared and non shared
        # policy_rule_sets
        ptg = self.create_policy_target_group(
            l2_policy_id=l2p['id'], expected_res_status=201)
        self.assertEqual(False, ptg['policy_target_group']['shared'])
        ptg = self.create_policy_target_group(
            l2_policy_id=l2p['id'],
            provided_policy_rule_sets={prs['id']: '', ctns['id']: ''},
            consumed_policy_rule_sets={prs['id']: '', ctns['id']: ''},
            expected_res_status=201)
        self.assertEqual(False, ptg['policy_target_group']['shared'])
        ptg = self.create_policy_target_group(
            l2_policy_id=l2p['id'], network_service_policy_id=nsp['id'],
            expected_res_status=201)
        self.assertEqual(False, ptg['policy_target_group']['shared'])
        ptg = self.create_policy_target_group(
            l2_policy_id=l2p['id'], network_service_policy_id=nspns['id'],
            expected_res_status=201)
        self.assertEqual(False, ptg['policy_target_group']['shared'])

        # Verify shared True created without errors by providing/consuming
        # shared policy_rule_sets
        ptg = self.create_policy_target_group(
            l2_policy_id=l2p['id'], shared=True,
            expected_res_status=201)
        self.assertEqual(True, ptg['policy_target_group']['shared'])
        ptg = self.create_policy_target_group(
            l2_policy_id=l2p['id'], provided_policy_rule_sets={prs['id']: ''},
            consumed_policy_rule_sets={prs['id']: ''}, shared=True,
            expected_res_status=201)
        self.assertEqual(True, ptg['policy_target_group']['shared'])

        # Verify not shared created without error on not shared l2p
        self.create_policy_target_group(l2_policy_id=l2pns['id'],
                                   expected_res_status=201)

    def test_shared_ptg_update(self):
        ptg = self._create_ptg_on_shared()['policy_target_group']
        self.update_policy_target_group(
            ptg['id'], expected_res_status=200, shared=True)

        self.create_policy_target(policy_target_group_id=ptg['id'])
        self.update_policy_target_group(
            ptg['id'], expected_res_status=200, shared=False)

    def test_shared_ptg_create_negative(self):
        l2pns = self._create_l2_policy_on_shared()
        ctns = self._create_policy_rule_set_on_shared()
        # Verify shared PTG fails on non-shared l2p
        self.create_policy_target_group(
            l2_policy_id=l2pns['id'], shared=True,
            expected_res_status=400)
        # Verify shared PTG fails to provide/consume non shared
        # policy_rule_sets
        self._create_ptg_on_shared(
            shared=True,
            provided_policy_rule_sets={ctns['id']: ''},
            consumed_policy_rule_sets={ctns['id']: ''},
            expected_res_status=400)

    def test_shared_ptg_update_negative(self):
        ptg = self._create_ptg_on_shared(
            shared=True)['policy_target_group']
        self.create_policy_target(policy_target_group_id=ptg['id'],
                                  tenant_id='other')
        self.update_policy_target_group(
            ptg['id'], expected_res_status=400, shared=False)

        # Verify update to non shared L2p fails
        l2p = self.create_l2_policy()['l2_policy']
        self.update_policy_target_group(
            ptg['id'], expected_res_status=400,
            l2_policy_id=l2p['id'])

        # Verify update to non shared NSP fails
        nsp = self.create_network_service_policy()['network_service_policy']
        self.update_policy_target_group(
            ptg['id'], expected_res_status=400,
            network_service_policy_id=nsp['id'])

        # Verify update to non shared provided PRS fails
        pts = self._create_policy_rule_set_on_shared()
        self.update_policy_target_group(
            ptg['id'], expected_res_status=400,
            provided_policy_rule_sets={pts['id']: ''})
        # Verify update to non shared consumed PRS fails
        self.update_policy_target_group(
            ptg['id'], expected_res_status=400,
            consumed_policy_rule_sets={pts['id']: ''})

    def test_complex_ptg_create_among_tenant(self):
        ctp = self._create_policy_rule_set_on_shared(
            shared=True)
        ctc = self._create_policy_rule_set_on_shared(
            shared=True)
        nsp = self.create_network_service_policy(
            shared=True)['network_service_policy']
        self._create_ptg_on_shared(
            tenant_id='other', provided_policy_rule_sets={ctp['id']: ''},
            consumed_policy_rule_sets={ctc['id']: ''},
            network_service_policy_id=nsp['id'], expected_res_status=201)

    def test_ptg_create_among_tenants(self):
        self._create_ptg_on_shared(tenant_id='other',
                                   expected_res_status=201)


class TestExternalSegment(GroupPolicyPluginTestCase):

    def test_shared_es_create(self):
        # Verify default is False
        es = self.create_external_segment()
        self.assertEqual(False, es['external_segment']['shared'])
        # Verify shared True created without errors
        es = self.create_external_segment(shared=True)
        self.assertEqual(True, es['external_segment']['shared'])

    def test_shared_es_update(self):
        es = self.create_external_segment()['external_segment']
        for shared in [True, False]:
            self.update_external_segment(
                es['id'], expected_res_status=200,
                shared=shared)

    def test_create_routes(self):
        attrs = {'external_routes': [{'destination': '0.0.0.0/0',
                                     'nexthop': '172.1.0.1'}],
                 'cidr': '172.1.0.0/24'}
        self.create_external_segment(expected_res_status=201, **attrs)

    def test_routes_negative(self):
        # Verify wrong NH
        attrs = {'external_routes': [{'destination': '0.0.0.0/0',
                                     'nexthop': '172.1.1.1'}],
                 'cidr': '172.1.0.0/24'}
        res = self.create_external_segment(expected_res_status=400, **attrs)
        self.assertEqual('ExternalRouteNextHopNotInExternalSegment',
                         res['NeutronError']['type'])
        attrs['cidr'] = '172.1.1.0/24'
        es = self.create_external_segment(**attrs)['external_segment']
        self.create_l3_policy(
            ip_pool='192.160.0.0/16',
            external_segments={es['id']: ['172.1.1.2']})['l3_policy']

        # Verify refused because overlapping with L3P
        attrs = {'external_routes': [{'destination': '192.168.2.0/0',
                                     'nexthop': '172.1.1.1'}]}
        res = self.update_external_segment(
            es['id'], expected_res_status=400, **attrs)
        self.assertEqual('ExternalRouteOverlapsWithL3PIpPool',
                         res['NeutronError']['type'])


class TestExternalPolicy(GroupPolicyPluginTestCase):

    def test_shared_ep_create(self):
        es = self.create_external_segment(
            shared=True)['external_segment']
        esns = self.create_external_segment(
        )['external_segment']

        prs = self._create_policy_rule_set_on_shared(shared=True)
        prsns = self._create_policy_rule_set_on_shared()

        # Verify non-shared ep providing and consuming shared and non shared
        # policy_rule_sets
        ep = self.create_external_policy(
            external_segments=[es['id']], expected_res_status=201)
        self.assertEqual(False, ep['external_policy']['shared'])
        ep = self.create_external_policy(
            external_segments=[es['id']],
            provided_policy_rule_sets={prs['id']: '', prsns['id']: ''},
            consumed_policy_rule_sets={prs['id']: '', prsns['id']: ''},
            expected_res_status=201)
        self.assertEqual(False, ep['external_policy']['shared'])

        # Verify shared True created without errors by providing/consuming
        # shared policy_rule_sets
        ep = self.create_external_policy(
            external_segments=[es['id']], shared=True,
            expected_res_status=201)
        self.assertEqual(True, ep['external_policy']['shared'])
        ep = self.create_external_policy(
            external_segments=[es['id']],
            provided_policy_rule_sets={prs['id']: ''},
            consumed_policy_rule_sets={prs['id']: ''}, shared=True,
            expected_res_status=201)
        self.assertEqual(True, ep['external_policy']['shared'])

        # Verify not shared created without error on not shared es
        self.create_external_policy(
            external_segments=[esns['id']], expected_res_status=201)

    def test_shared_ep_update(self):
        ep = self._create_external_policy_on_shared()
        self.update_external_policy(
            ep['id'], expected_res_status=200, shared=True)
        self.update_external_policy(
            ep['id'], expected_res_status=200, shared=False)

    def test_shared_ep_create_negative(self):
        es = self.create_external_segment()['external_segment']
        prs = self._create_policy_rule_set_on_shared()
        # Verify shared EP fails on non-shared es
        res = self.create_external_policy(
            external_segments=[es['id']], shared=True,
            expected_res_status=400)
        self.assertEqual('SharedResourceReferenceError',
                         res['NeutronError']['type'])
        # Verify shared EP fails to provide/consume non shared
        # policy_rule_sets
        res = self.create_external_policy(
            shared=True,
            provided_policy_rule_sets={prs['id']: ''},
            consumed_policy_rule_sets={prs['id']: ''},
            expected_res_status=400)
        self.assertEqual('SharedResourceReferenceError',
                         res['NeutronError']['type'])

    def test_shared_ep_update_negative(self):
        ep = self._create_external_policy_on_shared(shared=True)
        # Verify update to non shared ES fails
        es = self.create_external_segment()['external_segment']
        self.update_external_policy(
            ep['id'], expected_res_status=400, external_segments=[es['id']])

        # Verify update to non shared provided PRS fails
        prs = self._create_policy_rule_set_on_shared()
        self.update_external_policy(
            ep['id'], expected_res_status=400,
            provided_policy_rule_sets={prs['id']: ''})
        # Verify update to non shared consumed PRS fails
        self.update_external_policy(
            ep['id'], expected_res_status=400,
            consumed_policy_rule_sets={prs['id']: ''})


class TestNatPool(GroupPolicyPluginTestCase):

    def test_nat_pool_shared_create(self):
        def combination(np, es):
            return {'np': np, 'es': es}
        allowed = [combination(False, False), combination(True, True),
                   combination(False, True)]
        for shared in allowed:
            es = self.create_external_segment(
                shared=shared['es'])['external_segment']
            self.create_nat_pool(
                external_segment_id=es['id'], shared=shared['np'],
                expected_res_status=201)

    def test_nat_pool_shared_create_negative(self):
        es = self.create_external_segment(
            shared=False)['external_segment']
        res = self.create_nat_pool(
            external_segment_id=es['id'], shared=True,
            expected_res_status=400)
        self.assertEqual('SharedResourceReferenceError',
                         res['NeutronError']['type'])

    def test_nat_pool_shared_update(self):
        np = self.create_nat_pool(shared=False)['nat_pool']
        for shared in [False, True]:
            es = self.create_external_segment(
                shared=shared)['external_segment']
            self.update_nat_pool(
                np['id'], expected_res_status=200,
                external_segment_id=es['id'])
        np = self.create_nat_pool(shared=True)['nat_pool']
        es = self.create_external_segment(
            shared=True)['external_segment']
        # Verify shared NP on shared ES
        self.update_nat_pool(
            np['id'], expected_res_status=200,
            external_segment_id=es['id'])
        # Verify unshare NP
        self.update_nat_pool(
            np['id'], expected_res_status=200, shared=False)


class TestPolicyTarget(GroupPolicyPluginTestCase):

    def _test_cross_tenant_fails(self, is_admin=False):
        status = {False: 404, True: 400}
        ptg = self.create_policy_target_group(
            expected_res_status=201, tenant_id='tenant',
            is_admin_context=is_admin)['policy_target_group']
        # Create EP on a different tenant
        res = self.create_policy_target(
            expected_res_status=status[is_admin], tenant_id='another',
            is_admin_context=is_admin, policy_target_group_id=ptg['id'])
        if not is_admin:
            self.assertEqual(
                'GbpResourceNotFound', res['NeutronError']['type'])
        else:
            self.assertEqual(
                'InvalidCrossTenantReference', res['NeutronError']['type'])

        # Create EP without PTG
        pt = self.create_policy_target(
            expected_res_status=201, tenant_id='another',
            is_admin_context=is_admin)['policy_target']

        # Update PT fails
        res = self.update_policy_target(pt['id'],
                                        expected_res_status=status[is_admin],
                                        tenant_id='another',
                                        policy_target_group_id=ptg['id'],
                                        is_admin_context=is_admin)
        if not is_admin:
            self.assertEqual(
                'GbpResourceNotFound', res['NeutronError']['type'])
        else:
            self.assertEqual(
                'InvalidCrossTenantReference', res['NeutronError']['type'])

    def test_cross_tenant_fails(self):
        self._test_cross_tenant_fails()

    def test_cross_tenant_fails_admin(self):
        self._test_cross_tenant_fails(True)


class TestGroupPolicyPluginGroupResources(
        GroupPolicyPluginTestCase, tgpdb.TestGroupResources):

    pass


class TestGroupPolicyPluginMappedGroupResourceAttrs(
        GroupPolicyPluginTestCase, tgpmdb.TestMappedGroupResourceAttrs):
    pass
