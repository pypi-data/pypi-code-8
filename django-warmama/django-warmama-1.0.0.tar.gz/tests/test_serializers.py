from datetime import datetime
from django.utils import timezone
from tests import TestCase
from warmama import models, serializers


class Data(object):
    """Class for creating serializable objects, it maps kwargs to attributes"""
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class MatchTeamSerializerTest(TestCase):
    def test_serialize(self):
        data = {'name': 'team', 'score': 10, 'index': 1}
        serializer = serializers.MatchTeamSerializer(Data(**data))

        self.assertEqual(serializer.data, data)

    def test_deserialize(self):
        data = {'name': 'team', 'score': 10, 'index': 1}
        serializer = serializers.MatchTeamSerializer(data=data)
        expected = {'name': 'team', 'score': 10, 'index': 1}

        serializer.is_valid()
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.validated_data, expected)


class MatchWeaponSerializerTest(TestCase):
    def test_serialize(self):
        data = Data(
            weapon='pg',
            acc_strong=2.3,
            dmg_strong=1,
            acc_weak=5.6,
            dmg_weak=7,
        )
        serializer = serializers.MatchWeaponSerializer(data)
        expected = {
            'weapon': 'pg',
            'acc_strong': 2.3,
            'dmg_strong': 1,
            'acc_weak': 5.6,
            'dmg_weak': 7,
        }

        self.assertEqual(serializer.data, expected)

    def test_deserialize(self):
        data = {
            'weapon': 'pg',
            'acc_strong': 2.3,
            'dmg_strong': 1,
            'acc_weak': 5.6,
            'dmg_weak': 7,
        }
        serializer = serializers.MatchWeaponSerializer(data=data)
        expected = data

        serializer.is_valid()
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.validated_data, expected)


class MatchWeaponSetSerializerTest(TestCase):
    def setUp(self):
        self.weapon_data = {
            'acc_strong': 2.3,
            'dmg_strong': 1,
            'acc_weak': 5.6,
            'dmg_weak': 7,
        }

    def test_serialize(self):
        weapons = [Data(**self.weapon_data.copy()) for _ in range(3)]
        weapons[0].weapon = 'pg'
        weapons[1].weapon = 'rl'
        weapons[2].weapon = 'eb'
        serializer = serializers.MatchWeaponSetSerializer(instance=weapons)
        expected = {name: self.weapon_data for name in ('pg', 'rl', 'eb')}

        self.assertEqual(serializer.data, expected)

    def test_deserialize(self):
        data = {name: self.weapon_data.copy() for name in ('pg', 'rl', 'eb')}
        serializer = serializers.MatchWeaponSetSerializer(data=data)

        serializer.is_valid()
        self.assertFalse(serializer.errors)
        for weapon in serializer.validated_data:
            self.assertIn(weapon.pop('weapon'), ('pg', 'rl', 'eb'))
            self.assertEqual(weapon, self.weapon_data)

    def test_invalid_weapon(self):
        data = {'long': self.weapon_data.copy()}
        serializer = serializers.MatchWeaponSetSerializer(data=data)

        self.assertFalse(serializer.is_valid())

    def test_invalid_weaponset(self):
        serializer = serializers.MatchWeaponSetSerializer(data=3)

        self.assertFalse(serializer.is_valid())


class MatchAwardSerializerTest(TestCase):
    def test_serialize(self):
        data = Data(name='award', count=2)
        serializer = serializers.MatchAwardSerializer(data)
        expected = {'name': 'award', 'count': 2}

        self.assertEqual(serializer.data, expected)

    def test_deserialize(self):
        data = {'name': 'award', 'count': 2}
        serializer = serializers.MatchAwardSerializer(data=data)
        expected = {'name': 'award', 'count': 2}

        serializer.is_valid()
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.validated_data, expected)


class MatchFragSerializerTest(TestCase):
    def setUp(self):
        self.victim = models.Player.objects.create(
            login='victim',
            ip='132.233.139.177',
        )
        self.vsession = models.PlayerSession.objects.create(
            user_id=self.victim.pk,
            ip=self.victim.ip,
        )

    def test_serialize(self):
        data = Data(victim=self.vsession, weapon='pg')
        serializer = serializers.MatchFragSerializer(data)
        expected = {
            'victim': self.vsession.pk,
            'weapon': 'pg',
        }

        self.assertEqual(serializer.data, expected)

    def test_deserialize(self):
        data = {
            'victim': self.vsession.pk,
            'weapon': 'pg',
        }
        serializer = serializers.MatchFragSerializer(data=data)
        expected = {
            'victim': self.vsession,
            'weapon': 'pg',
        }

        serializer.is_valid()
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.validated_data, expected)


