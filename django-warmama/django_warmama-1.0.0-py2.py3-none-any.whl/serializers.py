from __future__ import division

from django.db import transaction
from rest_framework import serializers
from warmama import fields, models


class MatchTeamSerializer(serializers.ModelSerializer):
    """MatchTeam sub-serializer for MatchResults

    Excluded fields:
        matchresult

    Extra fields:
        index (int): Team index in the match, used to associate players with teams
    """
    index = serializers.IntegerField()

    class Meta:
        model = models.MatchTeam
        exclude = ('matchresult',)


class MatchWeaponSerializer(serializers.ModelSerializer):
    """MatchWeapon sub-serializer for MatchResults

    Override fields:
        weapon (str): Name of the weapon
        acc_strong (float): Handles as a float instead of a Decimal
        acc_weak (float): Handles as a float instead of a Decimal

    Excluded fields:
        player, match_result
    """
    weapon = serializers.CharField(max_length=2)
    acc_strong = serializers.FloatField(required=False)
    acc_weak = serializers.FloatField(required=False)

    class Meta:
        model = models.MatchWeapon
        exclude = ('player', 'matchresult')


class MatchWeaponSetSerializer(serializers.BaseSerializer):
    """Wrapper for serializing match weapons in the form

    ```
    {
        "name": { stats... },
        "name": { stats... },
        ...
    }
    ```
    """
    default_error_messages = {
        'invalid': 'data must be a dictionary',
        'invalid_weapon': 'Invalid weapon data: {weapon}',
    }

    def __init__(self, *args, **kwargs):
        self.skip_invalid = kwargs.pop('skip_invalid', False)
        super(MatchWeaponSetSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        """Serialize an iterable of weapons"""
        result = {}
        for weapon in obj:
            weapon_serializer = MatchWeaponSerializer(weapon)
            data = weapon_serializer.data
            name = data.pop('weapon')
            result[name] = data

        return result

    def to_internal_value(self, data):
        """Deserialize data"""
        result = []
        try:
            iterweapons = data.items()
        except AttributeError:
            self.fail('invalid')

        for name, weapon in iterweapons:
            data = weapon.copy()
            data['weapon'] = name
            weapon_serializer = MatchWeaponSerializer(data=data)
            if weapon_serializer.is_valid():
                result.append(weapon_serializer.validated_data)
            elif not self.skip_invalid:
                self.fail('invalid_weapon', weapon=data)

        return result


class MatchAwardSerializer(serializers.ModelSerializer):
    """MatchAward sub-serializer for MatchPlayer

    Included fields:
        count

    Extra fields:
        name (str): Name of the related award
    """
    name = serializers.CharField(max_length=64)

    class Meta:
        model = models.MatchAward
        fields = ('name', 'count')


class MatchFragSerializer(serializers.ModelSerializer):
    """MatchFrag sub-serializer for MatchPlayer

    Override fields:
        victim (int): Match players based on PlayerSessions
        weapon (str): Name of the weapon

    Excluded fields:
        created, matchresult, attacker
    """
    victim = serializers.PrimaryKeyRelatedField(queryset=models.PlayerSession.objects)
    weapon = serializers.CharField(max_length=2)

    class Meta:
        model = models.MatchFrag
        exclude = ('created', 'matchresult', 'attacker')


class MatchPlayerSerializer(serializers.ModelSerializer):
    """MatchReport sub-serializer for MatchPlayer objects

    Players are looked up by PlayerSession, not Player pk

    Excluded fields:
        player, matchresult, matchteam, oldrating, newrating,
        teamkills, matchtime

    Extra fields:
        final (int): If falsey, the player quit before the match ended
        sessionid (int): pk of player session, used to identify player
        team (int): index of team this player was a member of
        teamfrags (int): alias for player.teamkills
        timeplayed (int): alias for player.matchtime
        weapons (dict): Set of weapon stats for the player, see
            MatchWeaponSetSerializer for details
        awards (iterable): Iterable of Awards for the player
        log_frags (iterable): Iterable of frags for the player
    """
    final = serializers.IntegerField()
    sessionid = serializers.PrimaryKeyRelatedField(queryset=models.PlayerSession.objects)
    team = serializers.IntegerField(source='matchteam', required=False)
    teamfrags = serializers.IntegerField(source='teamkills', required=False)
    timeplayed = serializers.IntegerField(source='matchtime', min_value=1, required=False)
    weapons = MatchWeaponSetSerializer(required=False)
    awards = MatchAwardSerializer(many=True, required=False)
    log_frags = MatchFragSerializer(many=True, required=False)

    class Meta:
        model = models.MatchPlayer
        exclude = (
            'player', 'matchresult', 'matchteam', 'oldrating',
            'newrating', 'teamkills', 'matchtime'
        )


class MatchRaceRunSerializer(serializers.Serializer):
    """MatchRaceRun sub-serializer for MatchResult

    Fields:
        session_id (int): PlayerSession for the racer
        timestamp (int): POSIX Timestamp for the time race was finished
        times (iterable): Iterable of sector times
    """
    session_id = serializers.PrimaryKeyRelatedField(queryset=models.PlayerSession.objects)
    timestamp = fields.TimestampField(source='utctime')
    times = serializers.ListField(child=serializers.IntegerField(min_value=0))


class MatchResultSerializer(serializers.ModelSerializer):
    """Match Result

    Override Fields:
        gametype (str): Maps to gametype objects by name
        map (str): Maps to Map objects by name

    Excluded Fields:
        created, updated, server, uuid, matchtime, utctime, winner_team,
        winner_player

    Extra fields:
        hostname (str): TODO I have no idea
        racegame (bool): True if the game was race
        timestamp (int): POSIX Timestamp when match finished
        timeplayed (int): Length of the match in milliseconds
    """
    gametype = serializers.CharField(max_length=16)
    map = serializers.CharField(max_length=64)
    hostname = serializers.CharField(max_length=128)
    racegame = serializers.BooleanField()
    timeplayed = serializers.IntegerField(min_value=66, source='matchtime')
    timestamp = fields.TimestampField(source='utctime')

    class Meta:
        model = models.MatchResult
        exclude = (
            'created', 'updated', 'server', 'uuid', 'matchtime', 'utctime',
            'winner_team', 'winner_player'
        )

    def create(self, validated_data):
        return super(MatchResultSerializer, self).create(validated_data)


class MatchSerializer(serializers.Serializer):
    """Match Serializer

    Fields:
        match (dict): MatchResult
        teams (iterable): MatchTeams
        players (iterable): MatchPlayers (optional)
        runs (iterable): RaceRuns (optional)
    """
    match = MatchResultSerializer()
    teams = MatchTeamSerializer(many=True, required=False)
    players = MatchPlayerSerializer(many=True, required=False)
    runs = MatchRaceRunSerializer(many=True, required=False)

    def _init_cache(self):
        """Create caches for base models"""
        self._award_cache = {}  # name: models.Award
        self._weapon_cache = {}  # name: models.Weapon

    def _create_match_result(self, matchdata, server_id):
        """Create the MatchResult model from matchdata

        This may create a Gametype and Map model if nessecary
        """
        matchdata['gametype'], _ = models.Gametype.objects.get_or_create(
            name=matchdata['gametype'],
            defaults={'description': matchdata['gametype']}
        )
        matchdata['map'], _ = models.Map.objects.get_or_create(mapname=matchdata['map'])
        return models.MatchResult.objects.create(server_id=server_id, **matchdata)

    def _create_match_teams(self, teamdata, matchresult):
        """Create Team models for the match

        Creates Team models and returns them in a dict of { teamindex : Team }
        """
        # The team pk is needed for players later, so `.bulk_create()` cannot be
        # used here
        teams = {}
        for team in teamdata:
            index = team.pop('index')
            teams[index] = models.MatchTeam.objects.create(matchresult=matchresult, **team)
        return teams

    def _create_match_players(self, playerdata, matchteams):
        """Create MatchPlayers for the match

        Returns a map { session_id : MatchPlayer }
        """
        players = {}
        for matchplayer in playerdata:
            matchplayer.pop('final')  # TODO: used in skill calculation
            player_session = matchplayer.pop('sessionid')
            matchplayer['player_id'] = player_session.user_id

            teamindex = matchplayer.pop('matchteam', None)
            if teamindex is not None:
                matchplayer['matchteam'] = matchteams[teamindex]

            players[player_session.pk] = models.MatchPlayer.objects.create(**matchplayer)

        return players

    def _create_match_awards(self, awarddata):
        """Create MatchAwards for the match

        This will create missing Award models if necessary
        """
        for matchaward in awarddata:
            name = matchaward.pop('name')
            if name not in self._award_cache:
                self._award_cache[name], _ = models.Award.objects.get_or_create(name=name)

            matchaward['award'] = self._award_cache[name]

        models.MatchAward.objects.bulk_create(
            models.MatchAward(**matchaward) for matchaward in awarddata
        )

    def _create_match_frags(self, fragdata):
        """Create MatchFrags for the match

        This will create missing Weapon models if necessary
        """
        for matchfrag in fragdata:
            name = matchfrag.pop('weapon')
            if name not in self._weapon_cache:
                self._weapon_cache[name], _ = models.Weapon.objects.get_or_create(name=name, defaults={'fullname': name})

            victim_session = matchfrag.pop('victim')
            matchfrag['victim_id'] = victim_session.user_id
            matchfrag['weapon'] = self._weapon_cache[name]

        models.MatchFrag.objects.bulk_create(
            models.MatchFrag(**matchfrag) for matchfrag in fragdata
        )

    def _create_match_weapons(self, weapondata):
        """Create MatchWeapons for the match

        This will create missing Weapon models if necessary
        """
        for matchweapon in weapondata:
            name = matchweapon.pop('weapon')
            if name not in self._weapon_cache:
                self._weapon_cache[name], _ = models.Weapon.objects.get_or_create(name=name, defaults={'fullname': name})

            matchweapon['weapon'] = self._weapon_cache[name]

        models.MatchWeapon.objects.bulk_create(
            models.MatchWeapon(**matchweapon) for matchweapon in weapondata
        )

    def _create_runs(self, rundata, map_id, server_id):
        """Create Raceruns and RaceSectors for the match"""
        sectors = []
        for racerun in rundata:
            player_session = racerun.pop('session_id')
            times = sorted(racerun.pop('times'))
            racerun['map_id'] = map_id
            racerun['server_id'] = server_id
            racerun['player_id'] = player_session.user_id
            runobj = models.RaceRun.objects.create(**racerun)

            if not times:
                continue

            # The last entry is the race time, not a checkpoint
            # Gets saved with special value `sector -1`
            sectors.append(
                models.RaceSector(run=runobj, sector=-1, time=times[-1])
            )

            # The others are indexed by their position
            sectors.extend(
                models.RaceSector(run=runobj, sector=index, time=time)
                for index, time in enumerate(times[:-1])
            )

        models.RaceSector.objects.bulk_create(sectors)

    def _get_player_data(self, playerdata, matchresult):
        """Pull the awards, frags, and weapons out of players

        Returns a tuple `(awards, frags, weapons)` where each entry is a list of
        data for that model. The returned data is ready to be used in the
        relevant `_create_*` method. The argument `playerdata` will be modified
        to have the nested values removed.
        """
        awards = []
        frags = []
        weapons = []
        for player in playerdata:
            pid = player['sessionid'].user_id
            player['matchresult'] = matchresult
            player_awards = player.pop('awards', [])
            player_frags = player.pop('log_frags', [])
            player_weapons = player.pop('weapons', [])

            # attach player / match information to the entries and append them
            awards.extend(
                dict(player_id=pid, matchresult=matchresult, **awd)
                for awd in player_awards
            )
            frags.extend(
                dict(attacker_id=pid, matchresult=matchresult, **frag)
                for frag in player_frags
            )
            weapons.extend(
                dict(player_id=pid, matchresult=matchresult, **weapon)
                for weapon in player_weapons
            )
        return awards, frags, weapons

    @transaction.atomic
    def create(self, data):
        """Save the validated_data to all the associated model objects"""
        ssession = data.get('server_session', None)
        assert isinstance(ssession, models.ServerSession), (
            'A valid server session was not provided. Serializer must be saved'
            'using `.save(server_session=ServerSessionObject)`'
        )

        assert 'players' in data or 'runs' in data, (
            'No players section or runs section in match'
        )

        assert 'teams' in data or not data['match'].get('teamgame', True), (
            'No teams section in match'
        )

        self._init_cache()
        sid = ssession.user_id
        data['match'].pop('hostname', '')  # TODO what is this used for?
        data['match'].pop('racegame', False)  # not used atm

        matchresult = self._create_match_result(data['match'], sid)
        matchteams = self._create_match_teams(data.get('teams', []), matchresult)

        players = data.get('players', [])
        awards, frags, weapons = self._get_player_data(players, matchresult)

        matchplayers = self._create_match_players(players, matchteams)
        self._create_match_awards(awards)
        self._create_match_frags(frags)
        self._create_match_weapons(weapons)

        self._create_runs(data.get('runs', []), matchresult.map_id, sid)

        # TODO process stats, ratings and set winner_team / winner_player

        # Release the cache
        self._init_cache()
        return matchresult, matchplayers
