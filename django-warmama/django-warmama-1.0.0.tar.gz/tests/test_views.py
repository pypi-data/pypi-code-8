import json
import mock
import time
import zlib
from base64 import urlsafe_b64encode
from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import Client, override_settings
from django.utils import timezone
from tests import TestCase, loadJson
from warmama import models


##########
# Base classes for test cases
##########


class SampleData(object):
    """Mixin to setup sample data for test cases"""

    def setUp(self):
        """Set up data and test client for tests"""
        super(SampleData, self).setUp()
        User = get_user_model()
        self.user = User.objects.create_user('user', 'user@email.com', 'pass')

        self.server = models.Server.objects.create(
            login='server',
            ipv6='1:2:3:4:5:6:7:8',
        )
        self.ssession = models.ServerSession.objects.create(
            user=self.server,
            ipv6=self.server.ipv6,
            port=44400,
        )
        self.player = models.Player.objects.create(
            login='user',
            ip='132.233.139.177',
        )
        self.csession = models.PlayerSession.objects.create(
            user=self.player,
            ip=self.player.ip,
            ticket_id=1,
            ticket_server=self.ssession,
            ticket_expiration=timezone.now() + timedelta(days=1),
        )
        self.gametypes = [
            models.Gametype.objects.create(
                name='gt_{0}'.format(name),
                description='Gametype {0}'.format(name),
            ) for name in ('gt_b', 'gt_a')
        ]
        self.pstats = [
            models.PlayerStat.objects.create(
                player_id=self.player.pk,
                gametype_id=self.gametypes[0].pk,
                rating=4,
            ),
            models.PlayerStat.objects.create(
                player_id=self.player.pk,
                gametype_id=self.gametypes[1].pk,
                rating=5,
            )
        ]


class ServerTestCase(SampleData, TestCase):
    def setUp(self):
        """Attach a test client with server ip"""
        super(ServerTestCase, self).setUp()
        self.c = Client(REMOTE_ADDR='1:2:3:4:5:6:7:8')


class ClientTestCase(SampleData, TestCase):
    def setUp(self):
        """Attach a test client with client ip"""
        super(ClientTestCase, self).setUp()
        self.c = Client(REMOTE_ADDR='132.233.139.177')


##########
# Test Cases
##########


class ServerLoginTest(ServerTestCase):
    def test_unregistered_server(self):
        """It should return 403 on unknown ip addresses"""
        c = Client(REMOTE_ADDR='253.168.132.100')
        response = c.post('/slogin', {'authkey': 'login', 'port': 44400})

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'id': 0})

    def test_invalid_authkey(self):
        """It should return 403 on unknown ip addresses"""
        response = self.c.post('/slogin', {'authkey': 'invalid', 'port': 44400})

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'id': 0})

    def test_banned_server(self):
        """It should return 403 on banned servers"""
        self.server.banned = True
        self.server.save()

        response = self.c.post('/slogin', {'authkey': 'login', 'port': 44400})
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'id': 0})

    def test_update_server(self):
        """It should update server hostname and demos_baseurl"""
        response = self.c.post('/slogin', {
            'authkey': 'server',
            'port': 44400,
            'hostname': 'hostname',
            'demos_baseurl': 'baseurl',
        })
        server = models.Server.objects.get(pk=self.server.pk)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(server.hostname, 'hostname')
        self.assertEqual(server.demos_baseurl, 'baseurl')

    def test_create_session(self):
        """It should create a session if there is none"""
        self.ssession.delete()
        response = self.c.post('/slogin', {'authkey': 'server', 'port': 44400})
        session = models.ServerSession.objects.get(user_id=self.server.pk)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'id': session.pk})

    def test_existing_session(self):
        """It should return an existing session if possible"""
        response = self.c.post('/slogin', {'authkey': 'server', 'port': 44400})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'id': self.ssession.pk})

    def test_update_session(self):
        """It should update an existing session's port"""
        response = self.c.post('/slogin', {
            'authkey': 'server',
            'port': '1234'
        })
        session = models.ServerSession.objects.get(pk=self.ssession.pk)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'id': session.pk})
        self.assertEqual(session.port, 1234)

    def test_invalid_port(self):
        """It should 400 on an invalid session port"""
        response = self.c.post('/slogin', {
            'authkey': 'login',
            'port': 'abcd'
        })

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'id': 0})