class MatchPlayerSerializerTest(TestCase):
    def setUp(self):
        self.player = models.Player.objects.create(
            login='player',
            ip='132.233.139.177',
        )
        self.csession = models.PlayerSession.objects.create(
            user_id=self.player.pk,
            ip=self.player.ip,
        )

    def test_serialize(self):
        data = {
            'final': 1,
            'sessionid': self.csession,
            'awards': [
                Data(name='a', count=2),
                Data(name='b', count=4),
            ],
        }
        serializer = serializers.MatchPlayerSerializer(Data(**data))
        expected = {
            'final': 1,
            'sessionid': self.csession.pk,
            'awards': [
                {'name': 'a', 'count': 2},
                {'name': 'b', 'count': 4},
            ],
        }

        self.assertEqual(serializer.data, expected)

    def test_deserialize(self):
        data = {
            'final': 1,
            'sessionid': self.csession.pk,
            'awards': [
                {'name': 'a', 'count': 2},
                {'name': 'b', 'count': 4},
            ],
        }
        serializer = serializers.MatchPlayerSerializer(data=data)
        expected = {
            'final': 1,
            'sessionid': self.csession,
            'awards': [
                {'name': 'a', 'count': 2},
                {'name': 'b', 'count': 4},
            ],
        }

        serializer.is_valid()
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.validated_data, expected)


class MatchRaceRunSerializerTest(TestCase):
    def setUp(self):
        self.player = models.Player.objects.create(
            login='player',
            ip='132.233.139.177',
        )
        self.csession = models.PlayerSession.objects.create(
            user_id=self.player.pk,
            ip=self.player.ip,
        )

    def test_serialize(self):
        data = Data(
            session_id=self.csession,
            utctime=datetime(1970, 1, 1, tzinfo=timezone.utc),
            times=[1, 2, 3],
        )
        serializer = serializers.MatchRaceRunSerializer(data)
        expected = {
            'session_id': self.csession.pk,
            'timestamp': 0,
            'times': [1, 2, 3],
        }

        self.assertEqual(serializer.data, expected)

    def test_deserialize(self):
        data = {
            'session_id': self.csession.pk,
            'timestamp': 0,
            'times': [1, 2, 3],
        }
        serializer = serializers.MatchRaceRunSerializer(data=data)
        expected = {
            'session_id': self.csession,
            'utctime': datetime(1970, 1, 1, tzinfo=timezone.utc),
            'times': [1, 2, 3],
        }

        serializer.is_valid()
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.validated_data, expected)


class MatchResultSerializerTest(TestCase):
    def setUp(self):
        self.player = models.Player.objects.create(
            login='player',
            ip='132.233.139.177',
        )
        self.csession = models.PlayerSession.objects.create(
            user_id=self.player.pk,
            ip=self.player.ip,
        )

    def test_deserialize(self):
        data = {
            'gametype': 'ca',
            'teamgame': True,
            'map': 'wca1',
            'hostname': 'host',
            'timeplayed': 1000,
            'timelimit': 999,
            'scorelimit': 998,
            'instagib': True,
            'teamgame': True,
            'racegame': False,
            'timestamp': 0,
            'gamedir': 'basewsw',
            'demo_filename': 'demo',
        }
        serializer = serializers.MatchResultSerializer(data=data)
        expected = {
            'gametype': 'ca',
            'teamgame': True,
            'map': 'wca1',
            'hostname': 'host',
            'matchtime': 1000,
            'timelimit': 999,
            'scorelimit': 998,
            'instagib': True,
            'teamgame': True,
            'racegame': False,
            'utctime': datetime(1970, 1, 1, tzinfo=timezone.utc),
            'gamedir': 'basewsw',
            'demo_filename': 'demo',
        }

        serializer.is_valid()
        self.assertFalse(serializer.errors)
        self.assertEqual(serializer.validated_data, expected)


