
from functools import wraps


__NI = []
class NotImplemented(Exception):
    pass

class NAR(NotImplemented):
    """ A special late-fail error
        allows the runtime to be of limited use while still incomplete.
    """
    def __str__(self):
        raise self

    def __repr__(self):
        raise self

    def __len__(self):
        raise self

    def __getattr__(self, item):
        raise self

    def __getitem__(self, item):
        raise self

    def __eq__(self, other):
        raise self

    def __gt__(self, other):
        raise self

    def __lt__(self, other):
        raise self

    def __iter__(self):
        raise self




def not_implemented(function):
    __NI.append(function.__name__)

    @wraps(function)
    def _func(*args,**kwargs):
        return NAR(function.__name__)

    return _func




# common.j implementation

# jass2->py3.4

class handle(object):
    pass

class agent(handle):
    pass

class event(agent):
    pass

class player(agent):
    pass

class widget(agent):
    pass

class unit(widget):
    pass

class destructable(widget):
    pass

class item(widget):
    pass

class ability(agent):
    pass

class buff(ability):
    pass

class force(agent):
    pass

class group(agent):
    pass

class trigger(agent):
    pass

class triggercondition(agent):
    pass

class triggeraction(handle):
    pass

class timer(agent):
    pass

class location(agent):
    pass

class region(agent):
    pass

class rect(agent):
    pass

class boolexpr(agent):
    pass

class sound(agent):
    pass

class conditionfunc(boolexpr):
    pass

class filterfunc(boolexpr):
    pass

class unitpool(handle):
    pass

class itempool(handle):
    pass

class race(handle):
    pass

class alliancetype(handle):
    pass

class racepreference(handle):
    pass

class gamestate(handle):
    pass

class igamestate(gamestate):
    pass

class fgamestate(gamestate):
    pass

class playerstate(handle):
    pass

class playerscore(handle):
    pass

class playergameresult(handle):
    pass

class unitstate(handle):
    pass

class aidifficulty(handle):
    pass

class eventid(handle):
    pass

class gameevent(eventid):
    pass

class playerevent(eventid):
    pass

class playerunitevent(eventid):
    pass

class unitevent(eventid):
    pass

class limitop(eventid):
    pass

class widgetevent(eventid):
    pass

class dialogevent(eventid):
    pass

class unittype(handle):
    pass

class gamespeed(handle):
    pass

class gamedifficulty(handle):
    pass

class gametype(handle):
    pass

class mapflag(handle):
    pass

class mapvisibility(handle):
    pass

class mapsetting(handle):
    pass

class mapdensity(handle):
    pass

class mapcontrol(handle):
    pass

class playerslotstate(handle):
    pass

class volumegroup(handle):
    pass

class camerafield(handle):
    pass

class camerasetup(handle):
    pass

class playercolor(handle):
    pass

class placement(handle):
    pass

class startlocprio(handle):
    pass

class raritycontrol(handle):
    pass

class blendmode(handle):
    pass

class texmapflags(handle):
    pass

class effect(agent):
    pass

class effecttype(handle):
    pass

class weathereffect(handle):
    pass

class terraindeformation(handle):
    pass

class fogstate(handle):
    pass

class fogmodifier(agent):
    pass

class dialog(agent):
    pass

class button(agent):
    pass

class quest(agent):
    pass

class questitem(agent):
    pass

class defeatcondition(agent):
    pass

class timerdialog(agent):
    pass

class leaderboard(agent):
    pass

class multiboard(agent):
    pass

class multiboarditem(agent):
    pass

class trackable(agent):
    pass

class gamecache(agent):
    pass

class version(handle):
    pass

class itemtype(handle):
    pass

class texttag(handle):
    pass

class attacktype(handle):
    pass

class damagetype(handle):
    pass

class weapontype(handle):
    pass

class soundtype(handle):
    pass

class lightning(handle):
    pass

class pathingtype(handle):
    pass

class image(handle):
    pass

class ubersplat(handle):
    pass

class hashtable(agent):
    pass


@not_implemented
def ConvertRace(i:"integer")->"race":
    raise NotImplemented
    pass

@not_implemented
def ConvertAllianceType(i:"integer")->"alliancetype":
    raise NotImplemented
    pass

@not_implemented
def ConvertRacePref(i:"integer")->"racepreference":
    raise NotImplemented
    pass

@not_implemented
def ConvertIGameState(i:"integer")->"igamestate":
    raise NotImplemented
    pass

@not_implemented
def ConvertFGameState(i:"integer")->"fgamestate":
    raise NotImplemented
    pass

@not_implemented
def ConvertPlayerState(i:"integer")->"playerstate":
    raise NotImplemented
    pass

@not_implemented
def ConvertPlayerScore(i:"integer")->"playerscore":
    raise NotImplemented
    pass

@not_implemented
def ConvertPlayerGameResult(i:"integer")->"playergameresult":
    raise NotImplemented
    pass

@not_implemented
def ConvertUnitState(i:"integer")->"unitstate":
    raise NotImplemented
    pass

@not_implemented
def ConvertAIDifficulty(i:"integer")->"aidifficulty":
    raise NotImplemented
    pass

@not_implemented
def ConvertGameEvent(i:"integer")->"gameevent":
    raise NotImplemented
    pass

@not_implemented
def ConvertPlayerEvent(i:"integer")->"playerevent":
    raise NotImplemented
    pass

@not_implemented
def ConvertPlayerUnitEvent(i:"integer")->"playerunitevent":
    raise NotImplemented
    pass

@not_implemented
def ConvertWidgetEvent(i:"integer")->"widgetevent":
    raise NotImplemented
    pass

@not_implemented
def ConvertDialogEvent(i:"integer")->"dialogevent":
    raise NotImplemented
    pass

@not_implemented
def ConvertUnitEvent(i:"integer")->"unitevent":
    raise NotImplemented
    pass

@not_implemented
def ConvertLimitOp(i:"integer")->"limitop":
    raise NotImplemented
    pass

@not_implemented
def ConvertUnitType(i:"integer")->"unittype":
    raise NotImplemented
    pass

@not_implemented
def ConvertGameSpeed(i:"integer")->"gamespeed":
    raise NotImplemented
    pass

@not_implemented
def ConvertPlacement(i:"integer")->"placement":
    raise NotImplemented
    pass

@not_implemented
def ConvertStartLocPrio(i:"integer")->"startlocprio":
    raise NotImplemented
    pass

@not_implemented
def ConvertGameDifficulty(i:"integer")->"gamedifficulty":
    raise NotImplemented
    pass

@not_implemented
def ConvertGameType(i:"integer")->"gametype":
    raise NotImplemented
    pass

@not_implemented
def ConvertMapFlag(i:"integer")->"mapflag":
    raise NotImplemented
    pass

@not_implemented
def ConvertMapVisibility(i:"integer")->"mapvisibility":
    raise NotImplemented
    pass

@not_implemented
def ConvertMapSetting(i:"integer")->"mapsetting":
    raise NotImplemented
    pass

@not_implemented
def ConvertMapDensity(i:"integer")->"mapdensity":
    raise NotImplemented
    pass

@not_implemented
def ConvertMapControl(i:"integer")->"mapcontrol":
    raise NotImplemented
    pass

@not_implemented
def ConvertPlayerColor(i:"integer")->"playercolor":
    raise NotImplemented
    pass

@not_implemented
def ConvertPlayerSlotState(i:"integer")->"playerslotstate":
    raise NotImplemented
    pass

@not_implemented
def ConvertVolumeGroup(i:"integer")->"volumegroup":
    raise NotImplemented
    pass

@not_implemented
def ConvertCameraField(i:"integer")->"camerafield":
    raise NotImplemented
    pass

@not_implemented
def ConvertBlendMode(i:"integer")->"blendmode":
    raise NotImplemented
    pass

@not_implemented
def ConvertRarityControl(i:"integer")->"raritycontrol":
    raise NotImplemented
    pass

@not_implemented
def ConvertTexMapFlags(i:"integer")->"texmapflags":
    raise NotImplemented
    pass

@not_implemented
def ConvertFogState(i:"integer")->"fogstate":
    raise NotImplemented
    pass

@not_implemented
def ConvertEffectType(i:"integer")->"effecttype":
    raise NotImplemented
    pass

@not_implemented
def ConvertVersion(i:"integer")->"version":
    raise NotImplemented
    pass

@not_implemented
def ConvertItemType(i:"integer")->"itemtype":
    raise NotImplemented
    pass

@not_implemented
def ConvertAttackType(i:"integer")->"attacktype":
    raise NotImplemented
    pass

@not_implemented
def ConvertDamageType(i:"integer")->"damagetype":
    raise NotImplemented
    pass

@not_implemented
def ConvertWeaponType(i:"integer")->"weapontype":
    raise NotImplemented
    pass

@not_implemented
def ConvertSoundType(i:"integer")->"soundtype":
    raise NotImplemented
    pass

@not_implemented
def ConvertPathingType(i:"integer")->"pathingtype":
    raise NotImplemented
    pass

@not_implemented
def OrderId(orderIdString:"string")->"integer":
    raise NotImplemented
    pass

@not_implemented
def OrderId2String(orderId:"integer")->"string":
    raise NotImplemented
    pass

@not_implemented
def UnitId(unitIdString:"string")->"integer":
    raise NotImplemented
    pass

@not_implemented
def UnitId2String(unitId:"integer")->"string":
    raise NotImplemented
    pass

@not_implemented
def AbilityId(abilityIdString:"string")->"integer":
    raise NotImplemented
    pass

@not_implemented
def AbilityId2String(abilityId:"integer")->"string":
    raise NotImplemented
    pass

@not_implemented
def GetObjectName(objectId:"integer")->"string":
    raise NotImplemented
    pass