class ServerLogoutTest(ServerTestCase):
    def test_invalid_ipaddr(self):
        """It should 403 on an invalid ip address"""
        c = Client(REMOTE_ADDR='132.233.139.177')
        response = c.post('/slogout', {'ssession': self.ssession.pk})

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'status': 0})

    def test_invalid_session(self):
        """It should 403 on an invalid session"""
        response = self.c.post('/slogout', {'ssession': 1234})

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'status': 0})

    def test_logout(self):
        """It should delete an existing session"""
        response = self.c.post('/slogout', {'ssession': self.ssession.pk})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 1})
        with self.assertRaises(models.ServerSession.DoesNotExist):
            models.ServerSession.objects.get(pk=self.ssession.pk)


class ServerClientConnectTest(ServerTestCase):
    def test_expired_ticket(self):
        """It should 403 on expired tickets"""
        self.csession.ticket_expiration = timezone.now() - timedelta(days=1)
        self.csession.save()
        response = self.c.post('/scc', {
            'ssession': self.ssession.pk,
            'csession': self.csession.pk,
            'cticket': self.csession.ticket_id,
            'cip': self.csession.ip + ':1234'
        })

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'id': 0})

    def test_reset_ticket(self):
        """It should reset the player's ticket"""
        response = self.c.post('/scc', {
            'ssession': self.ssession.pk,
            'csession': self.csession.pk,
            'cticket': self.csession.ticket_id,
            'cip': self.csession.ip + ':1234'
        })
        csession = models.PlayerSession.objects.get(pk=self.csession.pk)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(csession.ticket_id)
        self.assertIsNone(csession.ticket_server)
        self.assertIsNone(csession.ticket_expiration)

    def test_empty_ratings(self):
        """It should handle empty player ratings"""
        models.PlayerStat.objects.all().delete()
        response = self.c.post('/scc', {
            'ssession': self.ssession.pk,
            'csession': self.csession.pk,
            'cticket': self.csession.ticket_id,
            'cip': self.csession.ip + ':1234'
        })

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'id': self.csession.pk,
            'login': self.player.login,
            'ratings': [],
        })

    def test_ratings(self):
        """It should handle player ratings"""
        response = self.c.post('/scc', {
            'ssession': self.ssession.pk,
            'csession': self.csession.pk,
            'cticket': self.csession.ticket_id,
            'cip': self.csession.ip + ':1234'
        })
        resdata = loadJson(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(resdata['id'], self.csession.pk)
        self.assertEqual(resdata['login'], self.player.login)
        self.assertEqual(
            resdata['ratings'],
            [{  # Should be ordered by gametype name
                'gametype': self.gametypes[1].name,
                'rating': 5.0,
                'deviation': 0,
            }, {
                'gametype': self.gametypes[0].name,
                'rating': 4.0,
                'deviation': 0,
            }]
        )


class ServerClientDisconnectTest(ServerTestCase):
    def setUp(self):
        """Connect client session to server session"""
        super(ServerClientDisconnectTest, self).setUp()
        self.csession.ticket_id = None
        self.csession.ticket_server = None
        self.csession.ticket_expiration = None
        self.csession.server_session = self.ssession
        self.csession.save()

    def test_client_session_permission(self):
        """It should 403 if client session does not belong to server session"""
        self.csession.server_session = None
        self.csession.save()
        response = self.c.post('/scd', {
            'ssession': self.ssession.pk,
            'csession': self.csession.pk,
        })

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'status': 0})

    def test_client_disconnect(self):
        """It should clear ticket and session and not add a PlayerPurge"""
        response = self.c.post('/scd', {
            'ssession': self.ssession.pk,
            'csession': self.csession.pk,
        })
        csession = models.PlayerSession.objects.get(pk=self.csession.pk)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 1})
        self.assertIsNone(csession.ticket_id)
        self.assertIsNone(csession.server_session)

    def test_nopurge(self):
        """It does not purge if `gameon` is 0 or not passed"""
        self.c.post('/scd', {
            'ssession': self.ssession.pk,
            'csession': self.csession.pk,
            'gameon': '0',
        })

        with self.assertRaises(models.PurgePlayer.DoesNotExist):
            models.PurgePlayer.objects.get(session=self.csession)

    def test_purge(self):
        """It add a PurgePlayer if `gameon` is passed"""
        self.c.post('/scd', {
            'ssession': self.ssession.pk,
            'csession': self.csession.pk,
            'gameon': 1,
        })
        purge = models.PurgePlayer.objects.get(
            session_id=self.csession.pk,
            server_session=self.ssession.pk,
        )

        self.assertIsNotNone(purge)