class MatchSerializerTest(TestCase):
    def setUp(self):
        self.attacker = models.Player.objects.create(
            login='attacker',
            ip='132.233.139.177',
        )
        self.asession = models.PlayerSession.objects.create(
            user_id=self.attacker.pk,
            ip=self.attacker.ip,
        )
        self.victim = models.Player.objects.create(
            login='victim',
            ip='132.139.233.177',
        )
        self.vsession = models.PlayerSession.objects.create(
            user_id=self.victim.pk,
            ip=self.victim.ip,
        )
        self.server = models.Server.objects.create(
            login='server',
            ip='1:2:3:4:5:6:7:8',
        )
        self.ssession = models.ServerSession.objects.create(
            user_id=self.server.pk,
            ip=self.server.ip,
            port=44400,
        )

        self.data = {
            'match': {
                'gametype': 'ca',
                'teamgame': True,
                'racegame': False,
                'map': 'wca1',
                'hostname': 'host',
                'timeplayed': 100,
                'timestamp': 0,
                'gamedir': 'basewsw',
            },
            'players': [
                {
                    'final': 1,
                    'team': 1,
                    'sessionid': self.asession.pk,
                    'frags': 2,
                    'deaths': 0,
                    'awards': [
                        {'name': 'a', 'count': 2},
                        {'name': 'b', 'count': 3},
                    ],
                    'weapons': {
                        'pg': {'dmg_strong': 10},
                        'rl': {'dmg_strong': 20},
                    },
                    'log_frags': [
                        {
                            'victim': self.vsession.pk,
                            'weapon': 'pg',
                            'time': 1,
                        }, {
                            'victim': self.vsession.pk,
                            'weapon': 'rl',
                            'time': 2,
                        }
                    ],
                }, {
                    'final': 1,
                    'team': 2,
                    'frags': 0,
                    'deaths': 2,
                    'sessionid': self.vsession.pk,
                    'awards': [{'name': 'b', 'count': 4}],
                }
            ],
            'teams': [
                {'name': 'Alpha', 'score': 2, 'index': 1},
                {'name': 'Beta', 'score': 0, 'index': 2},
            ],
        }
        self.serializer = serializers.MatchSerializer(data=self.data)
        self.serializer.is_valid()
        self.serializer.save(server_session=self.ssession)

    def test_valid(self):
        self.assertFalse(self.serializer.errors)

    def test_create_base_models(self):
        """It should create base models if they don't exist"""
        models.Gametype.objects.get(name='ca')
        models.Map.objects.get(mapname='wca1')
        models.Weapon.objects.get(name='pg')
        models.Weapon.objects.get(name='rl')

    def test_matchresult(self):
        """Ensure the matchresult is properly created"""
        matchresult = models.MatchResult.objects.get(server=self.server)
        self.assertEqual(matchresult.gametype.name, 'ca')
        self.assertEqual(matchresult.map.mapname, 'wca1')
        self.assertEqual(matchresult.gamedir, 'basewsw')

    def test_matchplayers(self):
        """Ensure players are properly created"""
        attacker = models.MatchPlayer.objects.get(player=self.attacker)
        victim = models.MatchPlayer.objects.get(player=self.victim)
        self.assertEqual(attacker.matchteam.name, 'Alpha')
        self.assertEqual(attacker.deaths, 0)
        self.assertEqual(attacker.frags, 2)
        self.assertEqual(victim.matchteam.name, 'Beta')
        self.assertEqual(victim.deaths, 2)
        self.assertEqual(victim.frags, 0)

    def test_matchawards(self):
        """Ensure awards are properly created"""
        self.assertEqual(models.MatchAward.objects.filter(player=self.attacker).count(), 2)
        self.assertEqual(models.MatchAward.objects.filter(player=self.victim).count(), 1)

    def test_matchfrags(self):
        """Ensure frags are properly created"""
        models.MatchFrag.objects.get(attacker=self.attacker, weapon__name='pg')
        models.MatchFrag.objects.get(attacker=self.attacker, weapon__name='rl')

    def test_matchweapons(self):
        """Ensure weapons are properly created"""
        models.MatchWeapon.objects.get(player=self.attacker, weapon__name='pg', dmg_strong=10)
        models.MatchWeapon.objects.get(player=self.attacker, weapon__name='rl', dmg_strong=20)


class RaceMatchSerializerTest(TestCase):
    def setUp(self):
        self.player = models.Player.objects.create(
            login='player',
            ip='132.233.139.177',
        )
        self.csession = models.PlayerSession.objects.create(
            user_id=self.player.pk,
            ip=self.player.ip,
        )
        self.server = models.Server.objects.create(
            login='server',
            ip='1:2:3:4:5:6:7:8',
        )
        self.ssession = models.ServerSession.objects.create(
            user_id=self.server.pk,
            ip=self.server.ip,
            port=44400,
        )

        self.data = {
            'match': {
                'gametype': 'race',
                'teamgame': False,
                'racegame': True,
                'map': 'wrace1',
                'hostname': 'host',
                'timeplayed': 100,
                'timestamp': 0,
                'gamedir': 'basewsw',
            },
            'runs': [{
                'session_id': self.csession.pk,
                'timestamp': 0,
                'times': [1, 2, 3],
            }, {
                'session_id': self.csession.pk,
                'timestamp': 0,
                'times': [2, 3, 4],
            }]
        }
        self.serializer = serializers.MatchSerializer(data=self.data)
        self.serializer.is_valid()
        self.serializer.save(server_session=self.ssession)

    def test_runs(self):
        """It should create the proper sectors and race runs"""
        # Check first race sectors
        models.RaceSector.objects.get(sector=-1, time=3)
        models.RaceSector.objects.get(sector=0, time=1)
        models.RaceSector.objects.get(sector=1, time=2)

        # Check second race sectors
        models.RaceSector.objects.get(sector=-1, time=4)
        models.RaceSector.objects.get(sector=0, time=2)
        models.RaceSector.objects.get(sector=1, time=3)

        self.assertEqual(models.RaceRun.objects.count(), 2)
        self.assertEqual(models.RaceSector.objects.count(), 6)
