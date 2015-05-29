from unittest.case import TestCase

from trendy.connection import Connection, MissingContextError, _clients
from mock import MagicMock, patch


class ConnectionClientTestCases(TestCase):
    def test_client_is_created_only_if_required(self):
        with patch('trendy.connection.Client') as mock_client:
            t = Connection('wsdl', 'user', 'pass')

            self.assertIsNone(t._client)
            self.assertIsNotNone(t.client)
            self.assertIsNotNone(t._client)

    def test_client_is_cloned_from_cache(self):
        c = MagicMock()
        c.clone.return_value = []
        _clients['wsdl'] = c

        t = Connection('wsdl', 'user', 'pass')

        self.assertEqual(t.client, [])
        c.clone.assert_called_once

class ConnectionTestCases(TestCase):
    def setUp(self):
        # this will bypass setting up the wsdl etc
        Connection.client = MagicMock()

        def auth(s):
            s.sid = 'test'
        Connection._authenticate = auth

    def test_connection_will_raise_error_when_used_improperly(self):
        with self.assertRaises(MissingContextError):
            t = Connection('wsdl', 'user', 'pass')
            t.securityProfileRetrieveAll()

        try:
            with Connection('wsdl', 'user', 'pass') as t:
                t.securityProfileRetrieve(1)
        except MissingContextError:
            self.fail('MissingContextError raised unexpectedly')

    def test_provides_all_services_as_snake_case_attr(self):
        with Connection('wsdl', 'user', 'pass') as t:
            self.assertTrue(hasattr(t, 'security_profiles'))
            self.assertTrue(hasattr(t, 'ip_lists'))
            self.assertTrue(hasattr(t, 'firewall_rules'))

    def test_only_uses_suds_for_known_methods(self):
        with self.assertRaises(MissingContextError):
            t = Connection('wsdl', 'user', 'pass')
            t.securityProfileRetrieveAll()

        # there is no session here so it would throw a MissingContextError
        # if it was going through the __getattr__ wrapper
        with self.assertRaises(TypeError):
            t = Connection('wsdl', 'user', 'pass')
            t.unknownMethod()