class ServerHeartbeat(ServerTestCase):
    def test_heartbeat(self):
        """It should update the `updated` timestamp"""
        # Force set `updated` to a time in the past and make sure it worked
        models.ServerSession.objects.update(updated=timezone.now() - timedelta(days=1))
        ssession = models.ServerSession.objects.get(pk=self.ssession.pk)
        self.assertTrue(timezone.now() - ssession.updated > timedelta(minutes=1))

        response = self.c.post('/shb', {'ssession': self.ssession.pk})
        ssession = models.ServerSession.objects.get(pk=self.ssession.pk)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 1})
        self.assertTrue(timezone.now() - ssession.updated < timedelta(minutes=1))


class ServerMatchReportTest(ServerTestCase):
    def test_matchreport(self):
        data = {
            'match': {
                'gametype': 'ca',
                'teamgame': False,
                'racegame': False,
                'map': 'wca1',
                'hostname': 'host',
                'timeplayed': 100,
                'timestamp': 0,
                'gamedir': 'basewsw',
            },
            'players': [{
                'final': 1,
                'frags': 0,
                'deaths': 2,
                'sessionid': self.csession.pk,
            }],
        }
        packed = json.dumps(data).encode('utf-8')
        packed = zlib.compress(packed)
        packed = urlsafe_b64encode(packed).decode('ascii')
        expected = {
            'status': 1,
            'ratings': {
                'gametype': 'ca',
                'ratings': [[self.csession.pk, 0]],
            }
        }

        response = self.c.post('/smr', {'ssession': self.ssession.pk, 'data': packed})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, expected)


class ServerMatchUUIDTest(ServerTestCase):
    def test_matchuuid(self):
        response = self.c.post('/smuuid', {'ssession': self.ssession.pk})
        content = json.loads(response.content.decode('utf-8'))
        ssession = models.ServerSession.objects.get(pk=self.ssession.pk)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(content['uuid'])
        self.assertEqual(ssession.next_match_uuid, content['uuid'])


