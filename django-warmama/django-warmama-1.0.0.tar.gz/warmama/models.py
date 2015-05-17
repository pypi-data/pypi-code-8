"""Warmama database models"""
import uuid
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


##########
# Game Models
##########


@python_2_unicode_compatible
class Award(models.Model):
    """Award

    Attributes:
        name (str): Name of the map.
    """
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = 'awards'

    def __str__(self):
        return '{0}'.format(self.name)


@python_2_unicode_compatible
class Achievement(models.Model):
    """Achievement

    Attributes:
        name (str): Name of the achievement
        description (str): Description of the achievement
        numgotten (int): (default: 0) #TODO no idea what this is for
    """
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=128)
    numgotten = models.IntegerField(default=0)

    class Meta:
        db_table = 'achievements'

    def __str__(self):
        return '{0}'.format(self.name)


@python_2_unicode_compatible
class Gametype(models.Model):
    """Gametype

    Attributes:
        name (str): Abbreviated name of the gametype.
        description (str): Long name of the gametype.

    Reverse lookup attributes:
        matches (QuerySet): MatchResult objects for every match of the gametype
    """
    name = models.CharField(max_length=16, unique=True)
    description = models.CharField(max_length=32)

    class Meta:
        db_table = 'gametypes'

    def __str__(self):
        return '{0}'.format(self.name)


@python_2_unicode_compatible
class Map(models.Model):
    """Map

    Attributes:
        mapname (str): Name of the map

    Reverse lookup attributes:
        matches (QuerySet): MatchResult objects for every match on the map
    """
    mapname = models.CharField(max_length=64, unique=True)

    class Meta:
        db_table = 'mapnames'

    def __str__(self):
        return '{0}'.format(self.mapname)


@python_2_unicode_compatible
class Weapon(models.Model):
    """Weapon

    Attributes:
        name (str): Abbreviated name of the weapon.
        fullname (str): Long name of the weapon.
    """
    name = models.CharField(max_length=2, unique=True)
    fullname = models.CharField(max_length=16)

    class Meta:
        db_table = 'weapons'

    def __str__(self):
        return '{0}'.format(self.name)


@python_2_unicode_compatible
class Player(models.Model):
    """Player class

    Attributes:
        created (datetime): Time when the record was created
        updated (datetime): Time when the record was last modified
        login (str): Login username. This field must be unique
        nickname (str): Ingame nickname with color codes
        ip (str): IPv4 address
        ipv6 (str): IPv6 address
        location (str): Two letter country code
        banned (bool): Player is banned (default: False)

    Reverse lookup attributes:
        session (PlayerSession): Session the player is connected with
        stats (QuerySet): PlayerStat objects for the player
        achievements (QuerySet): PlayerAchievement objects for the player
        matches (QuerySet): MatchPlayer objects for the player
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    login = models.CharField(max_length=64, unique=True)
    nickname = models.CharField(max_length=64, blank=True)
    ip = models.CharField(max_length=22, blank=True)
    ipv6 = models.CharField(max_length=54, blank=True)
    location = models.CharField(max_length=2, blank=True, db_index=True)
    banned = models.BooleanField(default=False)

    class Meta:
        db_table = 'players'

    def __str__(self):
        return '{0}'.format(self.login)


@python_2_unicode_compatible
class Server(models.Model):
    """Server class

    Attributes:
        created (datetime): Time when the record was created
        updated (datetime): Time when the record was last modified
        login (str): Login username. This field must be unique
        regip (str): IPv4 address server registered with
        regipv6 (str): IPv6 address server registered with
        hostname (str): Hostname
        ip (str): IPv4 address server logged in with TODO: will this ever differ from regip?
        ipv6 (str): IPv6 address server logged in with TODO: will this ever differ from regipv6?
        location (str): Two letter country code
        banned (bool): Banned (default: False)
        demos_baseurl (str): `sv_uploads_demos_baseurl` value for server

    Reverse lookup attributes:
        session (ServerSession): Session the server is connected with
        matches (QuerySet): MatchResult objects for every match the server hosted
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    login = models.CharField(max_length=64, unique=True)
    regip = models.CharField(max_length=22, blank=True, db_index=True)
    regipv6 = models.CharField(max_length=54, blank=True)
    hostname = models.CharField(max_length=64, blank=True)
    ip = models.CharField(max_length=22, blank=True, db_index=True)
    ipv6 = models.CharField(max_length=54, blank=True)
    location = models.CharField(max_length=2, blank=True, db_index=True)
    banned = models.BooleanField(default=False)
    demos_baseurl = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = 'servers'

    def __str__(self):
        return '{0}'.format(self.regip)