FALSE = False
TRUE = True
JASS_MAX_ARRAY_SIZE = 8192
PLAYER_NEUTRAL_PASSIVE = 15
PLAYER_NEUTRAL_AGGRESSIVE = 12
PLAYER_COLOR_RED = ConvertPlayerColor(0)
PLAYER_COLOR_BLUE = ConvertPlayerColor(1)
PLAYER_COLOR_CYAN = ConvertPlayerColor(2)
PLAYER_COLOR_PURPLE = ConvertPlayerColor(3)
PLAYER_COLOR_YELLOW = ConvertPlayerColor(4)
PLAYER_COLOR_ORANGE = ConvertPlayerColor(5)
PLAYER_COLOR_GREEN = ConvertPlayerColor(6)
PLAYER_COLOR_PINK = ConvertPlayerColor(7)
PLAYER_COLOR_LIGHT_GRAY = ConvertPlayerColor(8)
PLAYER_COLOR_LIGHT_BLUE = ConvertPlayerColor(9)
PLAYER_COLOR_AQUA = ConvertPlayerColor(10)
PLAYER_COLOR_BROWN = ConvertPlayerColor(11)
RACE_HUMAN = ConvertRace(1)
RACE_ORC = ConvertRace(2)
RACE_UNDEAD = ConvertRace(3)
RACE_NIGHTELF = ConvertRace(4)
RACE_DEMON = ConvertRace(5)
RACE_OTHER = ConvertRace(7)
PLAYER_GAME_RESULT_VICTORY = ConvertPlayerGameResult(0)
PLAYER_GAME_RESULT_DEFEAT = ConvertPlayerGameResult(1)
PLAYER_GAME_RESULT_TIE = ConvertPlayerGameResult(2)
PLAYER_GAME_RESULT_NEUTRAL = ConvertPlayerGameResult(3)
ALLIANCE_PASSIVE = ConvertAllianceType(0)
ALLIANCE_HELP_REQUEST = ConvertAllianceType(1)
ALLIANCE_HELP_RESPONSE = ConvertAllianceType(2)
ALLIANCE_SHARED_XP = ConvertAllianceType(3)
ALLIANCE_SHARED_SPELLS = ConvertAllianceType(4)
ALLIANCE_SHARED_VISION = ConvertAllianceType(5)
ALLIANCE_SHARED_CONTROL = ConvertAllianceType(6)
ALLIANCE_SHARED_ADVANCED_CONTROL = ConvertAllianceType(7)
ALLIANCE_RESCUABLE = ConvertAllianceType(8)
ALLIANCE_SHARED_VISION_FORCED = ConvertAllianceType(9)
VERSION_REIGN_OF_CHAOS = ConvertVersion(0)
VERSION_FROZEN_THRONE = ConvertVersion(1)
ATTACK_TYPE_NORMAL = ConvertAttackType(0)
ATTACK_TYPE_MELEE = ConvertAttackType(1)
ATTACK_TYPE_PIERCE = ConvertAttackType(2)
ATTACK_TYPE_SIEGE = ConvertAttackType(3)
ATTACK_TYPE_MAGIC = ConvertAttackType(4)
ATTACK_TYPE_CHAOS = ConvertAttackType(5)
ATTACK_TYPE_HERO = ConvertAttackType(6)
DAMAGE_TYPE_UNKNOWN = ConvertDamageType(0)
DAMAGE_TYPE_NORMAL = ConvertDamageType(4)
DAMAGE_TYPE_ENHANCED = ConvertDamageType(5)
DAMAGE_TYPE_FIRE = ConvertDamageType(8)
DAMAGE_TYPE_COLD = ConvertDamageType(9)
DAMAGE_TYPE_LIGHTNING = ConvertDamageType(10)
DAMAGE_TYPE_POISON = ConvertDamageType(11)
DAMAGE_TYPE_DISEASE = ConvertDamageType(12)
DAMAGE_TYPE_DIVINE = ConvertDamageType(13)
DAMAGE_TYPE_MAGIC = ConvertDamageType(14)
DAMAGE_TYPE_SONIC = ConvertDamageType(15)
DAMAGE_TYPE_ACID = ConvertDamageType(16)
DAMAGE_TYPE_FORCE = ConvertDamageType(17)
DAMAGE_TYPE_DEATH = ConvertDamageType(18)
DAMAGE_TYPE_MIND = ConvertDamageType(19)
DAMAGE_TYPE_PLANT = ConvertDamageType(20)
DAMAGE_TYPE_DEFENSIVE = ConvertDamageType(21)
DAMAGE_TYPE_DEMOLITION = ConvertDamageType(22)
DAMAGE_TYPE_SLOW_POISON = ConvertDamageType(23)
DAMAGE_TYPE_SPIRIT_LINK = ConvertDamageType(24)
DAMAGE_TYPE_SHADOW_STRIKE = ConvertDamageType(25)
DAMAGE_TYPE_UNIVERSAL = ConvertDamageType(26)
WEAPON_TYPE_WHOKNOWS = ConvertWeaponType(0)
WEAPON_TYPE_METAL_LIGHT_CHOP = ConvertWeaponType(1)
WEAPON_TYPE_METAL_MEDIUM_CHOP = ConvertWeaponType(2)
WEAPON_TYPE_METAL_HEAVY_CHOP = ConvertWeaponType(3)
WEAPON_TYPE_METAL_LIGHT_SLICE = ConvertWeaponType(4)
WEAPON_TYPE_METAL_MEDIUM_SLICE = ConvertWeaponType(5)
WEAPON_TYPE_METAL_HEAVY_SLICE = ConvertWeaponType(6)
WEAPON_TYPE_METAL_MEDIUM_BASH = ConvertWeaponType(7)
WEAPON_TYPE_METAL_HEAVY_BASH = ConvertWeaponType(8)
WEAPON_TYPE_METAL_MEDIUM_STAB = ConvertWeaponType(9)
WEAPON_TYPE_METAL_HEAVY_STAB = ConvertWeaponType(10)
WEAPON_TYPE_WOOD_LIGHT_SLICE = ConvertWeaponType(11)
WEAPON_TYPE_WOOD_MEDIUM_SLICE = ConvertWeaponType(12)
WEAPON_TYPE_WOOD_HEAVY_SLICE = ConvertWeaponType(13)
WEAPON_TYPE_WOOD_LIGHT_BASH = ConvertWeaponType(14)
WEAPON_TYPE_WOOD_MEDIUM_BASH = ConvertWeaponType(15)
WEAPON_TYPE_WOOD_HEAVY_BASH = ConvertWeaponType(16)
WEAPON_TYPE_WOOD_LIGHT_STAB = ConvertWeaponType(17)
WEAPON_TYPE_WOOD_MEDIUM_STAB = ConvertWeaponType(18)
WEAPON_TYPE_CLAW_LIGHT_SLICE = ConvertWeaponType(19)
WEAPON_TYPE_CLAW_MEDIUM_SLICE = ConvertWeaponType(20)
WEAPON_TYPE_CLAW_HEAVY_SLICE = ConvertWeaponType(21)
WEAPON_TYPE_AXE_MEDIUM_CHOP = ConvertWeaponType(22)
WEAPON_TYPE_ROCK_HEAVY_BASH = ConvertWeaponType(23)
PATHING_TYPE_ANY = ConvertPathingType(0)
PATHING_TYPE_WALKABILITY = ConvertPathingType(1)
PATHING_TYPE_FLYABILITY = ConvertPathingType(2)
PATHING_TYPE_BUILDABILITY = ConvertPathingType(3)
PATHING_TYPE_PEONHARVESTPATHING = ConvertPathingType(4)
PATHING_TYPE_BLIGHTPATHING = ConvertPathingType(5)
PATHING_TYPE_FLOATABILITY = ConvertPathingType(6)
PATHING_TYPE_AMPHIBIOUSPATHING = ConvertPathingType(7)
RACE_PREF_HUMAN = ConvertRacePref(1)
RACE_PREF_ORC = ConvertRacePref(2)
RACE_PREF_NIGHTELF = ConvertRacePref(4)
RACE_PREF_UNDEAD = ConvertRacePref(8)
RACE_PREF_DEMON = ConvertRacePref(16)
RACE_PREF_RANDOM = ConvertRacePref(32)
RACE_PREF_USER_SELECTABLE = ConvertRacePref(64)
MAP_CONTROL_USER = ConvertMapControl(0)
MAP_CONTROL_COMPUTER = ConvertMapControl(1)
MAP_CONTROL_RESCUABLE = ConvertMapControl(2)
MAP_CONTROL_NEUTRAL = ConvertMapControl(3)
MAP_CONTROL_CREEP = ConvertMapControl(4)
MAP_CONTROL_NONE = ConvertMapControl(5)
GAME_TYPE_MELEE = ConvertGameType(1)
GAME_TYPE_FFA = ConvertGameType(2)
GAME_TYPE_USE_MAP_SETTINGS = ConvertGameType(4)
GAME_TYPE_BLIZ = ConvertGameType(8)
GAME_TYPE_ONE_ON_ONE = ConvertGameType(16)
GAME_TYPE_TWO_TEAM_PLAY = ConvertGameType(32)
GAME_TYPE_THREE_TEAM_PLAY = ConvertGameType(64)
GAME_TYPE_FOUR_TEAM_PLAY = ConvertGameType(128)
MAP_FOG_HIDE_TERRAIN = ConvertMapFlag(1)
MAP_FOG_MAP_EXPLORED = ConvertMapFlag(2)
MAP_FOG_ALWAYS_VISIBLE = ConvertMapFlag(4)
MAP_USE_HANDICAPS = ConvertMapFlag(8)
MAP_OBSERVERS = ConvertMapFlag(16)
MAP_OBSERVERS_ON_DEATH = ConvertMapFlag(32)
MAP_FIXED_COLORS = ConvertMapFlag(128)
MAP_LOCK_RESOURCE_TRADING = ConvertMapFlag(256)
MAP_RESOURCE_TRADING_ALLIES_ONLY = ConvertMapFlag(512)
MAP_LOCK_ALLIANCE_CHANGES = ConvertMapFlag(1024)
MAP_ALLIANCE_CHANGES_HIDDEN = ConvertMapFlag(2048)
MAP_CHEATS = ConvertMapFlag(4096)
MAP_CHEATS_HIDDEN = ConvertMapFlag(8192)
MAP_LOCK_SPEED = ConvertMapFlag(8192 * 2)
MAP_LOCK_RANDOM_SEED = ConvertMapFlag(8192 * 4)
MAP_SHARED_ADVANCED_CONTROL = ConvertMapFlag(8192 * 8)
MAP_RANDOM_HERO = ConvertMapFlag(8192 * 16)
MAP_RANDOM_RACES = ConvertMapFlag(8192 * 32)
MAP_RELOADED = ConvertMapFlag(8192 * 64)
MAP_PLACEMENT_RANDOM = ConvertPlacement(0)
MAP_PLACEMENT_FIXED = ConvertPlacement(1)
MAP_PLACEMENT_USE_MAP_SETTINGS = ConvertPlacement(2)
MAP_PLACEMENT_TEAMS_TOGETHER = ConvertPlacement(3)
MAP_LOC_PRIO_LOW = ConvertStartLocPrio(0)
MAP_LOC_PRIO_HIGH = ConvertStartLocPrio(1)
MAP_LOC_PRIO_NOT = ConvertStartLocPrio(2)
MAP_DENSITY_NONE = ConvertMapDensity(0)
MAP_DENSITY_LIGHT = ConvertMapDensity(1)
MAP_DENSITY_MEDIUM = ConvertMapDensity(2)
MAP_DENSITY_HEAVY = ConvertMapDensity(3)
MAP_DIFFICULTY_EASY = ConvertGameDifficulty(0)
MAP_DIFFICULTY_NORMAL = ConvertGameDifficulty(1)
MAP_DIFFICULTY_HARD = ConvertGameDifficulty(2)
MAP_DIFFICULTY_INSANE = ConvertGameDifficulty(3)
MAP_SPEED_SLOWEST = ConvertGameSpeed(0)
MAP_SPEED_SLOW = ConvertGameSpeed(1)
MAP_SPEED_NORMAL = ConvertGameSpeed(2)
MAP_SPEED_FAST = ConvertGameSpeed(3)
MAP_SPEED_FASTEST = ConvertGameSpeed(4)
PLAYER_SLOT_STATE_EMPTY = ConvertPlayerSlotState(0)
PLAYER_SLOT_STATE_PLAYING = ConvertPlayerSlotState(1)
PLAYER_SLOT_STATE_LEFT = ConvertPlayerSlotState(2)
SOUND_VOLUMEGROUP_UNITMOVEMENT = ConvertVolumeGroup(0)
SOUND_VOLUMEGROUP_UNITSOUNDS = ConvertVolumeGroup(1)
SOUND_VOLUMEGROUP_COMBAT = ConvertVolumeGroup(2)
SOUND_VOLUMEGROUP_SPELLS = ConvertVolumeGroup(3)
SOUND_VOLUMEGROUP_UI = ConvertVolumeGroup(4)
SOUND_VOLUMEGROUP_MUSIC = ConvertVolumeGroup(5)
SOUND_VOLUMEGROUP_AMBIENTSOUNDS = ConvertVolumeGroup(6)
SOUND_VOLUMEGROUP_FIRE = ConvertVolumeGroup(7)
GAME_STATE_DIVINE_INTERVENTION = ConvertIGameState(0)
GAME_STATE_DISCONNECTED = ConvertIGameState(1)
GAME_STATE_TIME_OF_DAY = ConvertFGameState(2)
PLAYER_STATE_GAME_RESULT = ConvertPlayerState(0)
PLAYER_STATE_RESOURCE_GOLD = ConvertPlayerState(1)
PLAYER_STATE_RESOURCE_LUMBER = ConvertPlayerState(2)
PLAYER_STATE_RESOURCE_HERO_TOKENS = ConvertPlayerState(3)
PLAYER_STATE_RESOURCE_FOOD_CAP = ConvertPlayerState(4)
PLAYER_STATE_RESOURCE_FOOD_USED = ConvertPlayerState(5)
PLAYER_STATE_FOOD_CAP_CEILING = ConvertPlayerState(6)
PLAYER_STATE_GIVES_BOUNTY = ConvertPlayerState(7)
PLAYER_STATE_ALLIED_VICTORY = ConvertPlayerState(8)
PLAYER_STATE_PLACED = ConvertPlayerState(9)
PLAYER_STATE_OBSERVER_ON_DEATH = ConvertPlayerState(10)
PLAYER_STATE_OBSERVER = ConvertPlayerState(11)
PLAYER_STATE_UNFOLLOWABLE = ConvertPlayerState(12)
PLAYER_STATE_GOLD_UPKEEP_RATE = ConvertPlayerState(13)
PLAYER_STATE_LUMBER_UPKEEP_RATE = ConvertPlayerState(14)
PLAYER_STATE_GOLD_GATHERED = ConvertPlayerState(15)
PLAYER_STATE_LUMBER_GATHERED = ConvertPlayerState(16)
PLAYER_STATE_NO_CREEP_SLEEP = ConvertPlayerState(25)
UNIT_STATE_LIFE = ConvertUnitState(0)
UNIT_STATE_MAX_LIFE = ConvertUnitState(1)
UNIT_STATE_MANA = ConvertUnitState(2)
UNIT_STATE_MAX_MANA = ConvertUnitState(3)
AI_DIFFICULTY_NEWBIE = ConvertAIDifficulty(0)
AI_DIFFICULTY_NORMAL = ConvertAIDifficulty(1)
AI_DIFFICULTY_INSANE = ConvertAIDifficulty(2)
PLAYER_SCORE_UNITS_TRAINED = ConvertPlayerScore(0)
PLAYER_SCORE_UNITS_KILLED = ConvertPlayerScore(1)
PLAYER_SCORE_STRUCT_BUILT = ConvertPlayerScore(2)
PLAYER_SCORE_STRUCT_RAZED = ConvertPlayerScore(3)
PLAYER_SCORE_TECH_PERCENT = ConvertPlayerScore(4)
PLAYER_SCORE_FOOD_MAXPROD = ConvertPlayerScore(5)
PLAYER_SCORE_FOOD_MAXUSED = ConvertPlayerScore(6)
PLAYER_SCORE_HEROES_KILLED = ConvertPlayerScore(7)
PLAYER_SCORE_ITEMS_GAINED = ConvertPlayerScore(8)
PLAYER_SCORE_MERCS_HIRED = ConvertPlayerScore(9)
PLAYER_SCORE_GOLD_MINED_TOTAL = ConvertPlayerScore(10)
PLAYER_SCORE_GOLD_MINED_UPKEEP = ConvertPlayerScore(11)
PLAYER_SCORE_GOLD_LOST_UPKEEP = ConvertPlayerScore(12)
PLAYER_SCORE_GOLD_LOST_TAX = ConvertPlayerScore(13)
PLAYER_SCORE_GOLD_GIVEN = ConvertPlayerScore(14)
PLAYER_SCORE_GOLD_RECEIVED = ConvertPlayerScore(15)
PLAYER_SCORE_LUMBER_TOTAL = ConvertPlayerScore(16)
PLAYER_SCORE_LUMBER_LOST_UPKEEP = ConvertPlayerScore(17)
PLAYER_SCORE_LUMBER_LOST_TAX = ConvertPlayerScore(18)
PLAYER_SCORE_LUMBER_GIVEN = ConvertPlayerScore(19)
PLAYER_SCORE_LUMBER_RECEIVED = ConvertPlayerScore(20)
PLAYER_SCORE_UNIT_TOTAL = ConvertPlayerScore(21)
PLAYER_SCORE_HERO_TOTAL = ConvertPlayerScore(22)
PLAYER_SCORE_RESOURCE_TOTAL = ConvertPlayerScore(23)
PLAYER_SCORE_TOTAL = ConvertPlayerScore(24)
EVENT_GAME_VICTORY = ConvertGameEvent(0)
EVENT_GAME_END_LEVEL = ConvertGameEvent(1)
EVENT_GAME_VARIABLE_LIMIT = ConvertGameEvent(2)
EVENT_GAME_STATE_LIMIT = ConvertGameEvent(3)
EVENT_GAME_TIMER_EXPIRED = ConvertGameEvent(4)
EVENT_GAME_ENTER_REGION = ConvertGameEvent(5)
EVENT_GAME_LEAVE_REGION = ConvertGameEvent(6)
EVENT_GAME_TRACKABLE_HIT = ConvertGameEvent(7)
EVENT_GAME_TRACKABLE_TRACK = ConvertGameEvent(8)
EVENT_GAME_SHOW_SKILL = ConvertGameEvent(9)
EVENT_GAME_BUILD_SUBMENU = ConvertGameEvent(10)
EVENT_PLAYER_STATE_LIMIT = ConvertPlayerEvent(11)
EVENT_PLAYER_ALLIANCE_CHANGED = ConvertPlayerEvent(12)
EVENT_PLAYER_DEFEAT = ConvertPlayerEvent(13)
EVENT_PLAYER_VICTORY = ConvertPlayerEvent(14)
EVENT_PLAYER_LEAVE = ConvertPlayerEvent(15)
EVENT_PLAYER_CHAT = ConvertPlayerEvent(16)
EVENT_PLAYER_END_CINEMATIC = ConvertPlayerEvent(17)
EVENT_PLAYER_UNIT_ATTACKED = ConvertPlayerUnitEvent(18)
EVENT_PLAYER_UNIT_RESCUED = ConvertPlayerUnitEvent(19)
EVENT_PLAYER_UNIT_DEATH = ConvertPlayerUnitEvent(20)
EVENT_PLAYER_UNIT_DECAY = ConvertPlayerUnitEvent(21)
EVENT_PLAYER_UNIT_DETECTED = ConvertPlayerUnitEvent(22)
EVENT_PLAYER_UNIT_HIDDEN = ConvertPlayerUnitEvent(23)
EVENT_PLAYER_UNIT_SELECTED = ConvertPlayerUnitEvent(24)
EVENT_PLAYER_UNIT_DESELECTED = ConvertPlayerUnitEvent(25)
EVENT_PLAYER_UNIT_CONSTRUCT_START = ConvertPlayerUnitEvent(26)
EVENT_PLAYER_UNIT_CONSTRUCT_CANCEL = ConvertPlayerUnitEvent(27)
EVENT_PLAYER_UNIT_CONSTRUCT_FINISH = ConvertPlayerUnitEvent(28)
EVENT_PLAYER_UNIT_UPGRADE_START = ConvertPlayerUnitEvent(29)
EVENT_PLAYER_UNIT_UPGRADE_CANCEL = ConvertPlayerUnitEvent(30)
EVENT_PLAYER_UNIT_UPGRADE_FINISH = ConvertPlayerUnitEvent(31)
EVENT_PLAYER_UNIT_TRAIN_START = ConvertPlayerUnitEvent(32)
EVENT_PLAYER_UNIT_TRAIN_CANCEL = ConvertPlayerUnitEvent(33)
EVENT_PLAYER_UNIT_TRAIN_FINISH = ConvertPlayerUnitEvent(34)
EVENT_PLAYER_UNIT_RESEARCH_START = ConvertPlayerUnitEvent(35)
EVENT_PLAYER_UNIT_RESEARCH_CANCEL = ConvertPlayerUnitEvent(36)
EVENT_PLAYER_UNIT_RESEARCH_FINISH = ConvertPlayerUnitEvent(37)
EVENT_PLAYER_UNIT_ISSUED_ORDER = ConvertPlayerUnitEvent(38)
EVENT_PLAYER_UNIT_ISSUED_POINT_ORDER = ConvertPlayerUnitEvent(39)
EVENT_PLAYER_UNIT_ISSUED_TARGET_ORDER = ConvertPlayerUnitEvent(40)
EVENT_PLAYER_UNIT_ISSUED_UNIT_ORDER = ConvertPlayerUnitEvent(40)
EVENT_PLAYER_HERO_LEVEL = ConvertPlayerUnitEvent(41)
EVENT_PLAYER_HERO_SKILL = ConvertPlayerUnitEvent(42)
EVENT_PLAYER_HERO_REVIVABLE = ConvertPlayerUnitEvent(43)
EVENT_PLAYER_HERO_REVIVE_START = ConvertPlayerUnitEvent(44)
EVENT_PLAYER_HERO_REVIVE_CANCEL = ConvertPlayerUnitEvent(45)
EVENT_PLAYER_HERO_REVIVE_FINISH = ConvertPlayerUnitEvent(46)
EVENT_PLAYER_UNIT_SUMMON = ConvertPlayerUnitEvent(47)
EVENT_PLAYER_UNIT_DROP_ITEM = ConvertPlayerUnitEvent(48)
EVENT_PLAYER_UNIT_PICKUP_ITEM = ConvertPlayerUnitEvent(49)
EVENT_PLAYER_UNIT_USE_ITEM = ConvertPlayerUnitEvent(50)
EVENT_PLAYER_UNIT_LOADED = ConvertPlayerUnitEvent(51)
EVENT_UNIT_DAMAGED = ConvertUnitEvent(52)
EVENT_UNIT_DEATH = ConvertUnitEvent(53)
EVENT_UNIT_DECAY = ConvertUnitEvent(54)
EVENT_UNIT_DETECTED = ConvertUnitEvent(55)
EVENT_UNIT_HIDDEN = ConvertUnitEvent(56)
EVENT_UNIT_SELECTED = ConvertUnitEvent(57)
EVENT_UNIT_DESELECTED = ConvertUnitEvent(58)
EVENT_UNIT_STATE_LIMIT = ConvertUnitEvent(59)
EVENT_UNIT_ACQUIRED_TARGET = ConvertUnitEvent(60)
EVENT_UNIT_TARGET_IN_RANGE = ConvertUnitEvent(61)
EVENT_UNIT_ATTACKED = ConvertUnitEvent(62)
EVENT_UNIT_RESCUED = ConvertUnitEvent(63)
EVENT_UNIT_CONSTRUCT_CANCEL = ConvertUnitEvent(64)
EVENT_UNIT_CONSTRUCT_FINISH = ConvertUnitEvent(65)
EVENT_UNIT_UPGRADE_START = ConvertUnitEvent(66)
EVENT_UNIT_UPGRADE_CANCEL = ConvertUnitEvent(67)
EVENT_UNIT_UPGRADE_FINISH = ConvertUnitEvent(68)
EVENT_UNIT_TRAIN_START = ConvertUnitEvent(69)
EVENT_UNIT_TRAIN_CANCEL = ConvertUnitEvent(70)
EVENT_UNIT_TRAIN_FINISH = ConvertUnitEvent(71)
EVENT_UNIT_RESEARCH_START = ConvertUnitEvent(72)
EVENT_UNIT_RESEARCH_CANCEL = ConvertUnitEvent(73)
EVENT_UNIT_RESEARCH_FINISH = ConvertUnitEvent(74)
EVENT_UNIT_ISSUED_ORDER = ConvertUnitEvent(75)
EVENT_UNIT_ISSUED_POINT_ORDER = ConvertUnitEvent(76)
EVENT_UNIT_ISSUED_TARGET_ORDER = ConvertUnitEvent(77)
EVENT_UNIT_HERO_LEVEL = ConvertUnitEvent(78)
EVENT_UNIT_HERO_SKILL = ConvertUnitEvent(79)
EVENT_UNIT_HERO_REVIVABLE = ConvertUnitEvent(80)
EVENT_UNIT_HERO_REVIVE_START = ConvertUnitEvent(81)
EVENT_UNIT_HERO_REVIVE_CANCEL = ConvertUnitEvent(82)
EVENT_UNIT_HERO_REVIVE_FINISH = ConvertUnitEvent(83)
EVENT_UNIT_SUMMON = ConvertUnitEvent(84)
EVENT_UNIT_DROP_ITEM = ConvertUnitEvent(85)
EVENT_UNIT_PICKUP_ITEM = ConvertUnitEvent(86)
EVENT_UNIT_USE_ITEM = ConvertUnitEvent(87)
EVENT_UNIT_LOADED = ConvertUnitEvent(88)
EVENT_WIDGET_DEATH = ConvertWidgetEvent(89)
EVENT_DIALOG_BUTTON_CLICK = ConvertDialogEvent(90)
EVENT_DIALOG_CLICK = ConvertDialogEvent(91)
EVENT_GAME_LOADED = ConvertGameEvent(256)
EVENT_GAME_TOURNAMENT_FINISH_SOON = ConvertGameEvent(257)
EVENT_GAME_TOURNAMENT_FINISH_NOW = ConvertGameEvent(258)
EVENT_GAME_SAVE = ConvertGameEvent(259)
EVENT_PLAYER_ARROW_LEFT_DOWN = ConvertPlayerEvent(261)
EVENT_PLAYER_ARROW_LEFT_UP = ConvertPlayerEvent(262)
EVENT_PLAYER_ARROW_RIGHT_DOWN = ConvertPlayerEvent(263)
EVENT_PLAYER_ARROW_RIGHT_UP = ConvertPlayerEvent(264)
EVENT_PLAYER_ARROW_DOWN_DOWN = ConvertPlayerEvent(265)
EVENT_PLAYER_ARROW_DOWN_UP = ConvertPlayerEvent(266)
EVENT_PLAYER_ARROW_UP_DOWN = ConvertPlayerEvent(267)
EVENT_PLAYER_ARROW_UP_UP = ConvertPlayerEvent(268)
EVENT_PLAYER_UNIT_SELL = ConvertPlayerUnitEvent(269)
EVENT_PLAYER_UNIT_CHANGE_OWNER = ConvertPlayerUnitEvent(270)
EVENT_PLAYER_UNIT_SELL_ITEM = ConvertPlayerUnitEvent(271)
EVENT_PLAYER_UNIT_SPELL_CHANNEL = ConvertPlayerUnitEvent(272)
EVENT_PLAYER_UNIT_SPELL_CAST = ConvertPlayerUnitEvent(273)
EVENT_PLAYER_UNIT_SPELL_EFFECT = ConvertPlayerUnitEvent(274)
EVENT_PLAYER_UNIT_SPELL_FINISH = ConvertPlayerUnitEvent(275)
EVENT_PLAYER_UNIT_SPELL_ENDCAST = ConvertPlayerUnitEvent(276)
EVENT_PLAYER_UNIT_PAWN_ITEM = ConvertPlayerUnitEvent(277)
EVENT_UNIT_SELL = ConvertUnitEvent(286)
EVENT_UNIT_CHANGE_OWNER = ConvertUnitEvent(287)
EVENT_UNIT_SELL_ITEM = ConvertUnitEvent(288)
EVENT_UNIT_SPELL_CHANNEL = ConvertUnitEvent(289)
EVENT_UNIT_SPELL_CAST = ConvertUnitEvent(290)
EVENT_UNIT_SPELL_EFFECT = ConvertUnitEvent(291)
EVENT_UNIT_SPELL_FINISH = ConvertUnitEvent(292)
EVENT_UNIT_SPELL_ENDCAST = ConvertUnitEvent(293)
EVENT_UNIT_PAWN_ITEM = ConvertUnitEvent(294)
LESS_THAN = ConvertLimitOp(0)
LESS_THAN_OR_EQUAL = ConvertLimitOp(1)
EQUAL = ConvertLimitOp(2)
GREATER_THAN_OR_EQUAL = ConvertLimitOp(3)
GREATER_THAN = ConvertLimitOp(4)
NOT_EQUAL = ConvertLimitOp(5)
UNIT_TYPE_HERO = ConvertUnitType(0)
UNIT_TYPE_DEAD = ConvertUnitType(1)
UNIT_TYPE_STRUCTURE = ConvertUnitType(2)
UNIT_TYPE_FLYING = ConvertUnitType(3)
UNIT_TYPE_GROUND = ConvertUnitType(4)
UNIT_TYPE_ATTACKS_FLYING = ConvertUnitType(5)
UNIT_TYPE_ATTACKS_GROUND = ConvertUnitType(6)
UNIT_TYPE_MELEE_ATTACKER = ConvertUnitType(7)
UNIT_TYPE_RANGED_ATTACKER = ConvertUnitType(8)
UNIT_TYPE_GIANT = ConvertUnitType(9)
UNIT_TYPE_SUMMONED = ConvertUnitType(10)
UNIT_TYPE_STUNNED = ConvertUnitType(11)
UNIT_TYPE_PLAGUED = ConvertUnitType(12)
UNIT_TYPE_SNARED = ConvertUnitType(13)
UNIT_TYPE_UNDEAD = ConvertUnitType(14)
UNIT_TYPE_MECHANICAL = ConvertUnitType(15)
UNIT_TYPE_PEON = ConvertUnitType(16)
UNIT_TYPE_SAPPER = ConvertUnitType(17)
UNIT_TYPE_TOWNHALL = ConvertUnitType(18)
UNIT_TYPE_ANCIENT = ConvertUnitType(19)
UNIT_TYPE_TAUREN = ConvertUnitType(20)
UNIT_TYPE_POISONED = ConvertUnitType(21)
UNIT_TYPE_POLYMORPHED = ConvertUnitType(22)
UNIT_TYPE_SLEEPING = ConvertUnitType(23)
UNIT_TYPE_RESISTANT = ConvertUnitType(24)
UNIT_TYPE_ETHEREAL = ConvertUnitType(25)
UNIT_TYPE_MAGIC_IMMUNE = ConvertUnitType(26)
ITEM_TYPE_PERMANENT = ConvertItemType(0)
ITEM_TYPE_CHARGED = ConvertItemType(1)
ITEM_TYPE_POWERUP = ConvertItemType(2)
ITEM_TYPE_ARTIFACT = ConvertItemType(3)
ITEM_TYPE_PURCHASABLE = ConvertItemType(4)
ITEM_TYPE_CAMPAIGN = ConvertItemType(5)
ITEM_TYPE_MISCELLANEOUS = ConvertItemType(6)
ITEM_TYPE_UNKNOWN = ConvertItemType(7)
ITEM_TYPE_ANY = ConvertItemType(8)
ITEM_TYPE_TOME = ConvertItemType(2)
CAMERA_FIELD_TARGET_DISTANCE = ConvertCameraField(0)
CAMERA_FIELD_FARZ = ConvertCameraField(1)
CAMERA_FIELD_ANGLE_OF_ATTACK = ConvertCameraField(2)
CAMERA_FIELD_FIELD_OF_VIEW = ConvertCameraField(3)
CAMERA_FIELD_ROLL = ConvertCameraField(4)
CAMERA_FIELD_ROTATION = ConvertCameraField(5)
CAMERA_FIELD_ZOFFSET = ConvertCameraField(6)
BLEND_MODE_NONE = ConvertBlendMode(0)
BLEND_MODE_DONT_CARE = ConvertBlendMode(0)
BLEND_MODE_KEYALPHA = ConvertBlendMode(1)
BLEND_MODE_BLEND = ConvertBlendMode(2)
BLEND_MODE_ADDITIVE = ConvertBlendMode(3)
BLEND_MODE_MODULATE = ConvertBlendMode(4)
BLEND_MODE_MODULATE_2X = ConvertBlendMode(5)
RARITY_FREQUENT = ConvertRarityControl(0)
RARITY_RARE = ConvertRarityControl(1)
TEXMAP_FLAG_NONE = ConvertTexMapFlags(0)
TEXMAP_FLAG_WRAP_U = ConvertTexMapFlags(1)
TEXMAP_FLAG_WRAP_V = ConvertTexMapFlags(2)
TEXMAP_FLAG_WRAP_UV = ConvertTexMapFlags(3)
FOG_OF_WAR_MASKED = ConvertFogState(1)
FOG_OF_WAR_FOGGED = ConvertFogState(2)
FOG_OF_WAR_VISIBLE = ConvertFogState(4)
CAMERA_MARGIN_LEFT = 0
CAMERA_MARGIN_RIGHT = 1
CAMERA_MARGIN_TOP = 2
CAMERA_MARGIN_BOTTOM = 3
EFFECT_TYPE_EFFECT = ConvertEffectType(0)
EFFECT_TYPE_TARGET = ConvertEffectType(1)
EFFECT_TYPE_CASTER = ConvertEffectType(2)
EFFECT_TYPE_SPECIAL = ConvertEffectType(3)
EFFECT_TYPE_AREA_EFFECT = ConvertEffectType(4)
EFFECT_TYPE_MISSILE = ConvertEffectType(5)
EFFECT_TYPE_LIGHTNING = ConvertEffectType(6)
SOUND_TYPE_EFFECT = ConvertSoundType(0)
SOUND_TYPE_EFFECT_LOOPED = ConvertSoundType(1)