class ClientLoginTest(ClientTestCase):
    @override_settings(WARMAMA_REMOTE_CLIENTAUTH=False)
    @mock.patch('requests.post')
    def test_step_one_local(self, requests_post):
        """It should mark the login_player as valid"""
        response = self.c.post('/clogin', {'login': 'user', 'passwd': 'pass'})
        login_player = models.LoginPlayer.objects.get(login='user')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'ready': -1,
            'handle': login_player.pk,
            'id': 0,
        })
        self.assertTrue(login_player.ready)
        self.assertTrue(login_player.valid)
        self.assertFalse(requests_post.called)

    @override_settings(WARMAMA_REMOTE_CLIENTAUTH=False)
    def test_step_one_invalid_user(self):
        """It should mark the login_player as invalid"""
        response = self.c.post('/clogin', {'login': 'user', 'passwd': 'wrong'})
        login_player = models.LoginPlayer.objects.get(login='user')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'ready': -1,
            'handle': login_player.pk,
            'id': 0,
        })
        self.assertTrue(login_player.ready)
        self.assertFalse(login_player.valid)

    @override_settings(WARMAMA_REMOTE_CLIENTAUTH=True)
    @override_settings(WARMAMA_AUTH_URL='http://www.wmmauth.com/getauth')
    @mock.patch('requests.post')
    def test_step_one_remote(self, requests_post):
        """It should send the post request with the proper arguments"""
        response = self.c.post('/clogin', {'login': 'user', 'passwd': 'pass'})
        time.sleep(0.1)  # Give the `remote_login` thread some time
        login_player = models.LoginPlayer.objects.get(login='user')

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            'ready': -1,
            'handle': login_player.pk,
            'id': 0,
        })

        # Check the `remote_login` thread made the right post request
        self.assertEqual(requests_post.call_count, 1)
        requests_post.assert_called_with(
            'http://www.wmmauth.com/getauth',
            timeout=5,
            data={
                'login': 'user',
                'passwd': 'pass',
                'handle': '%d' % login_player.pk,
                'digest': 'something',
                'url': 'http://testserver/auth',
            }
        )

    def test_step_two_not_ready(self):
        login_player = models.LoginPlayer.objects.create(
            login='user', ready=False, valid=False
        )
        response = self.c.post('/clogin', {'handle': login_player.pk})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'ready': 1, 'id': 0})

    def test_step_two_invalid(self):
        login_player = models.LoginPlayer.objects.create(
            login='user', ready=True, valid=False
        )
        response = self.c.post('/clogin', {'handle': login_player.pk})

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'ready': 2, 'id': 0})
        with self.assertRaises(models.LoginPlayer.DoesNotExist):
            models.LoginPlayer.objects.get(pk=login_player.pk)

    def test_step_two_valid(self):
        login_player = models.LoginPlayer.objects.create(
            login='user', ready=True, valid=True
        )
        response = self.c.post('/clogin', {'handle': login_player.pk})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "ready": 2,
            "ratings": [
                {"deviation": 0.0, "rating": 5.0, "gametype": "gt_gt_a"},
                {"deviation": 0.0, "rating": 4.0, "gametype": "gt_gt_b"}
            ],
            "id": 1,
            "profile_url_rml": "",
            "profile_url": ""
        })


class ClientLogoutTest(ClientTestCase):
    def test_mark_purgable(self):
        """It should mark finished sessions as purgable"""
        models.PurgePlayer.objects.create(player=self.player, session=self.csession)
        response = self.c.post('/clogout', {'csession': self.csession.pk})
        csession = models.PlayerSession.objects.get(pk=self.csession.pk)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 1})
        self.assertTrue(csession.purgable)

    def test_delete(self):
        """It should delete sessions not marked as purgable"""
        response = self.c.post('/clogout', {'csession': self.csession.pk})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 1})
        with self.assertRaises(models.PlayerSession.DoesNotExist):
            models.PlayerSession.objects.get(pk=self.csession.pk)


class ClientConnectTest(ClientTestCase):
    def test_connect(self):
        response = self.c.post('/ccc', {
            'csession': self.csession.pk,
            'saddr': '%s:%d' % (self.ssession.ipv6, self.ssession.port)
        })
        csession = models.PlayerSession.objects.get(pk=self.csession.pk)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'ticket': csession.ticket_id})
        self.assertTrue(csession.ticket_id)


class ClientHeartbeatTest(ClientTestCase):
    def test_heartbeat(self):
        """It should update the `updated` timestamp"""
        # Force set `updated` to a time in the past and make sure it worked
        models.PlayerSession.objects.update(updated=timezone.now() - timedelta(days=1))
        csession = models.PlayerSession.objects.get(pk=self.csession.pk)
        self.assertTrue(timezone.now() - csession.updated > timedelta(minutes=1))

        response = self.c.post('/chb', {'csession': self.csession.pk})
        csession = models.PlayerSession.objects.get(pk=self.csession.pk)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 1})
        self.assertTrue(timezone.now() - csession.updated < timedelta(minutes=1))


class ClientAuthenticateTest(ClientTestCase):
    def test_authenticate(self):
        login_player = models.LoginPlayer.objects.create(
            login='user', ready=False, valid=False
        )
        response = self.c.post('/auth', {
            'handle': login_player.pk,
            'digest': 'something',
            'valid': '1',
            'profile_url': 'url',
            'profile_url_rml': 'url_rml',
        })
        login_player = models.LoginPlayer.objects.get(pk=login_player.pk)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 1})