##########
# Sessions and Auth
##########


@python_2_unicode_compatible
class ServerSession(models.Model):
    """Server session class

    Attributes:
        created (datetime): Time when the record was created
        updated (datetime): Time when the record was last modified
        user (Server): Server the session belongs to
        ip (str): IPv4 address
        ipv6 (str): IPv6 address
        digest (str): #TODO Used for remote authentication?
        port (int): Port game is being served on.
        next_match_uuid (str): #TODO No idea what this is for
    """
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField('Server', related_name='session', db_index=True)
    ip = models.CharField(max_length=22, blank=True, db_index=True)
    ipv6 = models.CharField(max_length=54, blank=True)
    digest = models.CharField(default=uuid.uuid4, max_length=36)
    port = models.IntegerField()
    next_match_uuid = models.CharField(max_length=36, blank=True, unique=True)

    class Meta:
        db_table = 'sessions_server'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class PlayerSession(models.Model):
    """Player session class

    If a player is requesting a connection, `ticket_id`, `ticket_server`, and
    `ticket_expiration` will be defined and `server_session` will be `None`.

    If a player has connected to a server `ticket_id`, `ticket_server`, and
    `ticket_expiration` will be `None` and `server_session` will be defined.

    If a player has disconnected, the session is over. All the fields will be
    `None` and `purgable` will be `True`.

    Attributes:
        created (datetime): Time when the record was created
        updated (datetime): Time when the record was last modified
        user (Player): Player
        ip (str): IPv4 address
        ipv6 (str): IPv6 address
        digest (str): #TODO Used for remote authentication?
        ticket_id (int): Identifier for the ticket
        ticket_server (ServerSession): ServerSession that client requested to connect to
        ticket_expiration (datetime): Time when the ticket expires
        server_session (ServerSession): ServerSession that client is connected to
        purgable (bool): True if the session may be purged (default: False)

    Reverse lookup attributes:
        purge_player (PurgePlayer): Purge object for the session
    """
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.OneToOneField('Player', related_name='session')
    ip = models.CharField(max_length=22, blank=True)
    ipv6 = models.CharField(max_length=54, blank=True)
    digest = models.CharField(default=uuid.uuid4, max_length=32)
    ticket_id = models.IntegerField(default=0, blank=True, null=True)
    ticket_server = models.ForeignKey('ServerSession', blank=True, null=True, db_column='ticket_server', related_name='+', on_delete=models.SET_NULL, db_index=True)
    ticket_expiration = models.DateTimeField(blank=True, null=True)
    server_session = models.ForeignKey('ServerSession', blank=True, null=True, db_column='server_session', related_name='+', on_delete=models.SET_NULL, db_index=True)
    purgable = models.BooleanField(default=False)

    class Meta:
        db_table = 'sessions_player'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class PurgePlayer(models.Model):
    """Purgable player sessions

    Attributes:
        created (datetime): Time when the record was created
        updated (datetime): Time when the record was last modified
        session (PlayerSession): PlayerSession that may be purged
        player (Player): Player for the session
        server_session (ServerSession): ServerSession that marked as purgable
    """
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    session = models.OneToOneField('PlayerSession', related_name='purge_player', db_index=True)
    player = models.OneToOneField('Player', related_name='+', db_index=True)
    server_session = models.ForeignKey('ServerSession', blank=True, null=True, db_column='server_session', related_name='+', db_index=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'purge_players'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class LoginPlayer(models.Model):
    """Login players

    Attributes:
        created (datetime): Time when record was created
        login (str): Player's login name
        ready (bool): Ready state (default: True)
        valid (bool): Valid state (default: True)
        profile_url (str): Url to player profile
        profile_url_rml (str): Url to player profile in rml format
    """
    created = models.DateTimeField(auto_now_add=True)
    login = models.CharField(max_length=64, unique=True)
    ready = models.BooleanField(default=False)
    valid = models.BooleanField(default=False)
    profile_url = models.CharField(max_length=255, blank=True)
    profile_url_rml = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'login_players'

    def __str__(self):
        return '{0}'.format(self.pk)


##########
# Player Results
##########


@python_2_unicode_compatible
class PlayerStat(models.Model):
    """Overall stats for a (player, gametype) pair

    Attributes:
        player (Player): Player stats belong to
        created (datetime): Time the record was first created
        updated (datetime): Time the record was last modified
        gametype (Gametype): Gametype the stat is for
        wins (int): Number of wins (default: 0)
        losses (int): Number of losses (default: 0)
        quits (int): Number of quits (default: 0)
        rating (Decimal): Player's rating value (mu) for the gametype (default: 0)
        deviation (Decimal): Player's rating deviation (sigma) for the gametype (default: 0)
    """
    player = models.ForeignKey('Player', related_name='stats')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    gametype = models.ForeignKey('Gametype', related_name='+')
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    quits = models.IntegerField(default=0)
    rating = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    deviation = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'player_stats'
        unique_together = ('player', 'gametype')

    def __str__(self):
        return '{0} {1}'.format(self.gametype_id, self.player_id)


@python_2_unicode_compatible
class PlayerAchievement(models.Model):
    """Achievements a player has won

    Attributes:
        player (Player): Player
        created (datetime): Time the record was first created
        updated (datetime): Time the record was last modified
        achievement (Achievement): Achievement
    """
    player = models.ForeignKey('Player', related_name='achievements', db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    achievement = models.ForeignKey('Achievement', related_name='+')

    class Meta:
        db_table = 'player_achievements'

    def __str__(self):
        return '{0} {1}'.format(self.achievement_id, self.player_id)


##########
# Match Results
##########


@python_2_unicode_compatible
class MatchResult(models.Model):
    """Match Result

    Attributes:
        created (datetime): Time the record was first created
        updated (datetime): Time the record was last modified
        server (Server): Server the match was hosted on
        gametype (Gametype): Gametype for the match
        uuid (str): Unique identifier string for the match result (default: uuid.uuid4)
        instagib (bool): True if match was instagib (default: False)
        teamgame (bool): True if match was teamgame (default: False)
        map_id (int): Pointer to map's pk
        timelimit (int): Time limit for the match (default: 0)
        scorelimit (int): Score limit for the match (default: 0)
        gamedir (str): `fs_game` value for the match
        matchtime (int): Length of the match in seconds (default: 0)
        utctime (datetime): Time the match was ended
        winner_team (MatchTeam): Winning MatchTeam
        winner_player (MatchPlayer): Winning MatchPlayer
        demo_filename (str): Name of demo file for the match

    Reverse lookup attributes:
        teams (QuerySet): MatchTeam objects in the match
        players (QuerySet): MatchPlayer objects in the match
        frags (QuerySet): MatchFrag objects in the match
    """
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)
    server = models.ForeignKey('Server', related_name='matches', db_index=True)
    gametype = models.ForeignKey('Gametype', related_name='matches', db_index=True)
    uuid = models.CharField(default=uuid.uuid4, max_length=36, unique=True)
    instagib = models.BooleanField(default=False)
    teamgame = models.BooleanField(default=False)
    map = models.ForeignKey('Map', related_name='matches')
    timelimit = models.IntegerField(default=0)
    scorelimit = models.IntegerField(default=0)
    gamedir = models.CharField(max_length=64, blank=True)
    matchtime = models.IntegerField(default=0)
    utctime = models.DateTimeField()
    winner_team = models.ForeignKey('MatchTeam', related_name='+', blank=True, null=True, db_index=True)
    winner_player = models.ForeignKey('MatchPlayer', related_name='+', blank=True, null=True, db_index=True)
    demo_filename = models.CharField(max_length=128, blank=True)

    class Meta:
        db_table = 'match_results'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class MatchTeam(models.Model):
    """Team in a match

    Attributes:
        matchresult (MatchResult): MatchResult the team was a member of
        name (str): Name of the team
        score (int): Score earned by the team (default: 0)

    Reverse lookup attributes:
        players (QuerySet): MatchPlayer objects in the match
    """
    matchresult = models.ForeignKey('MatchResult', related_name='teams', db_index=True)
    name = models.CharField(max_length=64)
    score = models.IntegerField(default=0)

    class Meta:
        db_table = 'match_teams'
        unique_together = ('matchresult', 'name')

    def __str__(self):
        return '{0}'.format(self.name)


@python_2_unicode_compatible
class MatchPlayer(models.Model):
    """Player results in a match

    Attributes:
        player (Player): Player
        matchresult (MatchResult): MatchResult
        matchteam (MatchTeam): MatchTeam
        name (str): Player's name in match TODO: is this login or nickname?
        score (int): Score earned (default: 0)
        frags (int): Frags made (default: 0)
        deaths (int): Times killed (default: 0)
        teamkills (int): Betrayal kills (default: 0)
        suicides (int): Suicides made (default: 0)
        numrounds (int): Rounds played in the match (default: 0)
        ga_taken (int): Green armors taken (default: 0)
        ya_taken (int): Yellow armors taken (default: 0)
        ra_taken (int): Red armors taken (default: 0)
        mh_taken (int): Mega healths taken (default: 0)
        uh_taken (int): Ultra healths taken (default: 0)
        quads_taken (int): Quad damages taken (default: 0)
        shells_taken (int): Wsw shells taken (default: 0)
        bombs_planted (int): Bombs planted (default: 0)
        bombs_defused (int): Bombs defused (default: 0)
        flags_capped (int): Flags captured (default: 0)
        matchtime (int): Playtime in seconds (default: 0)
        oldrating (Decimal): Player's rating before the match (default: 0)
        newrating (Decimal): Player's rating after the match (default: 0)
    """
    # TODO: add dmg, health, armor given/taken
    player = models.ForeignKey('Player', related_name='matches', db_index=True)
    matchresult = models.ForeignKey('MatchResult', related_name='players', db_index=True)
    matchteam = models.ForeignKey('MatchTeam', related_name='players', blank=True, null=True, db_index=True)
    name = models.CharField(max_length=64, blank=True)
    score = models.IntegerField(default=0)
    frags = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    teamkills = models.IntegerField(default=0)
    suicides = models.IntegerField(default=0)
    numrounds = models.IntegerField(default=0)
    ga_taken = models.IntegerField(default=0)
    ya_taken = models.IntegerField(default=0)
    ra_taken = models.IntegerField(default=0)
    mh_taken = models.IntegerField(default=0)
    uh_taken = models.IntegerField(default=0)
    quads_taken = models.IntegerField(default=0)
    shells_taken = models.IntegerField(default=0)
    bombs_planted = models.IntegerField(default=0)
    bombs_defused = models.IntegerField(default=0)
    flags_capped = models.IntegerField(default=0)
    matchtime = models.IntegerField(default=0)
    oldrating = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    newrating = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'match_players'
        unique_together = ('player', 'matchresult')

    def __str__(self):
        return '{0}'.format(self.player_id)


@python_2_unicode_compatible
class MatchAward(models.Model):
    """Player awards for a match

    Attributes:
        player (Player): Player
        matchresult (MatchResult): MatchResult
        award (Award): Award
        count (int): Number of times earned in the match (default: 0)
    """
    player = models.ForeignKey('Player', related_name='+', db_index=True)
    matchresult = models.ForeignKey('MatchResult', related_name='+', db_index=True)
    award = models.ForeignKey('Award', related_name='+', db_index=True)
    count = models.IntegerField(default=0)

    class Meta:
        db_table = 'match_awards'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class MatchWeapon(models.Model):
    """Weapon statistics for a player match

    Attributes:
        player (Player): Player
        matchresult (MatchResult): MatchResult
        weapon (Weapon): Weapon
        shots_strong (int): Number of shots made with strong ammo (default: 0)
        hits_stong (int): Number of hits made with strong ammo (default: 0)
        dmg_strong (int): Total damage dealt with strong ammo (default: 0)
        frags_strong (int): Number of kills made with strong ammo (default: 0)
        acc_strong (Decimal): Accuracy with strong ammo, hits / shots (default: 0)
        shots_weak (int): Number of shots made with weak ammo (default: 0)
        hits_weak (int): Number of hits made with weak ammo (default: 0)
        dmg_weak (int): Total damage dealt with weak ammo (default: 0)
        frags_weak (int): Number of kills made with weak ammo (default: 0)
        acc_weak (Decimal): Accuracy with weak ammo, hits / shots (default: 0)
    """
    player = models.ForeignKey('Player', related_name='+', db_index=True)
    matchresult = models.ForeignKey('MatchResult', related_name='+', db_index=True)
    weapon = models.ForeignKey('Weapon', related_name='+', db_index=True)
    shots_strong = models.IntegerField(default=0)
    hits_strong = models.IntegerField(default=0)
    dmg_strong = models.IntegerField(default=0)
    frags_strong = models.IntegerField(default=0)
    acc_strong = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    shots_weak = models.IntegerField(default=0)
    hits_weak = models.IntegerField(default=0)
    dmg_weak = models.IntegerField(default=0)
    frags_weak = models.IntegerField(default=0)
    acc_weak = models.DecimalField(default=0, max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'match_weapons'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class MatchFrag(models.Model):
    """Frags made in a match

    Attributes:
        created (datetime): Time the record was created
        matchresult (MatchResult): MatchResult
        attacker (MatchPlayer): attacker
        victim (MatchPlayer): victim
        weapon (Weapon): Weapon used in the frag, may be None
        time (int): match time in seconds the frag was made (default: 0)
    """
    created = models.DateTimeField(auto_now_add=True)
    matchresult = models.ForeignKey('MatchResult', related_name='frags', db_index=True)
    attacker = models.ForeignKey('Player', related_name='+', db_index=True)
    victim = models.ForeignKey('Player', related_name='+', db_index=True)
    weapon = models.ForeignKey('Weapon', blank=True, null=True, db_index=True)
    time = models.IntegerField(default=0)

    class Meta:
        db_table = 'frag_log'

    def __str__(self):
        return '{0}'.format(self.pk)


##########
# Race Results
##########


@python_2_unicode_compatible
class RaceRun(models.Model):
    """Race run

    Attributes:
        created (datetime): Time when the record was created
        map (Map): Map
        server (Server): Server
        player (Player): Player
        utctime (datetime): Time when the race was finished

    Reverse lookup attributes:
        sectors (QuerySet): RaceSectors for the run
    """
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    map = models.ForeignKey('Map', related_name='+', db_index=True)
    server = models.ForeignKey('Server', related_name='+', db_index=True)
    player = models.ForeignKey('Player', related_name='+', db_index=True)
    utctime = models.DateTimeField()

    class Meta:
        db_table = 'race_runs'

    def __str__(self):
        return '{0}'.format(self.pk)


@python_2_unicode_compatible
class RaceSector(models.Model):
    """Race sector / checkpoint

    Attributes:
        created (datetime): Time the record was created
        run (RaceRun): RaceRun this belongs to
        sector (int): Id of the sector on the map, `-1` indicates the total
            race time.
        time (int): Time when the sector was crossed in milliseconds (default: 0)
    """
    created = models.DateTimeField(auto_now_add=True)
    run = models.ForeignKey('RaceRun', related_name='sectors', db_index=True)
    sector = models.IntegerField()
    time = models.IntegerField(default=0, db_index=True)

    class Meta:
        db_table = 'race_sectors'
        unique_together = ('run', 'sector')

    def __str__(self):
        return '{0}'.format(self.pk)