@not_implemented
def Deg2Rad(degrees:"real")->"real":
    raise NotImplemented
    pass

@not_implemented
def Rad2Deg(radians:"real")->"real":
    raise NotImplemented
    pass

@not_implemented
def Sin(radians:"real")->"real":
    raise NotImplemented
    pass

@not_implemented
def Cos(radians:"real")->"real":
    raise NotImplemented
    pass

@not_implemented
def Tan(radians:"real")->"real":
    raise NotImplemented
    pass

@not_implemented
def Asin(y:"real")->"real":
    raise NotImplemented
    pass

@not_implemented
def Acos(x:"real")->"real":
    raise NotImplemented
    pass

@not_implemented
def Atan(x:"real")->"real":
    raise NotImplemented
    pass

@not_implemented
def Atan2(y:"real", x:"real")->"real":
    raise NotImplemented
    pass

@not_implemented
def SquareRoot(x:"real")->"real":
    raise NotImplemented
    pass

@not_implemented
def Pow(x:"real", power:"real")->"real":
    raise NotImplemented
    pass

@not_implemented
def I2R(i:"integer")->"real":
    raise NotImplemented
    pass

@not_implemented
def R2I(r:"real")->"integer":
    raise NotImplemented
    pass

@not_implemented
def I2S(i:"integer")->"string":
    raise NotImplemented
    pass

@not_implemented
def R2S(r:"real")->"string":
    raise NotImplemented
    pass

@not_implemented
def R2SW(r:"real", width:"integer", precision:"integer")->"string":
    raise NotImplemented
    pass

@not_implemented
def S2I(s:"string")->"integer":
    raise NotImplemented
    pass

@not_implemented
def S2R(s:"string")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetHandleId(h:"handle")->"integer":
    raise NotImplemented
    pass

@not_implemented
def SubString(source:"string", start:"integer", end:"integer")->"string":
    raise NotImplemented
    pass

@not_implemented
def StringLength(s:"string")->"integer":
    raise NotImplemented
    pass

@not_implemented
def StringCase(source:"string", upper:"boolean")->"string":
    raise NotImplemented
    pass

@not_implemented
def StringHash(s:"string")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetLocalizedString(source:"string")->"string":
    raise NotImplemented
    pass

@not_implemented
def GetLocalizedHotkey(source:"string")->"integer":
    raise NotImplemented
    pass

@not_implemented
def SetMapName(name:"string")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetMapDescription(description:"string")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetTeams(teamcount:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetPlayers(playercount:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def DefineStartLocation(whichStartLoc:"integer", x:"real", y:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def DefineStartLocationLoc(whichStartLoc:"integer", whichLocation:"location")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetStartLocPrioCount(whichStartLoc:"integer", prioSlotCount:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetStartLocPrio(whichStartLoc:"integer", prioSlotIndex:"integer", otherStartLocIndex:"integer", priority:"startlocprio")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetStartLocPrioSlot(whichStartLoc:"integer", prioSlotIndex:"integer")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetStartLocPrio(whichStartLoc:"integer", prioSlotIndex:"integer")->"startlocprio":
    raise NotImplemented
    pass

@not_implemented
def SetGameTypeSupported(whichGameType:"gametype", value:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetMapFlag(whichMapFlag:"mapflag", value:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetGamePlacement(whichPlacementType:"placement")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetGameSpeed(whichspeed:"gamespeed")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetGameDifficulty(whichdifficulty:"gamedifficulty")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetResourceDensity(whichdensity:"mapdensity")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetCreatureDensity(whichdensity:"mapdensity")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetTeams()->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetPlayers()->"integer":
    raise NotImplemented
    pass

@not_implemented
def IsGameTypeSupported(whichGameType:"gametype")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GetGameTypeSelected()->"gametype":
    raise NotImplemented
    pass

@not_implemented
def IsMapFlagSet(whichMapFlag:"mapflag")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GetGamePlacement()->"placement":
    raise NotImplemented
    pass

@not_implemented
def GetGameSpeed()->"gamespeed":
    raise NotImplemented
    pass

@not_implemented
def GetGameDifficulty()->"gamedifficulty":
    raise NotImplemented
    pass

@not_implemented
def GetResourceDensity()->"mapdensity":
    raise NotImplemented
    pass

@not_implemented
def GetCreatureDensity()->"mapdensity":
    raise NotImplemented
    pass

@not_implemented
def GetStartLocationX(whichStartLocation:"integer")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetStartLocationY(whichStartLocation:"integer")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetStartLocationLoc(whichStartLocation:"integer")->"location":
    raise NotImplemented
    pass

@not_implemented
def SetPlayerTeam(whichPlayer:"player", whichTeam:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetPlayerStartLocation(whichPlayer:"player", startLocIndex:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ForcePlayerStartLocation(whichPlayer:"player", startLocIndex:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetPlayerColor(whichPlayer:"player", color:"playercolor")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetPlayerAlliance(sourcePlayer:"player", otherPlayer:"player", whichAllianceSetting:"alliancetype", value:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetPlayerTaxRate(sourcePlayer:"player", otherPlayer:"player", whichResource:"playerstate", rate:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetPlayerRacePreference(whichPlayer:"player", whichRacePreference:"racepreference")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetPlayerRaceSelectable(whichPlayer:"player", value:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetPlayerController(whichPlayer:"player", controlType:"mapcontrol")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetPlayerName(whichPlayer:"player", name:"string")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetPlayerOnScoreScreen(whichPlayer:"player", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetPlayerTeam(whichPlayer:"player")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetPlayerStartLocation(whichPlayer:"player")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetPlayerColor(whichPlayer:"player")->"playercolor":
    raise NotImplemented
    pass

@not_implemented
def GetPlayerSelectable(whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GetPlayerController(whichPlayer:"player")->"mapcontrol":
    raise NotImplemented
    pass

@not_implemented
def GetPlayerSlotState(whichPlayer:"player")->"playerslotstate":
    raise NotImplemented
    pass

@not_implemented
def GetPlayerTaxRate(sourcePlayer:"player", otherPlayer:"player", whichResource:"playerstate")->"integer":
    raise NotImplemented
    pass

@not_implemented
def IsPlayerRacePrefSet(whichPlayer:"player", pref:"racepreference")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GetPlayerName(whichPlayer:"player")->"string":
    raise NotImplemented
    pass

@not_implemented
def CreateTimer()->"timer":
    raise NotImplemented
    pass

@not_implemented
def DestroyTimer(whichTimer:"timer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def TimerStart(whichTimer:"timer", timeout:"real", periodic:"boolean", handlerFunc:"code")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def TimerGetElapsed(whichTimer:"timer")->"real":
    raise NotImplemented
    pass

@not_implemented
def TimerGetRemaining(whichTimer:"timer")->"real":
    raise NotImplemented
    pass

@not_implemented
def TimerGetTimeout(whichTimer:"timer")->"real":
    raise NotImplemented
    pass

@not_implemented
def PauseTimer(whichTimer:"timer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ResumeTimer(whichTimer:"timer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetExpiredTimer()->"timer":
    raise NotImplemented
    pass

@not_implemented
def CreateGroup()->"group":
    raise NotImplemented
    pass

@not_implemented
def DestroyGroup(whichGroup:"group")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GroupAddUnit(whichGroup:"group", whichUnit:"unit")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GroupRemoveUnit(whichGroup:"group", whichUnit:"unit")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GroupClear(whichGroup:"group")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GroupEnumUnitsOfType(whichGroup:"group", unitname:"string", filter:"boolexpr")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GroupEnumUnitsOfPlayer(whichGroup:"group", whichPlayer:"player", filter:"boolexpr")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GroupEnumUnitsOfTypeCounted(whichGroup:"group", unitname:"string", filter:"boolexpr", countLimit:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GroupEnumUnitsInRect(whichGroup:"group", r:"rect", filter:"boolexpr")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GroupEnumUnitsInRectCounted(whichGroup:"group", r:"rect", filter:"boolexpr", countLimit:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GroupEnumUnitsInRange(whichGroup:"group", x:"real", y:"real", radius:"real", filter:"boolexpr")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GroupEnumUnitsInRangeOfLoc(whichGroup:"group", whichLocation:"location", radius:"real", filter:"boolexpr")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GroupEnumUnitsInRangeCounted(whichGroup:"group", x:"real", y:"real", radius:"real", filter:"boolexpr", countLimit:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GroupEnumUnitsInRangeOfLocCounted(whichGroup:"group", whichLocation:"location", radius:"real", filter:"boolexpr", countLimit:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GroupEnumUnitsSelected(whichGroup:"group", whichPlayer:"player", filter:"boolexpr")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GroupImmediateOrder(whichGroup:"group", order:"string")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GroupImmediateOrderById(whichGroup:"group", order:"integer")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GroupPointOrder(whichGroup:"group", order:"string", x:"real", y:"real")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GroupPointOrderLoc(whichGroup:"group", order:"string", whichLocation:"location")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GroupPointOrderById(whichGroup:"group", order:"integer", x:"real", y:"real")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GroupPointOrderByIdLoc(whichGroup:"group", order:"integer", whichLocation:"location")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GroupTargetOrder(whichGroup:"group", order:"string", targetWidget:"widget")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GroupTargetOrderById(whichGroup:"group", order:"integer", targetWidget:"widget")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def ForGroup(whichGroup:"group", callback:"code")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def FirstOfGroup(whichGroup:"group")->"unit":
    raise NotImplemented
    pass

@not_implemented
def CreateForce()->"force":
    raise NotImplemented
    pass

@not_implemented
def DestroyForce(whichForce:"force")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ForceAddPlayer(whichForce:"force", whichPlayer:"player")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ForceRemovePlayer(whichForce:"force", whichPlayer:"player")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ForceClear(whichForce:"force")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ForceEnumPlayers(whichForce:"force", filter:"boolexpr")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ForceEnumPlayersCounted(whichForce:"force", filter:"boolexpr", countLimit:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ForceEnumAllies(whichForce:"force", whichPlayer:"player", filter:"boolexpr")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ForceEnumEnemies(whichForce:"force", whichPlayer:"player", filter:"boolexpr")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ForForce(whichForce:"force", callback:"code")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def Rect(minx:"real", miny:"real", maxx:"real", maxy:"real")->"rect":
    raise NotImplemented
    pass

@not_implemented
def RectFromLoc(min:"location", max:"location")->"rect":
    raise NotImplemented
    pass

@not_implemented
def RemoveRect(whichRect:"rect")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetRect(whichRect:"rect", minx:"real", miny:"real", maxx:"real", maxy:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetRectFromLoc(whichRect:"rect", min:"location", max:"location")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def MoveRectTo(whichRect:"rect", newCenterX:"real", newCenterY:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def MoveRectToLoc(whichRect:"rect", newCenterLoc:"location")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetRectCenterX(whichRect:"rect")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetRectCenterY(whichRect:"rect")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetRectMinX(whichRect:"rect")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetRectMinY(whichRect:"rect")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetRectMaxX(whichRect:"rect")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetRectMaxY(whichRect:"rect")->"real":
    raise NotImplemented
    pass

@not_implemented
def CreateRegion()->"region":
    raise NotImplemented
    pass

@not_implemented
def RemoveRegion(whichRegion:"region")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def RegionAddRect(whichRegion:"region", r:"rect")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def RegionClearRect(whichRegion:"region", r:"rect")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def RegionAddCell(whichRegion:"region", x:"real", y:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def RegionAddCellAtLoc(whichRegion:"region", whichLocation:"location")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def RegionClearCell(whichRegion:"region", x:"real", y:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def RegionClearCellAtLoc(whichRegion:"region", whichLocation:"location")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def Location(x:"real", y:"real")->"location":
    raise NotImplemented
    pass

@not_implemented
def RemoveLocation(whichLocation:"location")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def MoveLocation(whichLocation:"location", newX:"real", newY:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetLocationX(whichLocation:"location")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetLocationY(whichLocation:"location")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetLocationZ(whichLocation:"location")->"real":
    raise NotImplemented
    pass

@not_implemented
def IsUnitInRegion(whichRegion:"region", whichUnit:"unit")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsPointInRegion(whichRegion:"region", x:"real", y:"real")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsLocationInRegion(whichRegion:"region", whichLocation:"location")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GetWorldBounds()->"rect":
    raise NotImplemented
    pass

@not_implemented
def CreateTrigger()->"trigger":
    raise NotImplemented
    pass

@not_implemented
def DestroyTrigger(whichTrigger:"trigger")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ResetTrigger(whichTrigger:"trigger")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def EnableTrigger(whichTrigger:"trigger")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def DisableTrigger(whichTrigger:"trigger")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def IsTriggerEnabled(whichTrigger:"trigger")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def TriggerWaitOnSleeps(whichTrigger:"trigger", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def IsTriggerWaitOnSleeps(whichTrigger:"trigger")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GetFilterUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetEnumUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetFilterDestructable()->"destructable":
    raise NotImplemented
    pass

@not_implemented
def GetEnumDestructable()->"destructable":
    raise NotImplemented
    pass

@not_implemented
def GetFilterItem()->"item":
    raise NotImplemented
    pass

@not_implemented
def GetEnumItem()->"item":
    raise NotImplemented
    pass

@not_implemented
def GetFilterPlayer()->"player":
    raise NotImplemented
    pass

@not_implemented
def GetEnumPlayer()->"player":
    raise NotImplemented
    pass

@not_implemented
def GetTriggeringTrigger()->"trigger":
    raise NotImplemented
    pass

@not_implemented
def GetTriggerEventId()->"eventid":
    raise NotImplemented
    pass

@not_implemented
def GetTriggerEvalCount(whichTrigger:"trigger")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetTriggerExecCount(whichTrigger:"trigger")->"integer":
    raise NotImplemented
    pass

@not_implemented
def ExecuteFunc(funcName:"string")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def And(operandA:"boolexpr", operandB:"boolexpr")->"boolexpr":
    raise NotImplemented
    pass

@not_implemented
def Or(operandA:"boolexpr", operandB:"boolexpr")->"boolexpr":
    raise NotImplemented
    pass

@not_implemented
def Not(operand:"boolexpr")->"boolexpr":
    raise NotImplemented
    pass

@not_implemented
def Condition(func:"code")->"conditionfunc":
    raise NotImplemented
    pass

@not_implemented
def DestroyCondition(c:"conditionfunc")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def Filter(func:"code")->"filterfunc":
    raise NotImplemented
    pass

@not_implemented
def DestroyFilter(f:"filterfunc")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def DestroyBoolExpr(e:"boolexpr")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterVariableEvent(whichTrigger:"trigger", varName:"string", opcode:"limitop", limitval:"real")->"event":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterTimerEvent(whichTrigger:"trigger", timeout:"real", periodic:"boolean")->"event":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterTimerExpireEvent(whichTrigger:"trigger", t:"timer")->"event":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterGameStateEvent(whichTrigger:"trigger", whichState:"gamestate", opcode:"limitop", limitval:"real")->"event":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterDialogEvent(whichTrigger:"trigger", whichDialog:"dialog")->"event":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterDialogButtonEvent(whichTrigger:"trigger", whichButton:"button")->"event":
    raise NotImplemented
    pass

@not_implemented
def GetEventGameState()->"gamestate":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterGameEvent(whichTrigger:"trigger", whichGameEvent:"gameevent")->"event":
    raise NotImplemented
    pass

@not_implemented
def GetWinningPlayer()->"player":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterEnterRegion(whichTrigger:"trigger", whichRegion:"region", filter:"boolexpr")->"event":
    raise NotImplemented
    pass

@not_implemented
def GetTriggeringRegion()->"region":
    raise NotImplemented
    pass

@not_implemented
def GetEnteringUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterLeaveRegion(whichTrigger:"trigger", whichRegion:"region", filter:"boolexpr")->"event":
    raise NotImplemented
    pass

@not_implemented
def GetLeavingUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterTrackableHitEvent(whichTrigger:"trigger", t:"trackable")->"event":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterTrackableTrackEvent(whichTrigger:"trigger", t:"trackable")->"event":
    raise NotImplemented
    pass

@not_implemented
def GetTriggeringTrackable()->"trackable":
    raise NotImplemented
    pass

@not_implemented
def GetClickedButton()->"button":
    raise NotImplemented
    pass

@not_implemented
def GetClickedDialog()->"dialog":
    raise NotImplemented
    pass

@not_implemented
def GetTournamentFinishSoonTimeRemaining()->"real":
    raise NotImplemented
    pass

@not_implemented
def GetTournamentFinishNowRule()->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetTournamentFinishNowPlayer()->"player":
    raise NotImplemented
    pass

@not_implemented
def GetTournamentScore(whichPlayer:"player")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetSaveBasicFilename()->"string":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterPlayerEvent(whichTrigger:"trigger", whichPlayer:"player", whichPlayerEvent:"playerevent")->"event":
    raise NotImplemented
    pass

@not_implemented
def GetTriggerPlayer()->"player":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterPlayerUnitEvent(whichTrigger:"trigger", whichPlayer:"player", whichPlayerUnitEvent:"playerunitevent", filter:"boolexpr")->"event":
    raise NotImplemented
    pass

@not_implemented
def GetLevelingUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetLearningUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetLearnedSkill()->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetLearnedSkillLevel()->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetRevivableUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetRevivingUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetAttacker()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetRescuer()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetDyingUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetKillingUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetDecayingUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetConstructingStructure()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetCancelledStructure()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetConstructedStructure()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetResearchingUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetResearched()->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetTrainedUnitType()->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetTrainedUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetDetectedUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetSummoningUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetSummonedUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetTransportUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetLoadedUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetSellingUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetSoldUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetBuyingUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetSoldItem()->"item":
    raise NotImplemented
    pass

@not_implemented
def GetChangingUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetChangingUnitPrevOwner()->"player":
    raise NotImplemented
    pass

@not_implemented
def GetManipulatingUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetManipulatedItem()->"item":
    raise NotImplemented
    pass

@not_implemented
def GetOrderedUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetIssuedOrderId()->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetOrderPointX()->"real":
    raise NotImplemented
    pass

@not_implemented
def GetOrderPointY()->"real":
    raise NotImplemented
    pass

@not_implemented
def GetOrderPointLoc()->"location":
    raise NotImplemented
    pass

@not_implemented
def GetOrderTarget()->"widget":
    raise NotImplemented
    pass

@not_implemented
def GetOrderTargetDestructable()->"destructable":
    raise NotImplemented
    pass

@not_implemented
def GetOrderTargetItem()->"item":
    raise NotImplemented
    pass

@not_implemented
def GetOrderTargetUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetSpellAbilityUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetSpellAbilityId()->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetSpellAbility()->"ability":
    raise NotImplemented
    pass

@not_implemented
def GetSpellTargetLoc()->"location":
    raise NotImplemented
    pass

@not_implemented
def GetSpellTargetX()->"real":
    raise NotImplemented
    pass

@not_implemented
def GetSpellTargetY()->"real":
    raise NotImplemented
    pass

@not_implemented
def GetSpellTargetDestructable()->"destructable":
    raise NotImplemented
    pass

@not_implemented
def GetSpellTargetItem()->"item":
    raise NotImplemented
    pass

@not_implemented
def GetSpellTargetUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterPlayerAllianceChange(whichTrigger:"trigger", whichPlayer:"player", whichAlliance:"alliancetype")->"event":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterPlayerStateEvent(whichTrigger:"trigger", whichPlayer:"player", whichState:"playerstate", opcode:"limitop", limitval:"real")->"event":
    raise NotImplemented
    pass

@not_implemented
def GetEventPlayerState()->"playerstate":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterPlayerChatEvent(whichTrigger:"trigger", whichPlayer:"player", chatMessageToDetect:"string", exactMatchOnly:"boolean")->"event":
    raise NotImplemented
    pass

@not_implemented
def GetEventPlayerChatString()->"string":
    raise NotImplemented
    pass

@not_implemented
def GetEventPlayerChatStringMatched()->"string":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterDeathEvent(whichTrigger:"trigger", whichWidget:"widget")->"event":
    raise NotImplemented
    pass

@not_implemented
def GetTriggerUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterUnitStateEvent(whichTrigger:"trigger", whichUnit:"unit", whichState:"unitstate", opcode:"limitop", limitval:"real")->"event":
    raise NotImplemented
    pass

@not_implemented
def GetEventUnitState()->"unitstate":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterUnitEvent(whichTrigger:"trigger", whichUnit:"unit", whichEvent:"unitevent")->"event":
    raise NotImplemented
    pass

@not_implemented
def GetEventDamage()->"real":
    raise NotImplemented
    pass

@not_implemented
def GetEventDamageSource()->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetEventDetectingPlayer()->"player":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterFilterUnitEvent(whichTrigger:"trigger", whichUnit:"unit", whichEvent:"unitevent", filter:"boolexpr")->"event":
    raise NotImplemented
    pass

@not_implemented
def GetEventTargetUnit()->"unit":
    raise NotImplemented
    pass

@not_implemented
def TriggerRegisterUnitInRange(whichTrigger:"trigger", whichUnit:"unit", range:"real", filter:"boolexpr")->"event":
    raise NotImplemented
    pass

@not_implemented
def TriggerAddCondition(whichTrigger:"trigger", condition:"boolexpr")->"triggercondition":
    raise NotImplemented
    pass

@not_implemented
def TriggerRemoveCondition(whichTrigger:"trigger", whichCondition:"triggercondition")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def TriggerClearConditions(whichTrigger:"trigger")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def TriggerAddAction(whichTrigger:"trigger", actionFunc:"code")->"triggeraction":
    raise NotImplemented
    pass

@not_implemented
def TriggerRemoveAction(whichTrigger:"trigger", whichAction:"triggeraction")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def TriggerClearActions(whichTrigger:"trigger")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def TriggerSleepAction(timeout:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def TriggerWaitForSound(s:"sound", offset:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def TriggerEvaluate(whichTrigger:"trigger")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def TriggerExecute(whichTrigger:"trigger")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def TriggerExecuteWait(whichTrigger:"trigger")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def TriggerSyncStart()->"nothing":
    raise NotImplemented
    pass

@not_implemented
def TriggerSyncReady()->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetWidgetLife(whichWidget:"widget")->"real":
    raise NotImplemented
    pass

@not_implemented
def SetWidgetLife(whichWidget:"widget", newLife:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetWidgetX(whichWidget:"widget")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetWidgetY(whichWidget:"widget")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetTriggerWidget()->"widget":
    raise NotImplemented
    pass

@not_implemented
def CreateDestructable(objectid:"integer", x:"real", y:"real", face:"real", scale:"real", variation:"integer")->"destructable":
    raise NotImplemented
    pass

@not_implemented
def CreateDestructableZ(objectid:"integer", x:"real", y:"real", z:"real", face:"real", scale:"real", variation:"integer")->"destructable":
    raise NotImplemented
    pass

@not_implemented
def CreateDeadDestructable(objectid:"integer", x:"real", y:"real", face:"real", scale:"real", variation:"integer")->"destructable":
    raise NotImplemented
    pass

@not_implemented
def CreateDeadDestructableZ(objectid:"integer", x:"real", y:"real", z:"real", face:"real", scale:"real", variation:"integer")->"destructable":
    raise NotImplemented
    pass

@not_implemented
def RemoveDestructable(d:"destructable")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def KillDestructable(d:"destructable")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetDestructableInvulnerable(d:"destructable", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def IsDestructableInvulnerable(d:"destructable")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def EnumDestructablesInRect(r:"rect", filter:"boolexpr", actionFunc:"code")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetDestructableTypeId(d:"destructable")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetDestructableX(d:"destructable")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetDestructableY(d:"destructable")->"real":
    raise NotImplemented
    pass

@not_implemented
def SetDestructableLife(d:"destructable", life:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetDestructableLife(d:"destructable")->"real":
    raise NotImplemented
    pass

@not_implemented
def SetDestructableMaxLife(d:"destructable", max:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetDestructableMaxLife(d:"destructable")->"real":
    raise NotImplemented
    pass

@not_implemented
def DestructableRestoreLife(d:"destructable", life:"real", birth:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def QueueDestructableAnimation(d:"destructable", whichAnimation:"string")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetDestructableAnimation(d:"destructable", whichAnimation:"string")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetDestructableAnimationSpeed(d:"destructable", speedFactor:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ShowDestructable(d:"destructable", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetDestructableOccluderHeight(d:"destructable")->"real":
    raise NotImplemented
    pass

@not_implemented
def SetDestructableOccluderHeight(d:"destructable", height:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetDestructableName(d:"destructable")->"string":
    raise NotImplemented
    pass

@not_implemented
def GetTriggerDestructable()->"destructable":
    raise NotImplemented
    pass

@not_implemented
def CreateItem(itemid:"integer", x:"real", y:"real")->"item":
    raise NotImplemented
    pass

@not_implemented
def RemoveItem(whichItem:"item")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetItemPlayer(whichItem:"item")->"player":
    raise NotImplemented
    pass

@not_implemented
def GetItemTypeId(i:"item")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetItemX(i:"item")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetItemY(i:"item")->"real":
    raise NotImplemented
    pass

@not_implemented
def SetItemPosition(i:"item", x:"real", y:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetItemDropOnDeath(whichItem:"item", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetItemDroppable(i:"item", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetItemPawnable(i:"item", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetItemPlayer(whichItem:"item", whichPlayer:"player", changeColor:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetItemInvulnerable(whichItem:"item", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def IsItemInvulnerable(whichItem:"item")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def SetItemVisible(whichItem:"item", show:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def IsItemVisible(whichItem:"item")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsItemOwned(whichItem:"item")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsItemPowerup(whichItem:"item")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsItemSellable(whichItem:"item")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsItemPawnable(whichItem:"item")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsItemIdPowerup(itemId:"integer")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsItemIdSellable(itemId:"integer")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsItemIdPawnable(itemId:"integer")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def EnumItemsInRect(r:"rect", filter:"boolexpr", actionFunc:"code")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetItemLevel(whichItem:"item")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetItemType(whichItem:"item")->"itemtype":
    raise NotImplemented
    pass

@not_implemented
def SetItemDropID(whichItem:"item", unitId:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetItemName(whichItem:"item")->"string":
    raise NotImplemented
    pass

@not_implemented
def GetItemCharges(whichItem:"item")->"integer":
    raise NotImplemented
    pass

@not_implemented
def SetItemCharges(whichItem:"item", charges:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetItemUserData(whichItem:"item")->"integer":
    raise NotImplemented
    pass

@not_implemented
def SetItemUserData(whichItem:"item", data:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def CreateUnit(id:"player", unitid:"integer", x:"real", y:"real", face:"real")->"unit":
    raise NotImplemented
    pass

@not_implemented
def CreateUnitByName(whichPlayer:"player", unitname:"string", x:"real", y:"real", face:"real")->"unit":
    raise NotImplemented
    pass

@not_implemented
def CreateUnitAtLoc(id:"player", unitid:"integer", whichLocation:"location", face:"real")->"unit":
    raise NotImplemented
    pass

@not_implemented
def CreateUnitAtLocByName(id:"player", unitname:"string", whichLocation:"location", face:"real")->"unit":
    raise NotImplemented
    pass

@not_implemented
def CreateCorpse(whichPlayer:"player", unitid:"integer", x:"real", y:"real", face:"real")->"unit":
    raise NotImplemented
    pass

@not_implemented
def KillUnit(whichUnit:"unit")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def RemoveUnit(whichUnit:"unit")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ShowUnit(whichUnit:"unit", show:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitState(whichUnit:"unit", whichUnitState:"unitstate", newVal:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitX(whichUnit:"unit", newX:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitY(whichUnit:"unit", newY:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitPosition(whichUnit:"unit", newX:"real", newY:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitPositionLoc(whichUnit:"unit", whichLocation:"location")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitFacing(whichUnit:"unit", facingAngle:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitFacingTimed(whichUnit:"unit", facingAngle:"real", duration:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitMoveSpeed(whichUnit:"unit", newSpeed:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitFlyHeight(whichUnit:"unit", newHeight:"real", rate:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitTurnSpeed(whichUnit:"unit", newTurnSpeed:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitPropWindow(whichUnit:"unit", newPropWindowAngle:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitAcquireRange(whichUnit:"unit", newAcquireRange:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitCreepGuard(whichUnit:"unit", creepGuard:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetUnitAcquireRange(whichUnit:"unit")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetUnitTurnSpeed(whichUnit:"unit")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetUnitPropWindow(whichUnit:"unit")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetUnitFlyHeight(whichUnit:"unit")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetUnitDefaultAcquireRange(whichUnit:"unit")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetUnitDefaultTurnSpeed(whichUnit:"unit")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetUnitDefaultPropWindow(whichUnit:"unit")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetUnitDefaultFlyHeight(whichUnit:"unit")->"real":
    raise NotImplemented
    pass

@not_implemented
def SetUnitOwner(whichUnit:"unit", whichPlayer:"player", changeColor:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitColor(whichUnit:"unit", whichColor:"playercolor")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitScale(whichUnit:"unit", scaleX:"real", scaleY:"real", scaleZ:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitTimeScale(whichUnit:"unit", timeScale:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitBlendTime(whichUnit:"unit", blendTime:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitVertexColor(whichUnit:"unit", red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def QueueUnitAnimation(whichUnit:"unit", whichAnimation:"string")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitAnimation(whichUnit:"unit", whichAnimation:"string")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitAnimationByIndex(whichUnit:"unit", whichAnimation:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitAnimationWithRarity(whichUnit:"unit", whichAnimation:"string", rarity:"raritycontrol")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def AddUnitAnimationProperties(whichUnit:"unit", animProperties:"string", add:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitLookAt(whichUnit:"unit", whichBone:"string", lookAtTarget:"unit", offsetX:"real", offsetY:"real", offsetZ:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ResetUnitLookAt(whichUnit:"unit")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitRescuable(whichUnit:"unit", byWhichPlayer:"player", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitRescueRange(whichUnit:"unit", range:"real")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetHeroStr(whichHero:"unit", newStr:"integer", permanent:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetHeroAgi(whichHero:"unit", newAgi:"integer", permanent:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetHeroInt(whichHero:"unit", newInt:"integer", permanent:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetHeroStr(whichHero:"unit", includeBonuses:"boolean")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetHeroAgi(whichHero:"unit", includeBonuses:"boolean")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetHeroInt(whichHero:"unit", includeBonuses:"boolean")->"integer":
    raise NotImplemented
    pass

@not_implemented
def UnitStripHeroLevel(whichHero:"unit", howManyLevels:"integer")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GetHeroXP(whichHero:"unit")->"integer":
    raise NotImplemented
    pass

@not_implemented
def SetHeroXP(whichHero:"unit", newXpVal:"integer", showEyeCandy:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetHeroSkillPoints(whichHero:"unit")->"integer":
    raise NotImplemented
    pass

@not_implemented
def UnitModifySkillPoints(whichHero:"unit", skillPointDelta:"integer")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def AddHeroXP(whichHero:"unit", xpToAdd:"integer", showEyeCandy:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetHeroLevel(whichHero:"unit", level:"integer", showEyeCandy:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetHeroLevel(whichHero:"unit")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetUnitLevel(whichUnit:"unit")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetHeroProperName(whichHero:"unit")->"string":
    raise NotImplemented
    pass

@not_implemented
def SuspendHeroXP(whichHero:"unit", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def IsSuspendedXP(whichHero:"unit")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def SelectHeroSkill(whichHero:"unit", abilcode:"integer")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetUnitAbilityLevel(whichUnit:"unit", abilcode:"integer")->"integer":
    raise NotImplemented
    pass

@not_implemented
def DecUnitAbilityLevel(whichUnit:"unit", abilcode:"integer")->"integer":
    raise NotImplemented
    pass

@not_implemented
def IncUnitAbilityLevel(whichUnit:"unit", abilcode:"integer")->"integer":
    raise NotImplemented
    pass

@not_implemented
def SetUnitAbilityLevel(whichUnit:"unit", abilcode:"integer", level:"integer")->"integer":
    raise NotImplemented
    pass

@not_implemented
def ReviveHero(whichHero:"unit", x:"real", y:"real", doEyecandy:"boolean")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def ReviveHeroLoc(whichHero:"unit", loc:"location", doEyecandy:"boolean")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def SetUnitExploded(whichUnit:"unit", exploded:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SetUnitInvulnerable(whichUnit:"unit", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def PauseUnit(whichUnit:"unit", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def IsUnitPaused(whichHero:"unit")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def SetUnitPathing(whichUnit:"unit", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def ClearSelection()->"nothing":
    raise NotImplemented
    pass

@not_implemented
def SelectUnit(whichUnit:"unit", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetUnitPointValue(whichUnit:"unit")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetUnitPointValueByType(unitType:"integer")->"integer":
    raise NotImplemented
    pass

@not_implemented
def UnitAddItem(whichUnit:"unit", whichItem:"item")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitAddItemById(whichUnit:"unit", itemId:"integer")->"item":
    raise NotImplemented
    pass

@not_implemented
def UnitAddItemToSlotById(whichUnit:"unit", itemId:"integer", itemSlot:"integer")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitRemoveItem(whichUnit:"unit", whichItem:"item")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def UnitRemoveItemFromSlot(whichUnit:"unit", itemSlot:"integer")->"item":
    raise NotImplemented
    pass

@not_implemented
def UnitHasItem(whichUnit:"unit", whichItem:"item")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitItemInSlot(whichUnit:"unit", itemSlot:"integer")->"item":
    raise NotImplemented
    pass

@not_implemented
def UnitInventorySize(whichUnit:"unit")->"integer":
    raise NotImplemented
    pass

@not_implemented
def UnitDropItemPoint(whichUnit:"unit", whichItem:"item", x:"real", y:"real")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitDropItemSlot(whichUnit:"unit", whichItem:"item", slot:"integer")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitDropItemTarget(whichUnit:"unit", whichItem:"item", target:"widget")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitUseItem(whichUnit:"unit", whichItem:"item")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitUseItemPoint(whichUnit:"unit", whichItem:"item", x:"real", y:"real")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitUseItemTarget(whichUnit:"unit", whichItem:"item", target:"widget")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def GetUnitX(whichUnit:"unit")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetUnitY(whichUnit:"unit")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetUnitLoc(whichUnit:"unit")->"location":
    raise NotImplemented
    pass

@not_implemented
def GetUnitFacing(whichUnit:"unit")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetUnitMoveSpeed(whichUnit:"unit")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetUnitDefaultMoveSpeed(whichUnit:"unit")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetUnitState(whichUnit:"unit", whichUnitState:"unitstate")->"real":
    raise NotImplemented
    pass

@not_implemented
def GetOwningPlayer(whichUnit:"unit")->"player":
    raise NotImplemented
    pass

@not_implemented
def GetUnitTypeId(whichUnit:"unit")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetUnitRace(whichUnit:"unit")->"race":
    raise NotImplemented
    pass

@not_implemented
def GetUnitName(whichUnit:"unit")->"string":
    raise NotImplemented
    pass

@not_implemented
def GetUnitFoodUsed(whichUnit:"unit")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetUnitFoodMade(whichUnit:"unit")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetFoodMade(unitId:"integer")->"integer":
    raise NotImplemented
    pass

@not_implemented
def GetFoodUsed(unitId:"integer")->"integer":
    raise NotImplemented
    pass

@not_implemented
def SetUnitUseFood(whichUnit:"unit", useFood:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def GetUnitRallyPoint(whichUnit:"unit")->"location":
    raise NotImplemented
    pass

@not_implemented
def GetUnitRallyUnit(whichUnit:"unit")->"unit":
    raise NotImplemented
    pass

@not_implemented
def GetUnitRallyDestructable(whichUnit:"unit")->"destructable":
    raise NotImplemented
    pass

@not_implemented
def IsUnitInGroup(whichUnit:"unit", whichGroup:"group")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitInForce(whichUnit:"unit", whichForce:"force")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitOwnedByPlayer(whichUnit:"unit", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitAlly(whichUnit:"unit", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitEnemy(whichUnit:"unit", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitVisible(whichUnit:"unit", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitDetected(whichUnit:"unit", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitInvisible(whichUnit:"unit", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitFogged(whichUnit:"unit", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitMasked(whichUnit:"unit", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitSelected(whichUnit:"unit", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitRace(whichUnit:"unit", whichRace:"race")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitType(whichUnit:"unit", whichUnitType:"unittype")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnit(whichUnit:"unit", whichSpecifiedUnit:"unit")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitInRange(whichUnit:"unit", otherUnit:"unit", distance:"real")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitInRangeXY(whichUnit:"unit", x:"real", y:"real", distance:"real")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitInRangeLoc(whichUnit:"unit", whichLocation:"location", distance:"real")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitHidden(whichUnit:"unit")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitIllusion(whichUnit:"unit")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitInTransport(whichUnit:"unit", whichTransport:"unit")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitLoaded(whichUnit:"unit")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsHeroUnitId(unitId:"integer")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def IsUnitIdType(unitId:"integer", whichUnitType:"unittype")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitShareVision(whichUnit:"unit", whichPlayer:"player", share:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def UnitSuspendDecay(whichUnit:"unit", suspend:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def UnitAddType(whichUnit:"unit", whichUnitType:"unittype")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitRemoveType(whichUnit:"unit", whichUnitType:"unittype")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitAddAbility(whichUnit:"unit", abilityId:"integer")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitRemoveAbility(whichUnit:"unit", abilityId:"integer")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitMakeAbilityPermanent(whichUnit:"unit", permanent:"boolean", abilityId:"integer")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitRemoveBuffs(whichUnit:"unit", removePositive:"boolean", removeNegative:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def UnitRemoveBuffsEx(whichUnit:"unit", removePositive:"boolean", removeNegative:"boolean", magic:"boolean", physical:"boolean", timedLife:"boolean", aura:"boolean", autoDispel:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def UnitHasBuffsEx(whichUnit:"unit", removePositive:"boolean", removeNegative:"boolean", magic:"boolean", physical:"boolean", timedLife:"boolean", aura:"boolean", autoDispel:"boolean")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitCountBuffsEx(whichUnit:"unit", removePositive:"boolean", removeNegative:"boolean", magic:"boolean", physical:"boolean", timedLife:"boolean", aura:"boolean", autoDispel:"boolean")->"integer":
    raise NotImplemented
    pass

@not_implemented
def UnitAddSleep(whichUnit:"unit", add:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def UnitCanSleep(whichUnit:"unit")->"boolean":
    raise NotImplemented
    pass

@not_implemented
def UnitAddSleepPerm(whichUnit:"unit", add:"boolean")->"nothing":
    raise NotImplemented
    pass

@not_implemented
def UnitCanSleepPerm(whichUnit:"unit")->"boolean":
    raise NotImplemented
    pass

def UnitIsSleeping(whichUnit:"unit")->"boolean":
    raise NotImplemented
    pass

def UnitWakeUp(whichUnit:"unit")->"nothing":
    raise NotImplemented
    pass

def UnitApplyTimedLife(whichUnit:"unit", buffId:"integer", duration:"real")->"nothing":
    raise NotImplemented
    pass

def UnitIgnoreAlarm(whichUnit:"unit", flag:"boolean")->"boolean":
    raise NotImplemented
    pass

def UnitIgnoreAlarmToggled(whichUnit:"unit")->"boolean":
    raise NotImplemented
    pass

def UnitResetCooldown(whichUnit:"unit")->"nothing":
    raise NotImplemented
    pass

def UnitSetConstructionProgress(whichUnit:"unit", constructionPercentage:"integer")->"nothing":
    raise NotImplemented
    pass

def UnitSetUpgradeProgress(whichUnit:"unit", upgradePercentage:"integer")->"nothing":
    raise NotImplemented
    pass

def UnitPauseTimedLife(whichUnit:"unit", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def UnitSetUsesAltIcon(whichUnit:"unit", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def UnitDamagePoint(whichUnit:"unit", delay:"real", radius:"real", x:"real", y:"real", amount:"real", attack:"boolean", ranged:"boolean", attackType:"attacktype", damageType:"damagetype", weaponType:"weapontype")->"boolean":
    raise NotImplemented
    pass

def UnitDamageTarget(whichUnit:"unit", target:"widget", amount:"real", attack:"boolean", ranged:"boolean", attackType:"attacktype", damageType:"damagetype", weaponType:"weapontype")->"boolean":
    raise NotImplemented
    pass

def IssueImmediateOrder(whichUnit:"unit", order:"string")->"boolean":
    raise NotImplemented
    pass

def IssueImmediateOrderById(whichUnit:"unit", order:"integer")->"boolean":
    raise NotImplemented
    pass

def IssuePointOrder(whichUnit:"unit", order:"string", x:"real", y:"real")->"boolean":
    raise NotImplemented
    pass

def IssuePointOrderLoc(whichUnit:"unit", order:"string", whichLocation:"location")->"boolean":
    raise NotImplemented
    pass

def IssuePointOrderById(whichUnit:"unit", order:"integer", x:"real", y:"real")->"boolean":
    raise NotImplemented
    pass

def IssuePointOrderByIdLoc(whichUnit:"unit", order:"integer", whichLocation:"location")->"boolean":
    raise NotImplemented
    pass

def IssueTargetOrder(whichUnit:"unit", order:"string", targetWidget:"widget")->"boolean":
    raise NotImplemented
    pass

def IssueTargetOrderById(whichUnit:"unit", order:"integer", targetWidget:"widget")->"boolean":
    raise NotImplemented
    pass

def IssueInstantPointOrder(whichUnit:"unit", order:"string", x:"real", y:"real", instantTargetWidget:"widget")->"boolean":
    raise NotImplemented
    pass

def IssueInstantPointOrderById(whichUnit:"unit", order:"integer", x:"real", y:"real", instantTargetWidget:"widget")->"boolean":
    raise NotImplemented
    pass

def IssueInstantTargetOrder(whichUnit:"unit", order:"string", targetWidget:"widget", instantTargetWidget:"widget")->"boolean":
    raise NotImplemented
    pass

def IssueInstantTargetOrderById(whichUnit:"unit", order:"integer", targetWidget:"widget", instantTargetWidget:"widget")->"boolean":
    raise NotImplemented
    pass

def IssueBuildOrder(whichPeon:"unit", unitToBuild:"string", x:"real", y:"real")->"boolean":
    raise NotImplemented
    pass

def IssueBuildOrderById(whichPeon:"unit", unitId:"integer", x:"real", y:"real")->"boolean":
    raise NotImplemented
    pass

def IssueNeutralImmediateOrder(forWhichPlayer:"player", neutralStructure:"unit", unitToBuild:"string")->"boolean":
    raise NotImplemented
    pass

def IssueNeutralImmediateOrderById(forWhichPlayer:"player", neutralStructure:"unit", unitId:"integer")->"boolean":
    raise NotImplemented
    pass

def IssueNeutralPointOrder(forWhichPlayer:"player", neutralStructure:"unit", unitToBuild:"string", x:"real", y:"real")->"boolean":
    raise NotImplemented
    pass

def IssueNeutralPointOrderById(forWhichPlayer:"player", neutralStructure:"unit", unitId:"integer", x:"real", y:"real")->"boolean":
    raise NotImplemented
    pass

def IssueNeutralTargetOrder(forWhichPlayer:"player", neutralStructure:"unit", unitToBuild:"string", target:"widget")->"boolean":
    raise NotImplemented
    pass

def IssueNeutralTargetOrderById(forWhichPlayer:"player", neutralStructure:"unit", unitId:"integer", target:"widget")->"boolean":
    raise NotImplemented
    pass

def GetUnitCurrentOrder(whichUnit:"unit")->"integer":
    raise NotImplemented
    pass

def SetResourceAmount(whichUnit:"unit", amount:"integer")->"nothing":
    raise NotImplemented
    pass

def AddResourceAmount(whichUnit:"unit", amount:"integer")->"nothing":
    raise NotImplemented
    pass

def GetResourceAmount(whichUnit:"unit")->"integer":
    raise NotImplemented
    pass

def WaygateGetDestinationX(waygate:"unit")->"real":
    raise NotImplemented
    pass

def WaygateGetDestinationY(waygate:"unit")->"real":
    raise NotImplemented
    pass

def WaygateSetDestination(waygate:"unit", x:"real", y:"real")->"nothing":
    raise NotImplemented
    pass

def WaygateActivate(waygate:"unit", activate:"boolean")->"nothing":
    raise NotImplemented
    pass

def WaygateIsActive(waygate:"unit")->"boolean":
    raise NotImplemented
    pass

def AddItemToAllStock(itemId:"integer", currentStock:"integer", stockMax:"integer")->"nothing":
    raise NotImplemented
    pass

def AddItemToStock(whichUnit:"unit", itemId:"integer", currentStock:"integer", stockMax:"integer")->"nothing":
    raise NotImplemented
    pass

def AddUnitToAllStock(unitId:"integer", currentStock:"integer", stockMax:"integer")->"nothing":
    raise NotImplemented
    pass

def AddUnitToStock(whichUnit:"unit", unitId:"integer", currentStock:"integer", stockMax:"integer")->"nothing":
    raise NotImplemented
    pass

def RemoveItemFromAllStock(itemId:"integer")->"nothing":
    raise NotImplemented
    pass

def RemoveItemFromStock(whichUnit:"unit", itemId:"integer")->"nothing":
    raise NotImplemented
    pass

def RemoveUnitFromAllStock(unitId:"integer")->"nothing":
    raise NotImplemented
    pass

def RemoveUnitFromStock(whichUnit:"unit", unitId:"integer")->"nothing":
    raise NotImplemented
    pass

def SetAllItemTypeSlots(slots:"integer")->"nothing":
    raise NotImplemented
    pass

def SetAllUnitTypeSlots(slots:"integer")->"nothing":
    raise NotImplemented
    pass

def SetItemTypeSlots(whichUnit:"unit", slots:"integer")->"nothing":
    raise NotImplemented
    pass

def SetUnitTypeSlots(whichUnit:"unit", slots:"integer")->"nothing":
    raise NotImplemented
    pass

def GetUnitUserData(whichUnit:"unit")->"integer":
    raise NotImplemented
    pass

def SetUnitUserData(whichUnit:"unit", data:"integer")->"nothing":
    raise NotImplemented
    pass

def Player(number:"integer")->"player":
    return number

@not_implemented
def GetLocalPlayer()->"player":
    raise NotImplemented
    pass

def IsPlayerAlly(whichPlayer:"player", otherPlayer:"player")->"boolean":
    raise NotImplemented
    pass

def IsPlayerEnemy(whichPlayer:"player", otherPlayer:"player")->"boolean":
    raise NotImplemented
    pass

def IsPlayerInForce(whichPlayer:"player", whichForce:"force")->"boolean":
    raise NotImplemented
    pass

def IsPlayerObserver(whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

def IsVisibleToPlayer(x:"real", y:"real", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

def IsLocationVisibleToPlayer(whichLocation:"location", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

def IsFoggedToPlayer(x:"real", y:"real", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

def IsLocationFoggedToPlayer(whichLocation:"location", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

def IsMaskedToPlayer(x:"real", y:"real", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

def IsLocationMaskedToPlayer(whichLocation:"location", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

def GetPlayerRace(whichPlayer:"player")->"race":
    raise NotImplemented
    pass

def GetPlayerId(whichPlayer:"player")->"integer":
    raise NotImplemented
    pass

def GetPlayerUnitCount(whichPlayer:"player", includeIncomplete:"boolean")->"integer":
    raise NotImplemented
    pass

def GetPlayerTypedUnitCount(whichPlayer:"player", unitName:"string", includeIncomplete:"boolean", includeUpgrades:"boolean")->"integer":
    raise NotImplemented
    pass

def GetPlayerStructureCount(whichPlayer:"player", includeIncomplete:"boolean")->"integer":
    raise NotImplemented
    pass

def GetPlayerState(whichPlayer:"player", whichPlayerState:"playerstate")->"integer":
    raise NotImplemented
    pass

def GetPlayerScore(whichPlayer:"player", whichPlayerScore:"playerscore")->"integer":
    raise NotImplemented
    pass

def GetPlayerAlliance(sourcePlayer:"player", otherPlayer:"player", whichAllianceSetting:"alliancetype")->"boolean":
    raise NotImplemented
    pass

def GetPlayerHandicap(whichPlayer:"player")->"real":
    raise NotImplemented
    pass

def GetPlayerHandicapXP(whichPlayer:"player")->"real":
    raise NotImplemented
    pass

def SetPlayerHandicap(whichPlayer:"player", handicap:"real")->"nothing":
    raise NotImplemented
    pass

def SetPlayerHandicapXP(whichPlayer:"player", handicap:"real")->"nothing":
    raise NotImplemented
    pass

def SetPlayerTechMaxAllowed(whichPlayer:"player", techid:"integer", maximum:"integer")->"nothing":
    raise NotImplemented
    pass

def GetPlayerTechMaxAllowed(whichPlayer:"player", techid:"integer")->"integer":
    raise NotImplemented
    pass

def AddPlayerTechResearched(whichPlayer:"player", techid:"integer", levels:"integer")->"nothing":
    raise NotImplemented
    pass

def SetPlayerTechResearched(whichPlayer:"player", techid:"integer", setToLevel:"integer")->"nothing":
    raise NotImplemented
    pass

def GetPlayerTechResearched(whichPlayer:"player", techid:"integer", specificonly:"boolean")->"boolean":
    raise NotImplemented
    pass

def GetPlayerTechCount(whichPlayer:"player", techid:"integer", specificonly:"boolean")->"integer":
    raise NotImplemented
    pass

def SetPlayerUnitsOwner(whichPlayer:"player", newOwner:"integer")->"nothing":
    raise NotImplemented
    pass

def CripplePlayer(whichPlayer:"player", toWhichPlayers:"force", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetPlayerAbilityAvailable(whichPlayer:"player", abilid:"integer", avail:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetPlayerState(whichPlayer:"player", whichPlayerState:"playerstate", value:"integer")->"nothing":
    raise NotImplemented
    pass

def RemovePlayer(whichPlayer:"player", gameResult:"playergameresult")->"nothing":
    raise NotImplemented
    pass

def CachePlayerHeroData(whichPlayer:"player")->"nothing":
    raise NotImplemented
    pass

def SetFogStateRect(forWhichPlayer:"player", whichState:"fogstate", where:"rect", useSharedVision:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetFogStateRadius(forWhichPlayer:"player", whichState:"fogstate", centerx:"real", centerY:"real", radius:"real", useSharedVision:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetFogStateRadiusLoc(forWhichPlayer:"player", whichState:"fogstate", center:"location", radius:"real", useSharedVision:"boolean")->"nothing":
    raise NotImplemented
    pass

def FogMaskEnable(enable:"boolean")->"nothing":
    raise NotImplemented
    pass

def IsFogMaskEnabled()->"boolean":
    raise NotImplemented
    pass

def FogEnable(enable:"boolean")->"nothing":
    raise NotImplemented
    pass

def IsFogEnabled()->"boolean":
    raise NotImplemented
    pass

def CreateFogModifierRect(forWhichPlayer:"player", whichState:"fogstate", where:"rect", useSharedVision:"boolean", afterUnits:"boolean")->"fogmodifier":
    raise NotImplemented
    pass

def CreateFogModifierRadius(forWhichPlayer:"player", whichState:"fogstate", centerx:"real", centerY:"real", radius:"real", useSharedVision:"boolean", afterUnits:"boolean")->"fogmodifier":
    raise NotImplemented
    pass

def CreateFogModifierRadiusLoc(forWhichPlayer:"player", whichState:"fogstate", center:"location", radius:"real", useSharedVision:"boolean", afterUnits:"boolean")->"fogmodifier":
    raise NotImplemented
    pass

def DestroyFogModifier(whichFogModifier:"fogmodifier")->"nothing":
    raise NotImplemented
    pass

def FogModifierStart(whichFogModifier:"fogmodifier")->"nothing":
    raise NotImplemented
    pass

def FogModifierStop(whichFogModifier:"fogmodifier")->"nothing":
    raise NotImplemented
    pass

def VersionGet()->"version":
    raise NotImplemented
    pass

def VersionCompatible(whichVersion:"version")->"boolean":
    raise NotImplemented
    pass

def VersionSupported(whichVersion:"version")->"boolean":
    raise NotImplemented
    pass

def EndGame(doScoreScreen:"boolean")->"nothing":
    raise NotImplemented
    pass

def ChangeLevel(newLevel:"string", doScoreScreen:"boolean")->"nothing":
    raise NotImplemented
    pass

def RestartGame(doScoreScreen:"boolean")->"nothing":
    raise NotImplemented
    pass

def ReloadGame()->"nothing":
    raise NotImplemented
    pass

def SetCampaignMenuRace(r:"race")->"nothing":
    raise NotImplemented
    pass

def SetCampaignMenuRaceEx(campaignIndex:"integer")->"nothing":
    raise NotImplemented
    pass

def ForceCampaignSelectScreen()->"nothing":
    raise NotImplemented
    pass

def LoadGame(saveFileName:"string", doScoreScreen:"boolean")->"nothing":
    raise NotImplemented
    pass

def SaveGame(saveFileName:"string")->"nothing":
    raise NotImplemented
    pass

def RenameSaveDirectory(sourceDirName:"string", destDirName:"string")->"boolean":
    raise NotImplemented
    pass

def RemoveSaveDirectory(sourceDirName:"string")->"boolean":
    raise NotImplemented
    pass

def CopySaveGame(sourceSaveName:"string", destSaveName:"string")->"boolean":
    raise NotImplemented
    pass

def SaveGameExists(saveName:"string")->"boolean":
    raise NotImplemented
    pass

def SyncSelections()->"nothing":
    raise NotImplemented
    pass

def SetFloatGameState(whichFloatGameState:"fgamestate", value:"real")->"nothing":
    raise NotImplemented
    pass

def GetFloatGameState(whichFloatGameState:"fgamestate")->"real":
    raise NotImplemented
    pass

def SetIntegerGameState(whichIntegerGameState:"igamestate", value:"integer")->"nothing":
    raise NotImplemented
    pass

def GetIntegerGameState(whichIntegerGameState:"igamestate")->"integer":
    raise NotImplemented
    pass

def SetTutorialCleared(cleared:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetMissionAvailable(campaignNumber:"integer", missionNumber:"integer", available:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetCampaignAvailable(campaignNumber:"integer", available:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetOpCinematicAvailable(campaignNumber:"integer", available:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetEdCinematicAvailable(campaignNumber:"integer", available:"boolean")->"nothing":
    raise NotImplemented
    pass

def GetDefaultDifficulty()->"gamedifficulty":
    raise NotImplemented
    pass

def SetDefaultDifficulty(g:"gamedifficulty")->"nothing":
    raise NotImplemented
    pass

def SetCustomCampaignButtonVisible(whichButton:"integer", visible:"boolean")->"nothing":
    raise NotImplemented
    pass

def GetCustomCampaignButtonVisible(whichButton:"integer")->"boolean":
    raise NotImplemented
    pass

def DoNotSaveReplay()->"nothing":
    raise NotImplemented
    pass

def DialogCreate()->"dialog":
    raise NotImplemented
    pass

def DialogDestroy(whichDialog:"dialog")->"nothing":
    raise NotImplemented
    pass

def DialogClear(whichDialog:"dialog")->"nothing":
    raise NotImplemented
    pass

def DialogSetMessage(whichDialog:"dialog", messageText:"string")->"nothing":
    raise NotImplemented
    pass

def DialogAddButton(whichDialog:"dialog", buttonText:"string", hotkey:"integer")->"button":
    raise NotImplemented
    pass

def DialogAddQuitButton(whichDialog:"dialog", doScoreScreen:"boolean", buttonText:"string", hotkey:"integer")->"button":
    raise NotImplemented
    pass

def DialogDisplay(whichPlayer:"player", whichDialog:"dialog", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def ReloadGameCachesFromDisk()->"boolean":
    raise NotImplemented
    pass

def InitGameCache(campaignFile:"string")->"gamecache":
    raise NotImplemented
    pass

def SaveGameCache(whichCache:"gamecache")->"boolean":
    raise NotImplemented
    pass

def StoreInteger(cache:"gamecache", missionKey:"string", key:"string", value:"integer")->"nothing":
    raise NotImplemented
    pass

def StoreReal(cache:"gamecache", missionKey:"string", key:"string", value:"real")->"nothing":
    raise NotImplemented
    pass

def StoreBoolean(cache:"gamecache", missionKey:"string", key:"string", value:"boolean")->"nothing":
    raise NotImplemented
    pass

def StoreUnit(cache:"gamecache", missionKey:"string", key:"string", whichUnit:"unit")->"boolean":
    raise NotImplemented
    pass

def StoreString(cache:"gamecache", missionKey:"string", key:"string", value:"string")->"boolean":
    raise NotImplemented
    pass

def SyncStoredInteger(cache:"gamecache", missionKey:"string", key:"string")->"nothing":
    raise NotImplemented
    pass

def SyncStoredReal(cache:"gamecache", missionKey:"string", key:"string")->"nothing":
    raise NotImplemented
    pass

def SyncStoredBoolean(cache:"gamecache", missionKey:"string", key:"string")->"nothing":
    raise NotImplemented
    pass

def SyncStoredUnit(cache:"gamecache", missionKey:"string", key:"string")->"nothing":
    raise NotImplemented
    pass

def SyncStoredString(cache:"gamecache", missionKey:"string", key:"string")->"nothing":
    raise NotImplemented
    pass

def HaveStoredInteger(cache:"gamecache", missionKey:"string", key:"string")->"boolean":
    raise NotImplemented
    pass

def HaveStoredReal(cache:"gamecache", missionKey:"string", key:"string")->"boolean":
    raise NotImplemented
    pass

def HaveStoredBoolean(cache:"gamecache", missionKey:"string", key:"string")->"boolean":
    raise NotImplemented
    pass

def HaveStoredUnit(cache:"gamecache", missionKey:"string", key:"string")->"boolean":
    raise NotImplemented
    pass

def HaveStoredString(cache:"gamecache", missionKey:"string", key:"string")->"boolean":
    raise NotImplemented
    pass

def FlushGameCache(cache:"gamecache")->"nothing":
    raise NotImplemented
    pass

def FlushStoredMission(cache:"gamecache", missionKey:"string")->"nothing":
    raise NotImplemented
    pass

def FlushStoredInteger(cache:"gamecache", missionKey:"string", key:"string")->"nothing":
    raise NotImplemented
    pass

def FlushStoredReal(cache:"gamecache", missionKey:"string", key:"string")->"nothing":
    raise NotImplemented
    pass

def FlushStoredBoolean(cache:"gamecache", missionKey:"string", key:"string")->"nothing":
    raise NotImplemented
    pass

def FlushStoredUnit(cache:"gamecache", missionKey:"string", key:"string")->"nothing":
    raise NotImplemented
    pass

def FlushStoredString(cache:"gamecache", missionKey:"string", key:"string")->"nothing":
    raise NotImplemented
    pass

def GetStoredInteger(cache:"gamecache", missionKey:"string", key:"string")->"integer":
    raise NotImplemented
    pass

def GetStoredReal(cache:"gamecache", missionKey:"string", key:"string")->"real":
    raise NotImplemented
    pass

def GetStoredBoolean(cache:"gamecache", missionKey:"string", key:"string")->"boolean":
    raise NotImplemented
    pass

def GetStoredString(cache:"gamecache", missionKey:"string", key:"string")->"string":
    raise NotImplemented
    pass

def RestoreUnit(cache:"gamecache", missionKey:"string", key:"string", forWhichPlayer:"player", x:"real", y:"real", facing:"real")->"unit":
    raise NotImplemented
    pass

def InitHashtable()->"hashtable":
    raise NotImplemented
    pass

def SaveInteger(table:"hashtable", parentKey:"integer", childKey:"integer", value:"integer")->"nothing":
    raise NotImplemented
    pass

def SaveReal(table:"hashtable", parentKey:"integer", childKey:"integer", value:"real")->"nothing":
    raise NotImplemented
    pass

def SaveBoolean(table:"hashtable", parentKey:"integer", childKey:"integer", value:"boolean")->"nothing":
    raise NotImplemented
    pass

def SaveStr(table:"hashtable", parentKey:"integer", childKey:"integer", value:"string")->"boolean":
    raise NotImplemented
    pass

def SavePlayerHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichPlayer:"player")->"boolean":
    raise NotImplemented
    pass

def SaveWidgetHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichWidget:"widget")->"boolean":
    raise NotImplemented
    pass

def SaveDestructableHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichDestructable:"destructable")->"boolean":
    raise NotImplemented
    pass

def SaveItemHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichItem:"item")->"boolean":
    raise NotImplemented
    pass

def SaveUnitHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichUnit:"unit")->"boolean":
    raise NotImplemented
    pass

def SaveAbilityHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichAbility:"ability")->"boolean":
    raise NotImplemented
    pass

def SaveTimerHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichTimer:"timer")->"boolean":
    raise NotImplemented
    pass

def SaveTriggerHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichTrigger:"trigger")->"boolean":
    raise NotImplemented
    pass

def SaveTriggerConditionHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichTriggercondition:"triggercondition")->"boolean":
    raise NotImplemented
    pass

def SaveTriggerActionHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichTriggeraction:"triggeraction")->"boolean":
    raise NotImplemented
    pass

def SaveTriggerEventHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichEvent:"event")->"boolean":
    raise NotImplemented
    pass

def SaveForceHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichForce:"force")->"boolean":
    raise NotImplemented
    pass

def SaveGroupHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichGroup:"group")->"boolean":
    raise NotImplemented
    pass

def SaveLocationHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichLocation:"location")->"boolean":
    raise NotImplemented
    pass

def SaveRectHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichRect:"rect")->"boolean":
    raise NotImplemented
    pass

def SaveBooleanExprHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichBoolexpr:"boolexpr")->"boolean":
    raise NotImplemented
    pass

def SaveSoundHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichSound:"sound")->"boolean":
    raise NotImplemented
    pass

def SaveEffectHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichEffect:"effect")->"boolean":
    raise NotImplemented
    pass

def SaveUnitPoolHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichUnitpool:"unitpool")->"boolean":
    raise NotImplemented
    pass

def SaveItemPoolHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichItempool:"itempool")->"boolean":
    raise NotImplemented
    pass

def SaveQuestHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichQuest:"quest")->"boolean":
    raise NotImplemented
    pass

def SaveQuestItemHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichQuestitem:"questitem")->"boolean":
    raise NotImplemented
    pass

def SaveDefeatConditionHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichDefeatcondition:"defeatcondition")->"boolean":
    raise NotImplemented
    pass

def SaveTimerDialogHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichTimerdialog:"timerdialog")->"boolean":
    raise NotImplemented
    pass

def SaveLeaderboardHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichLeaderboard:"leaderboard")->"boolean":
    raise NotImplemented
    pass

def SaveMultiboardHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichMultiboard:"multiboard")->"boolean":
    raise NotImplemented
    pass

def SaveMultiboardItemHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichMultiboarditem:"multiboarditem")->"boolean":
    raise NotImplemented
    pass

def SaveTrackableHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichTrackable:"trackable")->"boolean":
    raise NotImplemented
    pass

def SaveDialogHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichDialog:"dialog")->"boolean":
    raise NotImplemented
    pass

def SaveButtonHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichButton:"button")->"boolean":
    raise NotImplemented
    pass

def SaveTextTagHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichTexttag:"texttag")->"boolean":
    raise NotImplemented
    pass

def SaveLightningHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichLightning:"lightning")->"boolean":
    raise NotImplemented
    pass

def SaveImageHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichImage:"image")->"boolean":
    raise NotImplemented
    pass

def SaveUbersplatHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichUbersplat:"ubersplat")->"boolean":
    raise NotImplemented
    pass

def SaveRegionHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichRegion:"region")->"boolean":
    raise NotImplemented
    pass

def SaveFogStateHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichFogState:"fogstate")->"boolean":
    raise NotImplemented
    pass

def SaveFogModifierHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichFogModifier:"fogmodifier")->"boolean":
    raise NotImplemented
    pass

def SaveAgentHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichAgent:"agent")->"boolean":
    raise NotImplemented
    pass

def SaveHashtableHandle(table:"hashtable", parentKey:"integer", childKey:"integer", whichHashtable:"hashtable")->"boolean":
    raise NotImplemented
    pass

def LoadInteger(table:"hashtable", parentKey:"integer", childKey:"integer")->"integer":
    raise NotImplemented
    pass

def LoadReal(table:"hashtable", parentKey:"integer", childKey:"integer")->"real":
    raise NotImplemented
    pass

def LoadBoolean(table:"hashtable", parentKey:"integer", childKey:"integer")->"boolean":
    raise NotImplemented
    pass

def LoadStr(table:"hashtable", parentKey:"integer", childKey:"integer")->"string":
    raise NotImplemented
    pass

def LoadPlayerHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"player":
    raise NotImplemented
    pass

def LoadWidgetHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"widget":
    raise NotImplemented
    pass

def LoadDestructableHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"destructable":
    raise NotImplemented
    pass

def LoadItemHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"item":
    raise NotImplemented
    pass

def LoadUnitHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"unit":
    raise NotImplemented
    pass

def LoadAbilityHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"ability":
    raise NotImplemented
    pass

def LoadTimerHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"timer":
    raise NotImplemented
    pass

def LoadTriggerHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"trigger":
    raise NotImplemented
    pass

def LoadTriggerConditionHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"triggercondition":
    raise NotImplemented
    pass

def LoadTriggerActionHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"triggeraction":
    raise NotImplemented
    pass

def LoadTriggerEventHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"event":
    raise NotImplemented
    pass

def LoadForceHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"force":
    raise NotImplemented
    pass

def LoadGroupHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"group":
    raise NotImplemented
    pass

def LoadLocationHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"location":
    raise NotImplemented
    pass

def LoadRectHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"rect":
    raise NotImplemented
    pass

def LoadBooleanExprHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"boolexpr":
    raise NotImplemented
    pass

def LoadSoundHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"sound":
    raise NotImplemented
    pass

def LoadEffectHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"effect":
    raise NotImplemented
    pass

def LoadUnitPoolHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"unitpool":
    raise NotImplemented
    pass

def LoadItemPoolHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"itempool":
    raise NotImplemented
    pass

def LoadQuestHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"quest":
    raise NotImplemented
    pass

def LoadQuestItemHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"questitem":
    raise NotImplemented
    pass

def LoadDefeatConditionHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"defeatcondition":
    raise NotImplemented
    pass

def LoadTimerDialogHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"timerdialog":
    raise NotImplemented
    pass

def LoadLeaderboardHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"leaderboard":
    raise NotImplemented
    pass

def LoadMultiboardHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"multiboard":
    raise NotImplemented
    pass

def LoadMultiboardItemHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"multiboarditem":
    raise NotImplemented
    pass

def LoadTrackableHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"trackable":
    raise NotImplemented
    pass

def LoadDialogHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"dialog":
    raise NotImplemented
    pass

def LoadButtonHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"button":
    raise NotImplemented
    pass

def LoadTextTagHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"texttag":
    raise NotImplemented
    pass

def LoadLightningHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"lightning":
    raise NotImplemented
    pass

def LoadImageHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"image":
    raise NotImplemented
    pass

def LoadUbersplatHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"ubersplat":
    raise NotImplemented
    pass

def LoadRegionHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"region":
    raise NotImplemented
    pass

def LoadFogStateHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"fogstate":
    raise NotImplemented
    pass

def LoadFogModifierHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"fogmodifier":
    raise NotImplemented
    pass

def LoadHashtableHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"hashtable":
    raise NotImplemented
    pass

def HaveSavedInteger(table:"hashtable", parentKey:"integer", childKey:"integer")->"boolean":
    raise NotImplemented
    pass

def HaveSavedReal(table:"hashtable", parentKey:"integer", childKey:"integer")->"boolean":
    raise NotImplemented
    pass

def HaveSavedBoolean(table:"hashtable", parentKey:"integer", childKey:"integer")->"boolean":
    raise NotImplemented
    pass

def HaveSavedString(table:"hashtable", parentKey:"integer", childKey:"integer")->"boolean":
    raise NotImplemented
    pass

def HaveSavedHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"boolean":
    raise NotImplemented
    pass

def RemoveSavedInteger(table:"hashtable", parentKey:"integer", childKey:"integer")->"nothing":
    raise NotImplemented
    pass

def RemoveSavedReal(table:"hashtable", parentKey:"integer", childKey:"integer")->"nothing":
    raise NotImplemented
    pass

def RemoveSavedBoolean(table:"hashtable", parentKey:"integer", childKey:"integer")->"nothing":
    raise NotImplemented
    pass

def RemoveSavedString(table:"hashtable", parentKey:"integer", childKey:"integer")->"nothing":
    raise NotImplemented
    pass

def RemoveSavedHandle(table:"hashtable", parentKey:"integer", childKey:"integer")->"nothing":
    raise NotImplemented
    pass

def FlushParentHashtable(table:"hashtable")->"nothing":
    raise NotImplemented
    pass

def FlushChildHashtable(table:"hashtable", parentKey:"integer")->"nothing":
    raise NotImplemented
    pass

def GetRandomInt(lowBound:"integer", highBound:"integer")->"integer":
    raise NotImplemented
    pass

def GetRandomReal(lowBound:"real", highBound:"real")->"real":
    raise NotImplemented
    pass

def CreateUnitPool()->"unitpool":
    raise NotImplemented
    pass

def DestroyUnitPool(whichPool:"unitpool")->"nothing":
    raise NotImplemented
    pass

def UnitPoolAddUnitType(whichPool:"unitpool", unitId:"integer", weight:"real")->"nothing":
    raise NotImplemented
    pass

def UnitPoolRemoveUnitType(whichPool:"unitpool", unitId:"integer")->"nothing":
    raise NotImplemented
    pass

def PlaceRandomUnit(whichPool:"unitpool", forWhichPlayer:"player", x:"real", y:"real", facing:"real")->"unit":
    raise NotImplemented
    pass

def CreateItemPool()->"itempool":
    raise NotImplemented
    pass

def DestroyItemPool(whichItemPool:"itempool")->"nothing":
    raise NotImplemented
    pass

def ItemPoolAddItemType(whichItemPool:"itempool", itemId:"integer", weight:"real")->"nothing":
    raise NotImplemented
    pass

def ItemPoolRemoveItemType(whichItemPool:"itempool", itemId:"integer")->"nothing":
    raise NotImplemented
    pass

def PlaceRandomItem(whichItemPool:"itempool", x:"real", y:"real")->"item":
    raise NotImplemented
    pass

def ChooseRandomCreep(level:"integer")->"integer":
    raise NotImplemented
    pass

def ChooseRandomNPBuilding()->"integer":
    raise NotImplemented
    pass

def ChooseRandomItem(level:"integer")->"integer":
    raise NotImplemented
    pass

def ChooseRandomItemEx(whichType:"itemtype", level:"integer")->"integer":
    raise NotImplemented
    pass

def SetRandomSeed(seed:"integer")->"nothing":
    raise NotImplemented
    pass

def SetTerrainFog(a:"real", b:"real", c:"real", d:"real", e:"real")->"nothing":
    raise NotImplemented
    pass

def ResetTerrainFog()->"nothing":
    raise NotImplemented
    pass

def SetUnitFog(a:"real", b:"real", c:"real", d:"real", e:"real")->"nothing":
    raise NotImplemented
    pass

def SetTerrainFogEx(style:"integer", zstart:"real", zend:"real", density:"real", red:"real", green:"real", blue:"real")->"nothing":
    raise NotImplemented
    pass

def DisplayTextToPlayer(toPlayer:"player", x:"real", y:"real", message:"string")->"nothing":
    raise NotImplemented
    pass

def DisplayTimedTextToPlayer(toPlayer:"player", x:"real", y:"real", duration:"real", message:"string")->"nothing":
    # simple implementation for console uses
    print("to>",toPlayer,": ", message)
    pass

def DisplayTimedTextFromPlayer(toPlayer:"player", x:"real", y:"real", duration:"real", message:"string")->"nothing":
    raise NotImplemented
    pass

def ClearTextMessages()->"nothing":
    raise NotImplemented
    pass

def SetDayNightModels(terrainDNCFile:"string", unitDNCFile:"string")->"nothing":
    raise NotImplemented
    pass

def SetSkyModel(skyModelFile:"string")->"nothing":
    raise NotImplemented
    pass

def EnableUserControl(b:"boolean")->"nothing":
    raise NotImplemented
    pass

def EnableUserUI(b:"boolean")->"nothing":
    raise NotImplemented
    pass

def SuspendTimeOfDay(b:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetTimeOfDayScale(r:"real")->"nothing":
    raise NotImplemented
    pass

def GetTimeOfDayScale()->"real":
    raise NotImplemented
    pass

def ShowInterface(flag:"boolean", fadeDuration:"real")->"nothing":
    raise NotImplemented
    pass

def PauseGame(flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def UnitAddIndicator(whichUnit:"unit", red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def AddIndicator(whichWidget:"widget", red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def PingMinimap(x:"real", y:"real", duration:"real")->"nothing":
    raise NotImplemented
    pass

def PingMinimapEx(x:"real", y:"real", duration:"real", red:"integer", green:"integer", blue:"integer", extraEffects:"boolean")->"nothing":
    raise NotImplemented
    pass

def EnableOcclusion(flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetIntroShotText(introText:"string")->"nothing":
    raise NotImplemented
    pass

def SetIntroShotModel(introModelPath:"string")->"nothing":
    raise NotImplemented
    pass

def EnableWorldFogBoundary(b:"boolean")->"nothing":
    raise NotImplemented
    pass

def PlayModelCinematic(modelName:"string")->"nothing":
    raise NotImplemented
    pass

def PlayCinematic(movieName:"string")->"nothing":
    raise NotImplemented
    pass

def ForceUIKey(key:"string")->"nothing":
    raise NotImplemented
    pass

def ForceUICancel()->"nothing":
    raise NotImplemented
    pass

def DisplayLoadDialog()->"nothing":
    raise NotImplemented
    pass

def SetAltMinimapIcon(iconPath:"string")->"nothing":
    raise NotImplemented
    pass

def DisableRestartMission(flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def CreateTextTag()->"texttag":
    raise NotImplemented
    pass

def DestroyTextTag(t:"texttag")->"nothing":
    raise NotImplemented
    pass

def SetTextTagText(t:"texttag", s:"string", height:"real")->"nothing":
    raise NotImplemented
    pass

def SetTextTagPos(t:"texttag", x:"real", y:"real", heightOffset:"real")->"nothing":
    raise NotImplemented
    pass

def SetTextTagPosUnit(t:"texttag", whichUnit:"unit", heightOffset:"real")->"nothing":
    raise NotImplemented
    pass

def SetTextTagColor(t:"texttag", red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def SetTextTagVelocity(t:"texttag", xvel:"real", yvel:"real")->"nothing":
    raise NotImplemented
    pass

def SetTextTagVisibility(t:"texttag", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetTextTagSuspended(t:"texttag", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetTextTagPermanent(t:"texttag", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetTextTagAge(t:"texttag", age:"real")->"nothing":
    raise NotImplemented
    pass

def SetTextTagLifespan(t:"texttag", lifespan:"real")->"nothing":
    raise NotImplemented
    pass

def SetTextTagFadepoint(t:"texttag", fadepoint:"real")->"nothing":
    raise NotImplemented
    pass

def SetReservedLocalHeroButtons(reserved:"integer")->"nothing":
    raise NotImplemented
    pass

def GetAllyColorFilterState()->"integer":
    raise NotImplemented
    pass

def SetAllyColorFilterState(state:"integer")->"nothing":
    raise NotImplemented
    pass

def GetCreepCampFilterState()->"boolean":
    raise NotImplemented
    pass

def SetCreepCampFilterState(state:"boolean")->"nothing":
    raise NotImplemented
    pass

def EnableMinimapFilterButtons(enableAlly:"boolean", enableCreep:"boolean")->"nothing":
    raise NotImplemented
    pass

def EnableDragSelect(state:"boolean", ui:"boolean")->"nothing":
    raise NotImplemented
    pass

def EnablePreSelect(state:"boolean", ui:"boolean")->"nothing":
    raise NotImplemented
    pass

def EnableSelect(state:"boolean", ui:"boolean")->"nothing":
    raise NotImplemented
    pass

def CreateTrackable(trackableModelPath:"string", x:"real", y:"real", facing:"real")->"trackable":
    raise NotImplemented
    pass

def CreateQuest()->"quest":
    raise NotImplemented
    pass

def DestroyQuest(whichQuest:"quest")->"nothing":
    raise NotImplemented
    pass

def QuestSetTitle(whichQuest:"quest", title:"string")->"nothing":
    raise NotImplemented
    pass

def QuestSetDescription(whichQuest:"quest", description:"string")->"nothing":
    raise NotImplemented
    pass

def QuestSetIconPath(whichQuest:"quest", iconPath:"string")->"nothing":
    raise NotImplemented
    pass

def QuestSetRequired(whichQuest:"quest", required:"boolean")->"nothing":
    raise NotImplemented
    pass

def QuestSetCompleted(whichQuest:"quest", completed:"boolean")->"nothing":
    raise NotImplemented
    pass

def QuestSetDiscovered(whichQuest:"quest", discovered:"boolean")->"nothing":
    raise NotImplemented
    pass

def QuestSetFailed(whichQuest:"quest", failed:"boolean")->"nothing":
    raise NotImplemented
    pass

def QuestSetEnabled(whichQuest:"quest", enabled:"boolean")->"nothing":
    raise NotImplemented
    pass

def IsQuestRequired(whichQuest:"quest")->"boolean":
    raise NotImplemented
    pass

def IsQuestCompleted(whichQuest:"quest")->"boolean":
    raise NotImplemented
    pass

def IsQuestDiscovered(whichQuest:"quest")->"boolean":
    raise NotImplemented
    pass

def IsQuestFailed(whichQuest:"quest")->"boolean":
    raise NotImplemented
    pass

def IsQuestEnabled(whichQuest:"quest")->"boolean":
    raise NotImplemented
    pass

def QuestCreateItem(whichQuest:"quest")->"questitem":
    raise NotImplemented
    pass

def QuestItemSetDescription(whichQuestItem:"questitem", description:"string")->"nothing":
    raise NotImplemented
    pass

def QuestItemSetCompleted(whichQuestItem:"questitem", completed:"boolean")->"nothing":
    raise NotImplemented
    pass

def IsQuestItemCompleted(whichQuestItem:"questitem")->"boolean":
    raise NotImplemented
    pass

def CreateDefeatCondition()->"defeatcondition":
    raise NotImplemented
    pass

def DestroyDefeatCondition(whichCondition:"defeatcondition")->"nothing":
    raise NotImplemented
    pass

def DefeatConditionSetDescription(whichCondition:"defeatcondition", description:"string")->"nothing":
    raise NotImplemented
    pass

def FlashQuestDialogButton()->"nothing":
    raise NotImplemented
    pass

def ForceQuestDialogUpdate()->"nothing":
    raise NotImplemented
    pass

def CreateTimerDialog(t:"timer")->"timerdialog":
    raise NotImplemented
    pass

def DestroyTimerDialog(whichDialog:"timerdialog")->"nothing":
    raise NotImplemented
    pass

def TimerDialogSetTitle(whichDialog:"timerdialog", title:"string")->"nothing":
    raise NotImplemented
    pass

def TimerDialogSetTitleColor(whichDialog:"timerdialog", red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def TimerDialogSetTimeColor(whichDialog:"timerdialog", red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def TimerDialogSetSpeed(whichDialog:"timerdialog", speedMultFactor:"real")->"nothing":
    raise NotImplemented
    pass

def TimerDialogDisplay(whichDialog:"timerdialog", display:"boolean")->"nothing":
    raise NotImplemented
    pass

def IsTimerDialogDisplayed(whichDialog:"timerdialog")->"boolean":
    raise NotImplemented
    pass

def TimerDialogSetRealTimeRemaining(whichDialog:"timerdialog", timeRemaining:"real")->"nothing":
    raise NotImplemented
    pass

def CreateLeaderboard()->"leaderboard":
    raise NotImplemented
    pass

def DestroyLeaderboard(lb:"leaderboard")->"nothing":
    raise NotImplemented
    pass

def LeaderboardDisplay(lb:"leaderboard", show:"boolean")->"nothing":
    raise NotImplemented
    pass

def IsLeaderboardDisplayed(lb:"leaderboard")->"boolean":
    raise NotImplemented
    pass

def LeaderboardGetItemCount(lb:"leaderboard")->"integer":
    raise NotImplemented
    pass

def LeaderboardSetSizeByItemCount(lb:"leaderboard", count:"integer")->"nothing":
    raise NotImplemented
    pass

def LeaderboardAddItem(lb:"leaderboard", label:"string", value:"integer", p:"player")->"nothing":
    raise NotImplemented
    pass

def LeaderboardRemoveItem(lb:"leaderboard", index:"integer")->"nothing":
    raise NotImplemented
    pass

def LeaderboardRemovePlayerItem(lb:"leaderboard", p:"player")->"nothing":
    raise NotImplemented
    pass

def LeaderboardClear(lb:"leaderboard")->"nothing":
    raise NotImplemented
    pass

def LeaderboardSortItemsByValue(lb:"leaderboard", ascending:"boolean")->"nothing":
    raise NotImplemented
    pass

def LeaderboardSortItemsByPlayer(lb:"leaderboard", ascending:"boolean")->"nothing":
    raise NotImplemented
    pass

def LeaderboardSortItemsByLabel(lb:"leaderboard", ascending:"boolean")->"nothing":
    raise NotImplemented
    pass

def LeaderboardHasPlayerItem(lb:"leaderboard", p:"player")->"boolean":
    raise NotImplemented
    pass

def LeaderboardGetPlayerIndex(lb:"leaderboard", p:"player")->"integer":
    raise NotImplemented
    pass

def LeaderboardSetLabel(lb:"leaderboard", label:"string")->"nothing":
    raise NotImplemented
    pass

def LeaderboardGetLabelText(lb:"leaderboard")->"string":
    raise NotImplemented
    pass

def PlayerSetLeaderboard(toPlayer:"player", lb:"leaderboard")->"nothing":
    raise NotImplemented
    pass

def PlayerGetLeaderboard(toPlayer:"player")->"leaderboard":
    raise NotImplemented
    pass

def LeaderboardSetLabelColor(lb:"leaderboard", red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def LeaderboardSetValueColor(lb:"leaderboard", red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def LeaderboardSetStyle(lb:"leaderboard", showLabel:"boolean", showNames:"boolean", showValues:"boolean", showIcons:"boolean")->"nothing":
    raise NotImplemented
    pass

def LeaderboardSetItemValue(lb:"leaderboard", whichItem:"integer", val:"integer")->"nothing":
    raise NotImplemented
    pass

def LeaderboardSetItemLabel(lb:"leaderboard", whichItem:"integer", val:"string")->"nothing":
    raise NotImplemented
    pass

def LeaderboardSetItemStyle(lb:"leaderboard", whichItem:"integer", showLabel:"boolean", showValue:"boolean", showIcon:"boolean")->"nothing":
    raise NotImplemented
    pass

def LeaderboardSetItemLabelColor(lb:"leaderboard", whichItem:"integer", red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def LeaderboardSetItemValueColor(lb:"leaderboard", whichItem:"integer", red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def CreateMultiboard()->"multiboard":
    raise NotImplemented
    pass

def DestroyMultiboard(lb:"multiboard")->"nothing":
    raise NotImplemented
    pass

def MultiboardDisplay(lb:"multiboard", show:"boolean")->"nothing":
    raise NotImplemented
    pass

def IsMultiboardDisplayed(lb:"multiboard")->"boolean":
    raise NotImplemented
    pass

def MultiboardMinimize(lb:"multiboard", minimize:"boolean")->"nothing":
    raise NotImplemented
    pass

def IsMultiboardMinimized(lb:"multiboard")->"boolean":
    raise NotImplemented
    pass

def MultiboardClear(lb:"multiboard")->"nothing":
    raise NotImplemented
    pass

def MultiboardSetTitleText(lb:"multiboard", label:"string")->"nothing":
    raise NotImplemented
    pass

def MultiboardGetTitleText(lb:"multiboard")->"string":
    raise NotImplemented
    pass

def MultiboardSetTitleTextColor(lb:"multiboard", red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def MultiboardGetRowCount(lb:"multiboard")->"integer":
    raise NotImplemented
    pass

def MultiboardGetColumnCount(lb:"multiboard")->"integer":
    raise NotImplemented
    pass

def MultiboardSetColumnCount(lb:"multiboard", count:"integer")->"nothing":
    raise NotImplemented
    pass

def MultiboardSetRowCount(lb:"multiboard", count:"integer")->"nothing":
    raise NotImplemented
    pass

def MultiboardSetItemsStyle(lb:"multiboard", showValues:"boolean", showIcons:"boolean")->"nothing":
    raise NotImplemented
    pass

def MultiboardSetItemsValue(lb:"multiboard", value:"string")->"nothing":
    raise NotImplemented
    pass

def MultiboardSetItemsValueColor(lb:"multiboard", red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def MultiboardSetItemsWidth(lb:"multiboard", width:"real")->"nothing":
    raise NotImplemented
    pass

def MultiboardSetItemsIcon(lb:"multiboard", iconPath:"string")->"nothing":
    raise NotImplemented
    pass

def MultiboardGetItem(lb:"multiboard", row:"integer", column:"integer")->"multiboarditem":
    raise NotImplemented
    pass

def MultiboardReleaseItem(mbi:"multiboarditem")->"nothing":
    raise NotImplemented
    pass

def MultiboardSetItemStyle(mbi:"multiboarditem", showValue:"boolean", showIcon:"boolean")->"nothing":
    raise NotImplemented
    pass

def MultiboardSetItemValue(mbi:"multiboarditem", val:"string")->"nothing":
    raise NotImplemented
    pass

def MultiboardSetItemValueColor(mbi:"multiboarditem", red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def MultiboardSetItemWidth(mbi:"multiboarditem", width:"real")->"nothing":
    raise NotImplemented
    pass

def MultiboardSetItemIcon(mbi:"multiboarditem", iconFileName:"string")->"nothing":
    raise NotImplemented
    pass

def MultiboardSuppressDisplay(flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetCameraPosition(x:"real", y:"real")->"nothing":
    raise NotImplemented
    pass

def SetCameraQuickPosition(x:"real", y:"real")->"nothing":
    raise NotImplemented
    pass

def SetCameraBounds(x1:"real", y1:"real", x2:"real", y2:"real", x3:"real", y3:"real", x4:"real", y4:"real")->"nothing":
    raise NotImplemented
    pass

def StopCamera()->"nothing":
    raise NotImplemented
    pass

def ResetToGameCamera(duration:"real")->"nothing":
    raise NotImplemented
    pass

def PanCameraTo(x:"real", y:"real")->"nothing":
    raise NotImplemented
    pass

def PanCameraToTimed(x:"real", y:"real", duration:"real")->"nothing":
    raise NotImplemented
    pass

def PanCameraToWithZ(x:"real", y:"real", zOffsetDest:"real")->"nothing":
    raise NotImplemented
    pass

def PanCameraToTimedWithZ(x:"real", y:"real", zOffsetDest:"real", duration:"real")->"nothing":
    raise NotImplemented
    pass

def SetCinematicCamera(cameraModelFile:"string")->"nothing":
    raise NotImplemented
    pass

def SetCameraRotateMode(x:"real", y:"real", radiansToSweep:"real", duration:"real")->"nothing":
    raise NotImplemented
    pass

def SetCameraField(whichField:"camerafield", value:"real", duration:"real")->"nothing":
    raise NotImplemented
    pass

def AdjustCameraField(whichField:"camerafield", offset:"real", duration:"real")->"nothing":
    raise NotImplemented
    pass

def SetCameraTargetController(whichUnit:"unit", xoffset:"real", yoffset:"real", inheritOrientation:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetCameraOrientController(whichUnit:"unit", xoffset:"real", yoffset:"real")->"nothing":
    raise NotImplemented
    pass

def CreateCameraSetup()->"camerasetup":
    raise NotImplemented
    pass

def CameraSetupSetField(whichSetup:"camerasetup", whichField:"camerafield", value:"real", duration:"real")->"nothing":
    raise NotImplemented
    pass

def CameraSetupGetField(whichSetup:"camerasetup", whichField:"camerafield")->"real":
    raise NotImplemented
    pass

def CameraSetupSetDestPosition(whichSetup:"camerasetup", x:"real", y:"real", duration:"real")->"nothing":
    raise NotImplemented
    pass

def CameraSetupGetDestPositionLoc(whichSetup:"camerasetup")->"location":
    raise NotImplemented
    pass

def CameraSetupGetDestPositionX(whichSetup:"camerasetup")->"real":
    raise NotImplemented
    pass

def CameraSetupGetDestPositionY(whichSetup:"camerasetup")->"real":
    raise NotImplemented
    pass

def CameraSetupApply(whichSetup:"camerasetup", doPan:"boolean", panTimed:"boolean")->"nothing":
    raise NotImplemented
    pass

def CameraSetupApplyWithZ(whichSetup:"camerasetup", zDestOffset:"real")->"nothing":
    raise NotImplemented
    pass

def CameraSetupApplyForceDuration(whichSetup:"camerasetup", doPan:"boolean", forceDuration:"real")->"nothing":
    raise NotImplemented
    pass

def CameraSetupApplyForceDurationWithZ(whichSetup:"camerasetup", zDestOffset:"real", forceDuration:"real")->"nothing":
    raise NotImplemented
    pass

def CameraSetTargetNoise(mag:"real", velocity:"real")->"nothing":
    raise NotImplemented
    pass

def CameraSetSourceNoise(mag:"real", velocity:"real")->"nothing":
    raise NotImplemented
    pass

def CameraSetTargetNoiseEx(mag:"real", velocity:"real", vertOnly:"boolean")->"nothing":
    raise NotImplemented
    pass

def CameraSetSourceNoiseEx(mag:"real", velocity:"real", vertOnly:"boolean")->"nothing":
    raise NotImplemented
    pass

def CameraSetSmoothingFactor(factor:"real")->"nothing":
    raise NotImplemented
    pass

def SetCineFilterTexture(filename:"string")->"nothing":
    raise NotImplemented
    pass

def SetCineFilterBlendMode(whichMode:"blendmode")->"nothing":
    raise NotImplemented
    pass

def SetCineFilterTexMapFlags(whichFlags:"texmapflags")->"nothing":
    raise NotImplemented
    pass

def SetCineFilterStartUV(minu:"real", minv:"real", maxu:"real", maxv:"real")->"nothing":
    raise NotImplemented
    pass

def SetCineFilterEndUV(minu:"real", minv:"real", maxu:"real", maxv:"real")->"nothing":
    raise NotImplemented
    pass

def SetCineFilterStartColor(red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def SetCineFilterEndColor(red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def SetCineFilterDuration(duration:"real")->"nothing":
    raise NotImplemented
    pass

def DisplayCineFilter(flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def IsCineFilterDisplayed()->"boolean":
    raise NotImplemented
    pass

def SetCinematicScene(portraitUnitId:"integer", color:"playercolor", speakerTitle:"string", text:"string", sceneDuration:"real", voiceoverDuration:"real")->"nothing":
    raise NotImplemented
    pass

def EndCinematicScene()->"nothing":
    raise NotImplemented
    pass

def ForceCinematicSubtitles(flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def GetCameraMargin(whichMargin:"integer")->"real":
    raise NotImplemented
    pass

def GetCameraBoundMinX()->"real":
    raise NotImplemented
    pass

def GetCameraBoundMinY()->"real":
    raise NotImplemented
    pass

def GetCameraBoundMaxX()->"real":
    raise NotImplemented
    pass

def GetCameraBoundMaxY()->"real":
    raise NotImplemented
    pass

def GetCameraField(whichField:"camerafield")->"real":
    raise NotImplemented
    pass

def GetCameraTargetPositionX()->"real":
    raise NotImplemented
    pass

def GetCameraTargetPositionY()->"real":
    raise NotImplemented
    pass

def GetCameraTargetPositionZ()->"real":
    raise NotImplemented
    pass

def GetCameraTargetPositionLoc()->"location":
    raise NotImplemented
    pass

def GetCameraEyePositionX()->"real":
    raise NotImplemented
    pass

def GetCameraEyePositionY()->"real":
    raise NotImplemented
    pass

def GetCameraEyePositionZ()->"real":
    raise NotImplemented
    pass

def GetCameraEyePositionLoc()->"location":
    raise NotImplemented
    pass

def NewSoundEnvironment(environmentName:"string")->"nothing":
    raise NotImplemented
    pass

def CreateSound(fileName:"string", looping:"boolean", is3D:"boolean", stopwhenoutofrange:"boolean", fadeInRate:"integer", fadeOutRate:"integer", eaxSetting:"string")->"sound":
    raise NotImplemented
    pass

def CreateSoundFilenameWithLabel(fileName:"string", looping:"boolean", is3D:"boolean", stopwhenoutofrange:"boolean", fadeInRate:"integer", fadeOutRate:"integer", SLKEntryName:"string")->"sound":
    raise NotImplemented
    pass

def CreateSoundFromLabel(soundLabel:"string", looping:"boolean", is3D:"boolean", stopwhenoutofrange:"boolean", fadeInRate:"integer", fadeOutRate:"integer")->"sound":
    raise NotImplemented
    pass

def CreateMIDISound(soundLabel:"string", fadeInRate:"integer", fadeOutRate:"integer")->"sound":
    raise NotImplemented
    pass

def SetSoundParamsFromLabel(soundHandle:"sound", soundLabel:"string")->"nothing":
    raise NotImplemented
    pass

def SetSoundDistanceCutoff(soundHandle:"sound", cutoff:"real")->"nothing":
    raise NotImplemented
    pass

def SetSoundChannel(soundHandle:"sound", channel:"integer")->"nothing":
    raise NotImplemented
    pass

def SetSoundVolume(soundHandle:"sound", volume:"integer")->"nothing":
    raise NotImplemented
    pass

def SetSoundPitch(soundHandle:"sound", pitch:"real")->"nothing":
    raise NotImplemented
    pass

def SetSoundPlayPosition(soundHandle:"sound", millisecs:"integer")->"nothing":
    raise NotImplemented
    pass

def SetSoundDistances(soundHandle:"sound", minDist:"real", maxDist:"real")->"nothing":
    raise NotImplemented
    pass

def SetSoundConeAngles(soundHandle:"sound", inside:"real", outside:"real", outsideVolume:"integer")->"nothing":
    raise NotImplemented
    pass

def SetSoundConeOrientation(soundHandle:"sound", x:"real", y:"real", z:"real")->"nothing":
    raise NotImplemented
    pass

def SetSoundPosition(soundHandle:"sound", x:"real", y:"real", z:"real")->"nothing":
    raise NotImplemented
    pass

def SetSoundVelocity(soundHandle:"sound", x:"real", y:"real", z:"real")->"nothing":
    raise NotImplemented
    pass

def AttachSoundToUnit(soundHandle:"sound", whichUnit:"unit")->"nothing":
    raise NotImplemented
    pass

def StartSound(soundHandle:"sound")->"nothing":
    raise NotImplemented
    pass

def StopSound(soundHandle:"sound", killWhenDone:"boolean", fadeOut:"boolean")->"nothing":
    raise NotImplemented
    pass

def KillSoundWhenDone(soundHandle:"sound")->"nothing":
    raise NotImplemented
    pass

def SetMapMusic(musicName:"string", random:"boolean", index:"integer")->"nothing":
    raise NotImplemented
    pass

def ClearMapMusic()->"nothing":
    raise NotImplemented
    pass

def PlayMusic(musicName:"string")->"nothing":
    raise NotImplemented
    pass

def PlayMusicEx(musicName:"string", frommsecs:"integer", fadeinmsecs:"integer")->"nothing":
    raise NotImplemented
    pass

def StopMusic(fadeOut:"boolean")->"nothing":
    raise NotImplemented
    pass

def ResumeMusic()->"nothing":
    raise NotImplemented
    pass

def PlayThematicMusic(musicFileName:"string")->"nothing":
    raise NotImplemented
    pass

def PlayThematicMusicEx(musicFileName:"string", frommsecs:"integer")->"nothing":
    raise NotImplemented
    pass

def EndThematicMusic()->"nothing":
    raise NotImplemented
    pass

def SetMusicVolume(volume:"integer")->"nothing":
    raise NotImplemented
    pass

def SetMusicPlayPosition(millisecs:"integer")->"nothing":
    raise NotImplemented
    pass

def SetThematicMusicPlayPosition(millisecs:"integer")->"nothing":
    raise NotImplemented
    pass

def SetSoundDuration(soundHandle:"sound", duration:"integer")->"nothing":
    raise NotImplemented
    pass

def GetSoundDuration(soundHandle:"sound")->"integer":
    raise NotImplemented
    pass

def GetSoundFileDuration(musicFileName:"string")->"integer":
    raise NotImplemented
    pass

def VolumeGroupSetVolume(vgroup:"volumegroup", scale:"real")->"nothing":
    raise NotImplemented
    pass

def VolumeGroupReset()->"nothing":
    raise NotImplemented
    pass

def GetSoundIsPlaying(soundHandle:"sound")->"boolean":
    raise NotImplemented
    pass

def GetSoundIsLoading(soundHandle:"sound")->"boolean":
    raise NotImplemented
    pass

def RegisterStackedSound(soundHandle:"sound", byPosition:"boolean", rectwidth:"real", rectheight:"real")->"nothing":
    raise NotImplemented
    pass

def UnregisterStackedSound(soundHandle:"sound", byPosition:"boolean", rectwidth:"real", rectheight:"real")->"nothing":
    raise NotImplemented
    pass

def AddWeatherEffect(where:"rect", effectID:"integer")->"weathereffect":
    raise NotImplemented
    pass

def RemoveWeatherEffect(whichEffect:"weathereffect")->"nothing":
    raise NotImplemented
    pass

def EnableWeatherEffect(whichEffect:"weathereffect", enable:"boolean")->"nothing":
    raise NotImplemented
    pass

def TerrainDeformCrater(x:"real", y:"real", radius:"real", depth:"real", duration:"integer", permanent:"boolean")->"terraindeformation":
    raise NotImplemented
    pass

def TerrainDeformRipple(x:"real", y:"real", radius:"real", depth:"real", duration:"integer", count:"integer", spaceWaves:"real", timeWaves:"real", radiusStartPct:"real", limitNeg:"boolean")->"terraindeformation":
    raise NotImplemented
    pass

def TerrainDeformWave(x:"real", y:"real", dirX:"real", dirY:"real", distance:"real", speed:"real", radius:"real", depth:"real", trailTime:"integer", count:"integer")->"terraindeformation":
    raise NotImplemented
    pass

def TerrainDeformRandom(x:"real", y:"real", radius:"real", minDelta:"real", maxDelta:"real", duration:"integer", updateInterval:"integer")->"terraindeformation":
    raise NotImplemented
    pass

def TerrainDeformStop(deformation:"terraindeformation", duration:"integer")->"nothing":
    raise NotImplemented
    pass

def TerrainDeformStopAll()->"nothing":
    raise NotImplemented
    pass

def AddSpecialEffect(modelName:"string", x:"real", y:"real")->"effect":
    raise NotImplemented
    pass

def AddSpecialEffectLoc(modelName:"string", where:"location")->"effect":
    raise NotImplemented
    pass

def AddSpecialEffectTarget(modelName:"string", targetWidget:"widget", attachPointName:"string")->"effect":
    raise NotImplemented
    pass

def DestroyEffect(whichEffect:"effect")->"nothing":
    raise NotImplemented
    pass

def AddSpellEffect(abilityString:"string", t:"effecttype", x:"real", y:"real")->"effect":
    raise NotImplemented
    pass

def AddSpellEffectLoc(abilityString:"string", t:"effecttype", where:"location")->"effect":
    raise NotImplemented
    pass

def AddSpellEffectById(abilityId:"integer", t:"effecttype", x:"real", y:"real")->"effect":
    raise NotImplemented
    pass

def AddSpellEffectByIdLoc(abilityId:"integer", t:"effecttype", where:"location")->"effect":
    raise NotImplemented
    pass

def AddSpellEffectTarget(modelName:"string", t:"effecttype", targetWidget:"widget", attachPoint:"string")->"effect":
    raise NotImplemented
    pass

def AddSpellEffectTargetById(abilityId:"integer", t:"effecttype", targetWidget:"widget", attachPoint:"string")->"effect":
    raise NotImplemented
    pass

def AddLightning(codeName:"string", checkVisibility:"boolean", x1:"real", y1:"real", x2:"real", y2:"real")->"lightning":
    raise NotImplemented
    pass

def AddLightningEx(codeName:"string", checkVisibility:"boolean", x1:"real", y1:"real", z1:"real", x2:"real", y2:"real", z2:"real")->"lightning":
    raise NotImplemented
    pass

def DestroyLightning(whichBolt:"lightning")->"boolean":
    raise NotImplemented
    pass

def MoveLightning(whichBolt:"lightning", checkVisibility:"boolean", x1:"real", y1:"real", x2:"real", y2:"real")->"boolean":
    raise NotImplemented
    pass

def MoveLightningEx(whichBolt:"lightning", checkVisibility:"boolean", x1:"real", y1:"real", z1:"real", x2:"real", y2:"real", z2:"real")->"boolean":
    raise NotImplemented
    pass

def GetLightningColorA(whichBolt:"lightning")->"real":
    raise NotImplemented
    pass

def GetLightningColorR(whichBolt:"lightning")->"real":
    raise NotImplemented
    pass

def GetLightningColorG(whichBolt:"lightning")->"real":
    raise NotImplemented
    pass

def GetLightningColorB(whichBolt:"lightning")->"real":
    raise NotImplemented
    pass

def SetLightningColor(whichBolt:"lightning", r:"real", g:"real", b:"real", a:"real")->"boolean":
    raise NotImplemented
    pass

def GetAbilityEffect(abilityString:"string", t:"effecttype", index:"integer")->"string":
    raise NotImplemented
    pass

def GetAbilityEffectById(abilityId:"integer", t:"effecttype", index:"integer")->"string":
    raise NotImplemented
    pass

def GetAbilitySound(abilityString:"string", t:"soundtype")->"string":
    raise NotImplemented
    pass

def GetAbilitySoundById(abilityId:"integer", t:"soundtype")->"string":
    raise NotImplemented
    pass

def GetTerrainCliffLevel(x:"real", y:"real")->"integer":
    raise NotImplemented
    pass

def SetWaterBaseColor(red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def SetWaterDeforms(val:"boolean")->"nothing":
    raise NotImplemented
    pass

def GetTerrainType(x:"real", y:"real")->"integer":
    raise NotImplemented
    pass

def GetTerrainVariance(x:"real", y:"real")->"integer":
    raise NotImplemented
    pass

def SetTerrainType(x:"real", y:"real", terrainType:"integer", variation:"integer", area:"integer", shape:"integer")->"nothing":
    raise NotImplemented
    pass

def IsTerrainPathable(x:"real", y:"real", t:"pathingtype")->"boolean":
    raise NotImplemented
    pass

def SetTerrainPathable(x:"real", y:"real", t:"pathingtype", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def CreateImage(file:"string", sizeX:"real", sizeY:"real", sizeZ:"real", posX:"real", posY:"real", posZ:"real", originX:"real", originY:"real", originZ:"real", imageType:"integer")->"image":
    raise NotImplemented
    pass

def DestroyImage(whichImage:"image")->"nothing":
    raise NotImplemented
    pass

def ShowImage(whichImage:"image", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetImageConstantHeight(whichImage:"image", flag:"boolean", height:"real")->"nothing":
    raise NotImplemented
    pass

def SetImagePosition(whichImage:"image", x:"real", y:"real", z:"real")->"nothing":
    raise NotImplemented
    pass

def SetImageColor(whichImage:"image", red:"integer", green:"integer", blue:"integer", alpha:"integer")->"nothing":
    raise NotImplemented
    pass

def SetImageRender(whichImage:"image", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetImageRenderAlways(whichImage:"image", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetImageAboveWater(whichImage:"image", flag:"boolean", useWaterAlpha:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetImageType(whichImage:"image", imageType:"integer")->"nothing":
    raise NotImplemented
    pass

def CreateUbersplat(x:"real", y:"real", name:"string", red:"integer", green:"integer", blue:"integer", alpha:"integer", forcePaused:"boolean", noBirthTime:"boolean")->"ubersplat":
    raise NotImplemented
    pass

def DestroyUbersplat(whichSplat:"ubersplat")->"nothing":
    raise NotImplemented
    pass

def ResetUbersplat(whichSplat:"ubersplat")->"nothing":
    raise NotImplemented
    pass

def FinishUbersplat(whichSplat:"ubersplat")->"nothing":
    raise NotImplemented
    pass

def ShowUbersplat(whichSplat:"ubersplat", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetUbersplatRender(whichSplat:"ubersplat", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetUbersplatRenderAlways(whichSplat:"ubersplat", flag:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetBlight(whichPlayer:"player", x:"real", y:"real", radius:"real", addBlight:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetBlightRect(whichPlayer:"player", r:"rect", addBlight:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetBlightPoint(whichPlayer:"player", x:"real", y:"real", addBlight:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetBlightLoc(whichPlayer:"player", whichLocation:"location", radius:"real", addBlight:"boolean")->"nothing":
    raise NotImplemented
    pass

def CreateBlightedGoldmine(id:"player", x:"real", y:"real", face:"real")->"unit":
    raise NotImplemented
    pass

def IsPointBlighted(x:"real", y:"real")->"boolean":
    raise NotImplemented
    pass

def SetDoodadAnimation(x:"real", y:"real", radius:"real", doodadID:"integer", nearestOnly:"boolean", animName:"string", animRandom:"boolean")->"nothing":
    raise NotImplemented
    pass

def SetDoodadAnimationRect(r:"rect", doodadID:"integer", animName:"string", animRandom:"boolean")->"nothing":
    raise NotImplemented
    pass

def StartMeleeAI(num:"player", script:"string")->"nothing":
    raise NotImplemented
    pass

def StartCampaignAI(num:"player", script:"string")->"nothing":
    raise NotImplemented
    pass

def CommandAI(num:"player", command:"integer", data:"integer")->"nothing":
    raise NotImplemented
    pass

def PauseCompAI(p:"player", pause:"boolean")->"nothing":
    raise NotImplemented
    pass

def GetAIDifficulty(num:"player")->"aidifficulty":
    raise NotImplemented
    pass

def RemoveGuardPosition(hUnit:"unit")->"nothing":
    raise NotImplemented
    pass

def RecycleGuardPosition(hUnit:"unit")->"nothing":
    raise NotImplemented
    pass

def RemoveAllGuardPositions(num:"player")->"nothing":
    raise NotImplemented
    pass

def Cheat(cheatStr:"string")->"nothing":
    raise NotImplemented
    pass

def IsNoVictoryCheat()->"boolean":
    raise NotImplemented
    pass

def IsNoDefeatCheat()->"boolean":
    raise NotImplemented
    pass

def Preload(filename:"string")->"nothing":
    raise NotImplemented
    pass

def PreloadEnd(timeout:"real")->"nothing":
    raise NotImplemented
    pass

def PreloadStart()->"nothing":
    raise NotImplemented
    pass

def PreloadRefresh()->"nothing":
    raise NotImplemented
    pass

def PreloadEndEx()->"nothing":
    raise NotImplemented
    pass

def PreloadGenClear()->"nothing":
    raise NotImplemented
    pass

def PreloadGenStart()->"nothing":
    raise NotImplemented
    pass

def PreloadGenEnd(filename:"string")->"nothing":
    raise NotImplemented
    pass

def Preloader(filename:"string")->"nothing":
    raise NotImplemented
    pass
