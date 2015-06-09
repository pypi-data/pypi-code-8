
# Blizzard.j implementation
from jass_runtime.common_j import *

bj_PI = 3.14159
bj_E = 2.71828
bj_CELLWIDTH = 128.0
bj_CLIFFHEIGHT = 128.0
bj_UNIT_FACING = 270.0
bj_RADTODEG = 180.0 / bj_PI
bj_DEGTORAD = bj_PI / 180.0
bj_TEXT_DELAY_QUEST = 20.0
bj_TEXT_DELAY_QUESTUPDATE = 20.0
bj_TEXT_DELAY_QUESTDONE = 20.0
bj_TEXT_DELAY_QUESTFAILED = 20.0
bj_TEXT_DELAY_QUESTREQUIREMENT = 20.0
bj_TEXT_DELAY_MISSIONFAILED = 20.0
bj_TEXT_DELAY_ALWAYSHINT = 12.0
bj_TEXT_DELAY_HINT = 12.0
bj_TEXT_DELAY_SECRET = 10.0
bj_TEXT_DELAY_UNITACQUIRED = 15.0
bj_TEXT_DELAY_UNITAVAILABLE = 10.0
bj_TEXT_DELAY_ITEMACQUIRED = 10.0
bj_TEXT_DELAY_WARNING = 12.0
bj_QUEUE_DELAY_QUEST = 5.0
bj_QUEUE_DELAY_HINT = 5.0
bj_QUEUE_DELAY_SECRET = 3.0
bj_HANDICAP_EASY = 60.0
bj_GAME_STARTED_THRESHOLD = 0.01
bj_WAIT_FOR_COND_MIN_INTERVAL = 0.1
bj_POLLED_WAIT_INTERVAL = 0.1
bj_POLLED_WAIT_SKIP_THRESHOLD = 2.0
bj_MAX_INVENTORY = 6
bj_MAX_PLAYERS = 12
bj_PLAYER_NEUTRAL_VICTIM = 13
bj_PLAYER_NEUTRAL_EXTRA = 14
bj_MAX_PLAYER_SLOTS = 16
bj_MAX_SKELETONS = 25
bj_MAX_STOCK_ITEM_SLOTS = 11
bj_MAX_STOCK_UNIT_SLOTS = 11
bj_MAX_ITEM_LEVEL = 10
bj_TOD_DAWN = 6.0
bj_TOD_DUSK = 18.0
bj_MELEE_STARTING_TOD = 8.0
bj_MELEE_STARTING_GOLD_V0 = 750
bj_MELEE_STARTING_GOLD_V1 = 500
bj_MELEE_STARTING_LUMBER_V0 = 200
bj_MELEE_STARTING_LUMBER_V1 = 150
bj_MELEE_STARTING_HERO_TOKENS = 1
bj_MELEE_HERO_LIMIT = 3
bj_MELEE_HERO_TYPE_LIMIT = 1
bj_MELEE_MINE_SEARCH_RADIUS = 2000
bj_MELEE_CLEAR_UNITS_RADIUS = 1500
bj_MELEE_CRIPPLE_TIMEOUT = 120.0
bj_MELEE_CRIPPLE_MSG_DURATION = 20.0
bj_MELEE_MAX_TWINKED_HEROES_V0 = 3
bj_MELEE_MAX_TWINKED_HEROES_V1 = 1
bj_CREEP_ITEM_DELAY = 0.5
bj_STOCK_RESTOCK_INITIAL_DELAY = 120
bj_STOCK_RESTOCK_INTERVAL = 30
bj_STOCK_MAX_ITERATIONS = 20
bj_MAX_DEST_IN_REGION_EVENTS = 64
bj_CAMERA_MIN_FARZ = 100
bj_CAMERA_DEFAULT_DISTANCE = 1650
bj_CAMERA_DEFAULT_FARZ = 5000
bj_CAMERA_DEFAULT_AOA = 304
bj_CAMERA_DEFAULT_FOV = 70
bj_CAMERA_DEFAULT_ROLL = 0
bj_CAMERA_DEFAULT_ROTATION = 90
bj_RESCUE_PING_TIME = 2.0
bj_NOTHING_SOUND_DURATION = 5.0
bj_TRANSMISSION_PING_TIME = 1.0
bj_TRANSMISSION_IND_RED = 255
bj_TRANSMISSION_IND_BLUE = 255
bj_TRANSMISSION_IND_GREEN = 255
bj_TRANSMISSION_IND_ALPHA = 255
bj_TRANSMISSION_PORT_HANGTIME = 1.5
bj_CINEMODE_INTERFACEFADE = 0.5
bj_CINEMODE_GAMESPEED = MAP_SPEED_NORMAL
bj_CINEMODE_VOLUME_UNITMOVEMENT = 0.4
bj_CINEMODE_VOLUME_UNITSOUNDS = 0.0
bj_CINEMODE_VOLUME_COMBAT = 0.4
bj_CINEMODE_VOLUME_SPELLS = 0.4
bj_CINEMODE_VOLUME_UI = 0.0
bj_CINEMODE_VOLUME_MUSIC = 0.55
bj_CINEMODE_VOLUME_AMBIENTSOUNDS = 1.0
bj_CINEMODE_VOLUME_FIRE = 0.6
bj_SPEECH_VOLUME_UNITMOVEMENT = 0.25
bj_SPEECH_VOLUME_UNITSOUNDS = 0.0
bj_SPEECH_VOLUME_COMBAT = 0.25
bj_SPEECH_VOLUME_SPELLS = 0.25
bj_SPEECH_VOLUME_UI = 0.0
bj_SPEECH_VOLUME_MUSIC = 0.55
bj_SPEECH_VOLUME_AMBIENTSOUNDS = 1.0
bj_SPEECH_VOLUME_FIRE = 0.6
bj_SMARTPAN_TRESHOLD_PAN = 500
bj_SMARTPAN_TRESHOLD_SNAP = 3500
bj_MAX_QUEUED_TRIGGERS = 100
bj_QUEUED_TRIGGER_TIMEOUT = 180.0
bj_CAMPAIGN_INDEX_T = 0
bj_CAMPAIGN_INDEX_H = 1
bj_CAMPAIGN_INDEX_U = 2
bj_CAMPAIGN_INDEX_O = 3
bj_CAMPAIGN_INDEX_N = 4
bj_CAMPAIGN_INDEX_XN = 5
bj_CAMPAIGN_INDEX_XH = 6
bj_CAMPAIGN_INDEX_XU = 7
bj_CAMPAIGN_INDEX_XO = 8
bj_CAMPAIGN_OFFSET_T = 0
bj_CAMPAIGN_OFFSET_H = 1
bj_CAMPAIGN_OFFSET_U = 2
bj_CAMPAIGN_OFFSET_O = 3
bj_CAMPAIGN_OFFSET_N = 4
bj_CAMPAIGN_OFFSET_XN = 0
bj_CAMPAIGN_OFFSET_XH = 1
bj_CAMPAIGN_OFFSET_XU = 2
bj_CAMPAIGN_OFFSET_XO = 3
bj_MISSION_INDEX_T00 = bj_CAMPAIGN_OFFSET_T * 1000 + 0
bj_MISSION_INDEX_T01 = bj_CAMPAIGN_OFFSET_T * 1000 + 1
bj_MISSION_INDEX_H00 = bj_CAMPAIGN_OFFSET_H * 1000 + 0
bj_MISSION_INDEX_H01 = bj_CAMPAIGN_OFFSET_H * 1000 + 1
bj_MISSION_INDEX_H02 = bj_CAMPAIGN_OFFSET_H * 1000 + 2
bj_MISSION_INDEX_H03 = bj_CAMPAIGN_OFFSET_H * 1000 + 3
bj_MISSION_INDEX_H04 = bj_CAMPAIGN_OFFSET_H * 1000 + 4
bj_MISSION_INDEX_H05 = bj_CAMPAIGN_OFFSET_H * 1000 + 5
bj_MISSION_INDEX_H06 = bj_CAMPAIGN_OFFSET_H * 1000 + 6
bj_MISSION_INDEX_H07 = bj_CAMPAIGN_OFFSET_H * 1000 + 7
bj_MISSION_INDEX_H08 = bj_CAMPAIGN_OFFSET_H * 1000 + 8
bj_MISSION_INDEX_H09 = bj_CAMPAIGN_OFFSET_H * 1000 + 9
bj_MISSION_INDEX_H10 = bj_CAMPAIGN_OFFSET_H * 1000 + 10
bj_MISSION_INDEX_H11 = bj_CAMPAIGN_OFFSET_H * 1000 + 11
bj_MISSION_INDEX_U00 = bj_CAMPAIGN_OFFSET_U * 1000 + 0
bj_MISSION_INDEX_U01 = bj_CAMPAIGN_OFFSET_U * 1000 + 1
bj_MISSION_INDEX_U02 = bj_CAMPAIGN_OFFSET_U * 1000 + 2
bj_MISSION_INDEX_U03 = bj_CAMPAIGN_OFFSET_U * 1000 + 3
bj_MISSION_INDEX_U05 = bj_CAMPAIGN_OFFSET_U * 1000 + 4
bj_MISSION_INDEX_U07 = bj_CAMPAIGN_OFFSET_U * 1000 + 5
bj_MISSION_INDEX_U08 = bj_CAMPAIGN_OFFSET_U * 1000 + 6
bj_MISSION_INDEX_U09 = bj_CAMPAIGN_OFFSET_U * 1000 + 7
bj_MISSION_INDEX_U10 = bj_CAMPAIGN_OFFSET_U * 1000 + 8
bj_MISSION_INDEX_U11 = bj_CAMPAIGN_OFFSET_U * 1000 + 9
bj_MISSION_INDEX_O00 = bj_CAMPAIGN_OFFSET_O * 1000 + 0
bj_MISSION_INDEX_O01 = bj_CAMPAIGN_OFFSET_O * 1000 + 1
bj_MISSION_INDEX_O02 = bj_CAMPAIGN_OFFSET_O * 1000 + 2
bj_MISSION_INDEX_O03 = bj_CAMPAIGN_OFFSET_O * 1000 + 3
bj_MISSION_INDEX_O04 = bj_CAMPAIGN_OFFSET_O * 1000 + 4
bj_MISSION_INDEX_O05 = bj_CAMPAIGN_OFFSET_O * 1000 + 5
bj_MISSION_INDEX_O06 = bj_CAMPAIGN_OFFSET_O * 1000 + 6
bj_MISSION_INDEX_O07 = bj_CAMPAIGN_OFFSET_O * 1000 + 7
bj_MISSION_INDEX_O08 = bj_CAMPAIGN_OFFSET_O * 1000 + 8
bj_MISSION_INDEX_O09 = bj_CAMPAIGN_OFFSET_O * 1000 + 9
bj_MISSION_INDEX_O10 = bj_CAMPAIGN_OFFSET_O * 1000 + 10
bj_MISSION_INDEX_N00 = bj_CAMPAIGN_OFFSET_N * 1000 + 0
bj_MISSION_INDEX_N01 = bj_CAMPAIGN_OFFSET_N * 1000 + 1
bj_MISSION_INDEX_N02 = bj_CAMPAIGN_OFFSET_N * 1000 + 2
bj_MISSION_INDEX_N03 = bj_CAMPAIGN_OFFSET_N * 1000 + 3
bj_MISSION_INDEX_N04 = bj_CAMPAIGN_OFFSET_N * 1000 + 4
bj_MISSION_INDEX_N05 = bj_CAMPAIGN_OFFSET_N * 1000 + 5
bj_MISSION_INDEX_N06 = bj_CAMPAIGN_OFFSET_N * 1000 + 6
bj_MISSION_INDEX_N07 = bj_CAMPAIGN_OFFSET_N * 1000 + 7
bj_MISSION_INDEX_N08 = bj_CAMPAIGN_OFFSET_N * 1000 + 8
bj_MISSION_INDEX_N09 = bj_CAMPAIGN_OFFSET_N * 1000 + 9
bj_MISSION_INDEX_XN00 = bj_CAMPAIGN_OFFSET_XN * 1000 + 0
bj_MISSION_INDEX_XN01 = bj_CAMPAIGN_OFFSET_XN * 1000 + 1
bj_MISSION_INDEX_XN02 = bj_CAMPAIGN_OFFSET_XN * 1000 + 2
bj_MISSION_INDEX_XN03 = bj_CAMPAIGN_OFFSET_XN * 1000 + 3
bj_MISSION_INDEX_XN04 = bj_CAMPAIGN_OFFSET_XN * 1000 + 4
bj_MISSION_INDEX_XN05 = bj_CAMPAIGN_OFFSET_XN * 1000 + 5
bj_MISSION_INDEX_XN06 = bj_CAMPAIGN_OFFSET_XN * 1000 + 6
bj_MISSION_INDEX_XN07 = bj_CAMPAIGN_OFFSET_XN * 1000 + 7
bj_MISSION_INDEX_XN08 = bj_CAMPAIGN_OFFSET_XN * 1000 + 8
bj_MISSION_INDEX_XN09 = bj_CAMPAIGN_OFFSET_XN * 1000 + 9
bj_MISSION_INDEX_XN10 = bj_CAMPAIGN_OFFSET_XN * 1000 + 10
bj_MISSION_INDEX_XH00 = bj_CAMPAIGN_OFFSET_XH * 1000 + 0
bj_MISSION_INDEX_XH01 = bj_CAMPAIGN_OFFSET_XH * 1000 + 1
bj_MISSION_INDEX_XH02 = bj_CAMPAIGN_OFFSET_XH * 1000 + 2
bj_MISSION_INDEX_XH03 = bj_CAMPAIGN_OFFSET_XH * 1000 + 3
bj_MISSION_INDEX_XH04 = bj_CAMPAIGN_OFFSET_XH * 1000 + 4
bj_MISSION_INDEX_XH05 = bj_CAMPAIGN_OFFSET_XH * 1000 + 5
bj_MISSION_INDEX_XH06 = bj_CAMPAIGN_OFFSET_XH * 1000 + 6
bj_MISSION_INDEX_XH07 = bj_CAMPAIGN_OFFSET_XH * 1000 + 7
bj_MISSION_INDEX_XH08 = bj_CAMPAIGN_OFFSET_XH * 1000 + 8
bj_MISSION_INDEX_XH09 = bj_CAMPAIGN_OFFSET_XH * 1000 + 9
bj_MISSION_INDEX_XU00 = bj_CAMPAIGN_OFFSET_XU * 1000 + 0
bj_MISSION_INDEX_XU01 = bj_CAMPAIGN_OFFSET_XU * 1000 + 1
bj_MISSION_INDEX_XU02 = bj_CAMPAIGN_OFFSET_XU * 1000 + 2
bj_MISSION_INDEX_XU03 = bj_CAMPAIGN_OFFSET_XU * 1000 + 3
bj_MISSION_INDEX_XU04 = bj_CAMPAIGN_OFFSET_XU * 1000 + 4
bj_MISSION_INDEX_XU05 = bj_CAMPAIGN_OFFSET_XU * 1000 + 5
bj_MISSION_INDEX_XU06 = bj_CAMPAIGN_OFFSET_XU * 1000 + 6
bj_MISSION_INDEX_XU07 = bj_CAMPAIGN_OFFSET_XU * 1000 + 7
bj_MISSION_INDEX_XU08 = bj_CAMPAIGN_OFFSET_XU * 1000 + 8
bj_MISSION_INDEX_XU09 = bj_CAMPAIGN_OFFSET_XU * 1000 + 9
bj_MISSION_INDEX_XU10 = bj_CAMPAIGN_OFFSET_XU * 1000 + 10
bj_MISSION_INDEX_XU11 = bj_CAMPAIGN_OFFSET_XU * 1000 + 11
bj_MISSION_INDEX_XU12 = bj_CAMPAIGN_OFFSET_XU * 1000 + 12
bj_MISSION_INDEX_XU13 = bj_CAMPAIGN_OFFSET_XU * 1000 + 13
bj_MISSION_INDEX_XO00 = bj_CAMPAIGN_OFFSET_XO * 1000 + 0
bj_CINEMATICINDEX_TOP = 0
bj_CINEMATICINDEX_HOP = 1
bj_CINEMATICINDEX_HED = 2
bj_CINEMATICINDEX_OOP = 3
bj_CINEMATICINDEX_OED = 4
bj_CINEMATICINDEX_UOP = 5
bj_CINEMATICINDEX_UED = 6
bj_CINEMATICINDEX_NOP = 7
bj_CINEMATICINDEX_NED = 8
bj_CINEMATICINDEX_XOP = 9
bj_CINEMATICINDEX_XED = 10
bj_ALLIANCE_UNALLIED = 0
bj_ALLIANCE_UNALLIED_VISION = 1
bj_ALLIANCE_ALLIED = 2
bj_ALLIANCE_ALLIED_VISION = 3
bj_ALLIANCE_ALLIED_UNITS = 4
bj_ALLIANCE_ALLIED_ADVUNITS = 5
bj_ALLIANCE_NEUTRAL = 6
bj_ALLIANCE_NEUTRAL_VISION = 7
bj_KEYEVENTTYPE_DEPRESS = 0
bj_KEYEVENTTYPE_RELEASE = 1
bj_KEYEVENTKEY_LEFT = 0
bj_KEYEVENTKEY_RIGHT = 1
bj_KEYEVENTKEY_DOWN = 2
bj_KEYEVENTKEY_UP = 3
bj_TIMETYPE_ADD = 0
bj_TIMETYPE_SET = 1
bj_TIMETYPE_SUB = 2
bj_CAMERABOUNDS_ADJUST_ADD = 0
bj_CAMERABOUNDS_ADJUST_SUB = 1
bj_QUESTTYPE_REQ_DISCOVERED = 0
bj_QUESTTYPE_REQ_UNDISCOVERED = 1
bj_QUESTTYPE_OPT_DISCOVERED = 2
bj_QUESTTYPE_OPT_UNDISCOVERED = 3
bj_QUESTMESSAGE_DISCOVERED = 0
bj_QUESTMESSAGE_UPDATED = 1
bj_QUESTMESSAGE_COMPLETED = 2
bj_QUESTMESSAGE_FAILED = 3
bj_QUESTMESSAGE_REQUIREMENT = 4
bj_QUESTMESSAGE_MISSIONFAILED = 5
bj_QUESTMESSAGE_ALWAYSHINT = 6
bj_QUESTMESSAGE_HINT = 7
bj_QUESTMESSAGE_SECRET = 8
bj_QUESTMESSAGE_UNITACQUIRED = 9
bj_QUESTMESSAGE_UNITAVAILABLE = 10
bj_QUESTMESSAGE_ITEMACQUIRED = 11
bj_QUESTMESSAGE_WARNING = 12
bj_SORTTYPE_SORTBYVALUE = 0
bj_SORTTYPE_SORTBYPLAYER = 1
bj_SORTTYPE_SORTBYLABEL = 2
bj_CINEFADETYPE_FADEIN = 0
bj_CINEFADETYPE_FADEOUT = 1
bj_CINEFADETYPE_FADEOUTIN = 2
bj_REMOVEBUFFS_POSITIVE = 0
bj_REMOVEBUFFS_NEGATIVE = 1
bj_REMOVEBUFFS_ALL = 2
bj_REMOVEBUFFS_NONTLIFE = 3
bj_BUFF_POLARITY_POSITIVE = 0
bj_BUFF_POLARITY_NEGATIVE = 1
bj_BUFF_POLARITY_EITHER = 2
bj_BUFF_RESIST_MAGIC = 0
bj_BUFF_RESIST_PHYSICAL = 1
bj_BUFF_RESIST_EITHER = 2
bj_BUFF_RESIST_BOTH = 3
bj_HEROSTAT_STR = 0
bj_HEROSTAT_AGI = 1
bj_HEROSTAT_INT = 2
bj_MODIFYMETHOD_ADD = 0
bj_MODIFYMETHOD_SUB = 1
bj_MODIFYMETHOD_SET = 2
bj_UNIT_STATE_METHOD_ABSOLUTE = 0
bj_UNIT_STATE_METHOD_RELATIVE = 1
bj_UNIT_STATE_METHOD_DEFAULTS = 2
bj_UNIT_STATE_METHOD_MAXIMUM = 3
bj_GATEOPERATION_CLOSE = 0
bj_GATEOPERATION_OPEN = 1
bj_GATEOPERATION_DESTROY = 2
bj_GAMECACHE_BOOLEAN = 0
bj_GAMECACHE_INTEGER = 1
bj_GAMECACHE_REAL = 2
bj_GAMECACHE_UNIT = 3
bj_GAMECACHE_STRING = 4
bj_HASHTABLE_BOOLEAN = 0
bj_HASHTABLE_INTEGER = 1
bj_HASHTABLE_REAL = 2
bj_HASHTABLE_STRING = 3
bj_HASHTABLE_HANDLE = 4
bj_ITEM_STATUS_HIDDEN = 0
bj_ITEM_STATUS_OWNED = 1
bj_ITEM_STATUS_INVULNERABLE = 2
bj_ITEM_STATUS_POWERUP = 3
bj_ITEM_STATUS_SELLABLE = 4
bj_ITEM_STATUS_PAWNABLE = 5
bj_ITEMCODE_STATUS_POWERUP = 0
bj_ITEMCODE_STATUS_SELLABLE = 1
bj_ITEMCODE_STATUS_PAWNABLE = 2
bj_MINIMAPPINGSTYLE_SIMPLE = 0
bj_MINIMAPPINGSTYLE_FLASHY = 1
bj_MINIMAPPINGSTYLE_ATTACK = 2
bj_CORPSE_MAX_DEATH_TIME = 8.0
bj_CORPSETYPE_FLESH = 0
bj_CORPSETYPE_BONE = 1
bj_ELEVATOR_BLOCKER_CODE = 1146381680
bj_ELEVATOR_CODE01 = 1146384998
bj_ELEVATOR_CODE02 = 1146385016
bj_ELEVATOR_WALL_TYPE_ALL = 0
bj_ELEVATOR_WALL_TYPE_EAST = 1
bj_ELEVATOR_WALL_TYPE_NORTH = 2
bj_ELEVATOR_WALL_TYPE_SOUTH = 3
bj_ELEVATOR_WALL_TYPE_WEST = 4
bj_FORCE_ALL_PLAYERS = None
bj_FORCE_PLAYER = [None]*8192
bj_MELEE_MAX_TWINKED_HEROES = 0
bj_mapInitialPlayableArea = None
bj_mapInitialCameraBounds = None
bj_forLoopAIndex = 0
bj_forLoopBIndex = 0
bj_forLoopAIndexEnd = 0
bj_forLoopBIndexEnd = 0
bj_slotControlReady = False
bj_slotControlUsed = [None]*8192
bj_slotControl = [None]*8192
bj_gameStartedTimer = None
bj_gameStarted = False
bj_volumeGroupsTimer = CreateTimer()
bj_isSinglePlayer = False
bj_dncSoundsDay = None
bj_dncSoundsNight = None
bj_dayAmbientSound = None
bj_nightAmbientSound = None
bj_dncSoundsDawn = None
bj_dncSoundsDusk = None
bj_dawnSound = None
bj_duskSound = None
bj_useDawnDuskSounds = True
bj_dncIsDaytime = False
bj_rescueSound = None
bj_questDiscoveredSound = None
bj_questUpdatedSound = None
bj_questCompletedSound = None
bj_questFailedSound = None
bj_questHintSound = None
bj_questSecretSound = None
bj_questItemAcquiredSound = None
bj_questWarningSound = None
bj_victoryDialogSound = None
bj_defeatDialogSound = None
bj_stockItemPurchased = None
bj_stockUpdateTimer = None
bj_stockAllowedPermanent = [None]*8192
bj_stockAllowedCharged = [None]*8192
bj_stockAllowedArtifact = [None]*8192
bj_stockPickedItemLevel = 0
bj_stockPickedItemType = None
bj_meleeVisibilityTrained = None
bj_meleeVisibilityIsDay = True
bj_meleeGrantHeroItems = False
bj_meleeNearestMineToLoc = None
bj_meleeNearestMine = None
bj_meleeNearestMineDist = 0.0
bj_meleeGameOver = False
bj_meleeDefeated = [None]*8192
bj_meleeVictoried = [None]*8192
bj_ghoul = [None]*8192
bj_crippledTimer = [None]*8192
bj_crippledTimerWindows = [None]*8192
bj_playerIsCrippled = [None]*8192
bj_playerIsExposed = [None]*8192
bj_finishSoonAllExposed = False
bj_finishSoonTimerDialog = None
bj_meleeTwinkedHeroes = [None]*8192
bj_rescueUnitBehavior = None
bj_rescueChangeColorUnit = True
bj_rescueChangeColorBldg = True
bj_cineSceneEndingTimer = None
bj_cineSceneLastSound = None
bj_cineSceneBeingSkipped = None
bj_cineModePriorSpeed = MAP_SPEED_NORMAL
bj_cineModePriorFogSetting = False
bj_cineModePriorMaskSetting = False
bj_cineModeAlreadyIn = False
bj_cineModePriorDawnDusk = False
bj_cineModeSavedSeed = 0
bj_cineFadeFinishTimer = None
bj_cineFadeContinueTimer = None
bj_cineFadeContinueRed = 0
bj_cineFadeContinueGreen = 0
bj_cineFadeContinueBlue = 0
bj_cineFadeContinueTrans = 0
bj_cineFadeContinueDuration = 0
bj_cineFadeContinueTex = ""
bj_queuedExecTotal = 0
bj_queuedExecTriggers = [None]*8192
bj_queuedExecUseConds = [None]*8192
bj_queuedExecTimeoutTimer = CreateTimer()
bj_queuedExecTimeout = None
bj_destInRegionDiesCount = 0
bj_destInRegionDiesTrig = None
bj_groupCountUnits = 0
bj_forceCountPlayers = 0
bj_groupEnumTypeId = 0
bj_groupEnumOwningPlayer = None
bj_groupAddGroupDest = None
bj_groupRemoveGroupDest = None
bj_groupRandomConsidered = 0
bj_groupRandomCurrentPick = None
bj_groupLastCreatedDest = None
bj_randomSubGroupGroup = None
bj_randomSubGroupWant = 0
bj_randomSubGroupTotal = 0
bj_randomSubGroupChance = 0
bj_destRandomConsidered = 0
bj_destRandomCurrentPick = None
bj_elevatorWallBlocker = None
bj_elevatorNeighbor = None
bj_itemRandomConsidered = 0
bj_itemRandomCurrentPick = None
bj_forceRandomConsidered = 0
bj_forceRandomCurrentPick = None
bj_makeUnitRescuableUnit = None
bj_makeUnitRescuableFlag = True
bj_pauseAllUnitsFlag = True
bj_enumDestructableCenter = None
bj_enumDestructableRadius = 0
bj_setPlayerTargetColor = None
bj_isUnitGroupDeadResult = True
bj_isUnitGroupEmptyResult = True
bj_isUnitGroupInRectResult = True
bj_isUnitGroupInRectRect = None
bj_changeLevelShowScores = False
bj_changeLevelMapName = None
bj_suspendDecayFleshGroup = CreateGroup()
bj_suspendDecayBoneGroup = CreateGroup()
bj_delayedSuspendDecayTimer = CreateTimer()
bj_delayedSuspendDecayTrig = None
bj_livingPlayerUnitsTypeId = 0
bj_lastDyingWidget = None
bj_randDistCount = 0
bj_randDistID = [None]*8192
bj_randDistChance = [None]*8192
bj_lastCreatedUnit = None
bj_lastCreatedItem = None
bj_lastRemovedItem = None
bj_lastHauntedGoldMine = None
bj_lastCreatedDestructable = None
bj_lastCreatedGroup = CreateGroup()
bj_lastCreatedFogModifier = None
bj_lastCreatedEffect = None
bj_lastCreatedWeatherEffect = None
bj_lastCreatedTerrainDeformation = None
bj_lastCreatedQuest = None
bj_lastCreatedQuestItem = None
bj_lastCreatedDefeatCondition = None
bj_lastStartedTimer = CreateTimer()
bj_lastCreatedTimerDialog = None
bj_lastCreatedLeaderboard = None
bj_lastCreatedMultiboard = None
bj_lastPlayedSound = None
bj_lastPlayedMusic = ""
bj_lastTransmissionDuration = 0
bj_lastCreatedGameCache = None
bj_lastCreatedHashtable = None
bj_lastLoadedUnit = None
bj_lastCreatedButton = None
bj_lastReplacedUnit = None
bj_lastCreatedTextTag = None
bj_lastCreatedLightning = None
bj_lastCreatedImage = None
bj_lastCreatedUbersplat = None
filterIssueHauntOrderAtLocBJ = None
filterEnumDestructablesInCircleBJ = None
filterGetUnitsInRectOfPlayer = None
filterGetUnitsOfTypeIdAll = None
filterGetUnitsOfPlayerAndTypeId = None
filterMeleeTrainedUnitIsHeroBJ = None
filterLivingPlayerUnitsOfTypeId = None
bj_wantDestroyGroup = False

def BJDebugMsg(msg:"string")->"nothing":
    i = 0
    while True:
        DisplayTimedTextToPlayer(Player(i), 0, 0, 60, msg)
        i = i + 1
        if i == bj_MAX_PLAYERS:
            break
        pass

    pass

def RMinBJ(a:"real", b:"real")->"real":
    if ( a < b ):
        return a
    else:
        return b
    pass

def RMaxBJ(a:"real", b:"real")->"real":
    if ( a < b ):
        return b
    else:
        return a
    pass

def RAbsBJ(a:"real")->"real":
    if ( a >= 0 ):
        return a
    else:
        return - a
    pass

def RSignBJ(a:"real")->"real":
    if ( a >= 0.0 ):
        return 1.0
    else:
        return - 1.0
    pass

def IMinBJ(a:"integer", b:"integer")->"integer":
    if ( a < b ):
        return a
    else:
        return b
    pass

def IMaxBJ(a:"integer", b:"integer")->"integer":
    if ( a < b ):
        return b
    else:
        return a
    pass

def IAbsBJ(a:"integer")->"integer":
    if ( a >= 0 ):
        return a
    else:
        return - a
    pass

def ISignBJ(a:"integer")->"integer":
    if ( a >= 0 ):
        return 1
    else:
        return - 1
    pass

def SinBJ(degrees:"real")->"real":
    return Sin(degrees * bj_DEGTORAD)
    pass

def CosBJ(degrees:"real")->"real":
    return Cos(degrees * bj_DEGTORAD)
    pass

def TanBJ(degrees:"real")->"real":
    return Tan(degrees * bj_DEGTORAD)
    pass

def AsinBJ(degrees:"real")->"real":
    return Asin(degrees) * bj_RADTODEG
    pass

def AcosBJ(degrees:"real")->"real":
    return Acos(degrees) * bj_RADTODEG
    pass

def AtanBJ(degrees:"real")->"real":
    return Atan(degrees) * bj_RADTODEG
    pass

def Atan2BJ(y:"real", x:"real")->"real":
    return Atan2(y, x) * bj_RADTODEG
    pass

def AngleBetweenPoints(locA:"location", locB:"location")->"real":
    return bj_RADTODEG * Atan2(GetLocationY(locB) - GetLocationY(locA), GetLocationX(locB) - GetLocationX(locA))
    pass

def DistanceBetweenPoints(locA:"location", locB:"location")->"real":
    dx = GetLocationX(locB) - GetLocationX(locA)
    dy = GetLocationY(locB) - GetLocationY(locA)
    return SquareRoot(dx * dx + dy * dy)
    pass

def PolarProjectionBJ(source:"location", dist:"real", angle:"real")->"location":
    x = GetLocationX(source) + dist * Cos(angle * bj_DEGTORAD)
    y = GetLocationY(source) + dist * Sin(angle * bj_DEGTORAD)
    return Location(x, y)
    pass

def GetRandomDirectionDeg()->"real":
    return GetRandomReal(0, 360)
    pass

def GetRandomPercentageBJ()->"real":
    return GetRandomReal(0, 100)
    pass

def GetRandomLocInRect(whichRect:"rect")->"location":
    return Location(GetRandomReal(GetRectMinX(whichRect), GetRectMaxX(whichRect)), GetRandomReal(GetRectMinY(whichRect), GetRectMaxY(whichRect)))
    pass

def ModuloInteger(dividend:"integer", divisor:"integer")->"integer":
    modulus = dividend - ( dividend / divisor ) * divisor
    if ( modulus < 0 ):
        modulus = modulus + divisor
    return modulus
    pass

def ModuloReal(dividend:"real", divisor:"real")->"real":
    modulus = dividend - I2R(R2I(dividend / divisor)) * divisor
    if ( modulus < 0 ):
        modulus = modulus + divisor
    return modulus
    pass

def OffsetLocation(loc:"location", dx:"real", dy:"real")->"location":
    return Location(GetLocationX(loc) + dx, GetLocationY(loc) + dy)
    pass

def OffsetRectBJ(r:"rect", dx:"real", dy:"real")->"rect":
    return Rect(GetRectMinX(r) + dx, GetRectMinY(r) + dy, GetRectMaxX(r) + dx, GetRectMaxY(r) + dy)
    pass

def RectFromCenterSizeBJ(center:"location", width:"real", height:"real")->"rect":
    x = GetLocationX(center)
    y = GetLocationY(center)
    return Rect(x - width * 0.5, y - height * 0.5, x + width * 0.5, y + height * 0.5)
    pass

def RectContainsCoords(r:"rect", x:"real", y:"real")->"boolean":
    return ( GetRectMinX(r) <= x ) and ( x <= GetRectMaxX(r) ) and ( GetRectMinY(r) <= y ) and ( y <= GetRectMaxY(r) )
    pass

def RectContainsLoc(r:"rect", loc:"location")->"boolean":
    return RectContainsCoords(r, GetLocationX(loc), GetLocationY(loc))
    pass

def RectContainsUnit(r:"rect", whichUnit:"unit")->"boolean":
    return RectContainsCoords(r, GetUnitX(whichUnit), GetUnitY(whichUnit))
    pass

def RectContainsItem(whichItem:"item", r:"rect")->"boolean":
    if ( whichItem == None ):
        return False
    if ( IsItemOwned(whichItem) ):
        return False
    return RectContainsCoords(r, GetItemX(whichItem), GetItemY(whichItem))
    pass

def ConditionalTriggerExecute(trig:"trigger")->"nothing":
    if TriggerEvaluate(trig):
        TriggerExecute(trig)
    pass

def TriggerExecuteBJ(trig:"trigger", checkConditions:"boolean")->"boolean":
    if checkConditions:
        if not(TriggerEvaluate(trig)):
            return False
    TriggerExecute(trig)
    return True
    pass

def PostTriggerExecuteBJ(trig:"trigger", checkConditions:"boolean")->"boolean":
    if checkConditions:
        if not(TriggerEvaluate(trig)):
            return False
    TriggerRegisterTimerEvent(trig, 0, False)
    return True
    pass

def QueuedTriggerCheck()->"nothing":
    s = "TrigQueue Check "
    i = None
    i = 0
    while True:
        if i >= bj_queuedExecTotal:
            break
        s = s + "q["  + I2S(i) + "]="
        if ( bj_queuedExecTriggers[i] == None ):
            s = s + "null "
        else:
            s = s + "x "
        i = i + 1
        pass

    s = s + "("  + I2S(bj_queuedExecTotal) + " total)"
    DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, 600, s)
    pass

def QueuedTriggerGetIndex(trig:"trigger")->"integer":
    index = 0
    while True:
        if index >= bj_queuedExecTotal:
            break
        if ( bj_queuedExecTriggers[index] == trig ):
            return index
        index = index + 1
        pass

    return - 1
    pass

def QueuedTriggerRemoveByIndex(trigIndex:"integer")->"boolean":
    global bj_queuedExecTotal
    index = None
    if ( trigIndex >= bj_queuedExecTotal ):
        return False
    bj_queuedExecTotal = bj_queuedExecTotal - 1
    index = trigIndex
    while True:
        if index >= bj_queuedExecTotal:
            break
        bj_queuedExecTriggers[index] = bj_queuedExecTriggers[index + 1]
        bj_queuedExecUseConds[index] = bj_queuedExecUseConds[index + 1]
        index = index + 1
        pass

    return True
    pass

def QueuedTriggerAttemptExec()->"boolean":
    while True:
        if bj_queuedExecTotal == 0:
            break
        if TriggerExecuteBJ(bj_queuedExecTriggers[0], bj_queuedExecUseConds[0]):
            TimerStart(bj_queuedExecTimeoutTimer, bj_QUEUED_TRIGGER_TIMEOUT, False, None)
            return True
        QueuedTriggerRemoveByIndex(0)
        pass

    return False
    pass

def QueuedTriggerAddBJ(trig:"trigger", checkConditions:"boolean")->"boolean":
    global bj_queuedExecTotal
    if ( bj_queuedExecTotal >= bj_MAX_QUEUED_TRIGGERS ):
        return False
    bj_queuedExecTriggers[bj_queuedExecTotal] = trig
    bj_queuedExecUseConds[bj_queuedExecTotal] = checkConditions
    bj_queuedExecTotal = bj_queuedExecTotal + 1
    if ( bj_queuedExecTotal == 1 ):
        QueuedTriggerAttemptExec()
    return True
    pass

def QueuedTriggerRemoveBJ(trig:"trigger")->"nothing":
    index = None
    trigIndex = None
    trigExecuted = None
    trigIndex = QueuedTriggerGetIndex(trig)
    if ( trigIndex == - 1 ):
        pass

    QueuedTriggerRemoveByIndex(trigIndex)
    if ( trigIndex == 0 ):
        PauseTimer(bj_queuedExecTimeoutTimer)
        QueuedTriggerAttemptExec()
    pass

def QueuedTriggerDoneBJ()->"nothing":
    index = None
    if ( bj_queuedExecTotal <= 0 ):
        pass

    QueuedTriggerRemoveByIndex(0)
    PauseTimer(bj_queuedExecTimeoutTimer)
    QueuedTriggerAttemptExec()
    pass

def QueuedTriggerClearBJ()->"nothing":
    global bj_queuedExecTotal
    PauseTimer(bj_queuedExecTimeoutTimer)
    bj_queuedExecTotal = 0
    pass

def QueuedTriggerClearInactiveBJ()->"nothing":
    global bj_queuedExecTotal
    bj_queuedExecTotal = IMinBJ(bj_queuedExecTotal, 1)
    pass

def QueuedTriggerCountBJ()->"integer":
    return bj_queuedExecTotal
    pass

def IsTriggerQueueEmptyBJ()->"boolean":
    return bj_queuedExecTotal <= 0
    pass

def IsTriggerQueuedBJ(trig:"trigger")->"boolean":
    return QueuedTriggerGetIndex(trig) != - 1
    pass

def GetForLoopIndexA()->"integer":
    return bj_forLoopAIndex
    pass

def SetForLoopIndexA(newIndex:"integer")->"nothing":
    global bj_forLoopAIndex
    bj_forLoopAIndex = newIndex
    pass

def GetForLoopIndexB()->"integer":
    return bj_forLoopBIndex
    pass

def SetForLoopIndexB(newIndex:"integer")->"nothing":
    global bj_forLoopBIndex
    bj_forLoopBIndex = newIndex
    pass

def PolledWait(duration:"real")->"nothing":
    t = None
    timeRemaining = None
    if ( duration > 0 ):
        t = CreateTimer()
        TimerStart(t, duration, False, None)
        while True:
            timeRemaining = TimerGetRemaining(t)
            if timeRemaining <= 0:
                break
            if ( timeRemaining > bj_POLLED_WAIT_SKIP_THRESHOLD ):
                TriggerSleepAction(0.1 * timeRemaining)
            else:
                TriggerSleepAction(bj_POLLED_WAIT_INTERVAL)
            pass

        DestroyTimer(t)
    pass

def IntegerTertiaryOp(flag:"boolean", valueA:"integer", valueB:"integer")->"integer":
    if flag:
        return valueA
    else:
        return valueB
    pass

def DoNothing()->"nothing":
    pass

def CommentString(commentString:"string")->"nothing":
    pass

def StringIdentity(theString:"string")->"string":
    return GetLocalizedString(theString)
    pass

def GetBooleanAnd(valueA:"boolean", valueB:"boolean")->"boolean":
    return valueA and valueB
    pass

def GetBooleanOr(valueA:"boolean", valueB:"boolean")->"boolean":
    return valueA or valueB
    pass

def PercentToInt(percentage:"real", max:"integer")->"integer":
    result = R2I(percentage * I2R(max) * 0.01)
    if ( result < 0 ):
        result = 0
    elif ( result > max ):
        result = max
    return result
    pass

def PercentTo255(percentage:"real")->"integer":
    return PercentToInt(percentage, 255)
    pass

def GetTimeOfDay()->"real":
    return GetFloatGameState(GAME_STATE_TIME_OF_DAY)
    pass

def SetTimeOfDay(whatTime:"real")->"nothing":
    SetFloatGameState(GAME_STATE_TIME_OF_DAY, whatTime)
    pass

def SetTimeOfDayScalePercentBJ(scalePercent:"real")->"nothing":
    SetTimeOfDayScale(scalePercent * 0.01)
    pass

def GetTimeOfDayScalePercentBJ()->"real":
    return GetTimeOfDayScale() * 100
    pass

def PlaySound(soundName:"string")->"nothing":
    soundHandle = CreateSound(soundName, False, False, True, 12700, 12700, "")
    StartSound(soundHandle)
    KillSoundWhenDone(soundHandle)
    pass

def CompareLocationsBJ(A:"location", B:"location")->"boolean":
    return GetLocationX(A) == GetLocationX(B) and GetLocationY(A) == GetLocationY(B)
    pass

def CompareRectsBJ(A:"rect", B:"rect")->"boolean":
    return GetRectMinX(A) == GetRectMinX(B) and GetRectMinY(A) == GetRectMinY(B) and GetRectMaxX(A) == GetRectMaxX(B) and GetRectMaxY(A) == GetRectMaxY(B)
    pass

def GetRectFromCircleBJ(center:"location", radius:"real")->"rect":
    centerX = GetLocationX(center)
    centerY = GetLocationY(center)
    return Rect(centerX - radius, centerY - radius, centerX + radius, centerY + radius)
    pass

def GetCurrentCameraSetup()->"camerasetup":
    theCam = CreateCameraSetup()
    duration = 0
    CameraSetupSetField(theCam, CAMERA_FIELD_TARGET_DISTANCE, GetCameraField(CAMERA_FIELD_TARGET_DISTANCE), duration)
    CameraSetupSetField(theCam, CAMERA_FIELD_FARZ, GetCameraField(CAMERA_FIELD_FARZ), duration)
    CameraSetupSetField(theCam, CAMERA_FIELD_ZOFFSET, GetCameraField(CAMERA_FIELD_ZOFFSET), duration)
    CameraSetupSetField(theCam, CAMERA_FIELD_ANGLE_OF_ATTACK, bj_RADTODEG * GetCameraField(CAMERA_FIELD_ANGLE_OF_ATTACK), duration)
    CameraSetupSetField(theCam, CAMERA_FIELD_FIELD_OF_VIEW, bj_RADTODEG * GetCameraField(CAMERA_FIELD_FIELD_OF_VIEW), duration)
    CameraSetupSetField(theCam, CAMERA_FIELD_ROLL, bj_RADTODEG * GetCameraField(CAMERA_FIELD_ROLL), duration)
    CameraSetupSetField(theCam, CAMERA_FIELD_ROTATION, bj_RADTODEG * GetCameraField(CAMERA_FIELD_ROTATION), duration)
    CameraSetupSetDestPosition(theCam, GetCameraTargetPositionX(), GetCameraTargetPositionY(), duration)
    return theCam
    pass

def CameraSetupApplyForPlayer(doPan:"boolean", whichSetup:"camerasetup", whichPlayer:"player", duration:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        CameraSetupApplyForceDuration(whichSetup, doPan, duration)
    pass

def CameraSetupGetFieldSwap(whichField:"camerafield", whichSetup:"camerasetup")->"real":
    return CameraSetupGetField(whichSetup, whichField)
    pass

def SetCameraFieldForPlayer(whichPlayer:"player", whichField:"camerafield", value:"real", duration:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        SetCameraField(whichField, value, duration)
    pass

def SetCameraTargetControllerNoZForPlayer(whichPlayer:"player", whichUnit:"unit", xoffset:"real", yoffset:"real", inheritOrientation:"boolean")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        SetCameraTargetController(whichUnit, xoffset, yoffset, inheritOrientation)
    pass

def SetCameraPositionForPlayer(whichPlayer:"player", x:"real", y:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        SetCameraPosition(x, y)
    pass

def SetCameraPositionLocForPlayer(whichPlayer:"player", loc:"location")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        SetCameraPosition(GetLocationX(loc), GetLocationY(loc))
    pass

def RotateCameraAroundLocBJ(degrees:"real", loc:"location", whichPlayer:"player", duration:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        SetCameraRotateMode(GetLocationX(loc), GetLocationY(loc), bj_DEGTORAD * degrees, duration)
    pass

def PanCameraToForPlayer(whichPlayer:"player", x:"real", y:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        PanCameraTo(x, y)
    pass

def PanCameraToLocForPlayer(whichPlayer:"player", loc:"location")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        PanCameraTo(GetLocationX(loc), GetLocationY(loc))
    pass

def PanCameraToTimedForPlayer(whichPlayer:"player", x:"real", y:"real", duration:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        PanCameraToTimed(x, y, duration)
    pass

def PanCameraToTimedLocForPlayer(whichPlayer:"player", loc:"location", duration:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        PanCameraToTimed(GetLocationX(loc), GetLocationY(loc), duration)
    pass

def PanCameraToTimedLocWithZForPlayer(whichPlayer:"player", loc:"location", zOffset:"real", duration:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        PanCameraToTimedWithZ(GetLocationX(loc), GetLocationY(loc), zOffset, duration)
    pass

def SmartCameraPanBJ(whichPlayer:"player", loc:"location", duration:"real")->"nothing":
    dist = None
    if ( GetLocalPlayer() == whichPlayer ):
        dist = DistanceBetweenPoints(loc, GetCameraTargetPositionLoc())
        if ( dist >= bj_SMARTPAN_TRESHOLD_SNAP ):
            PanCameraToTimed(GetLocationX(loc), GetLocationY(loc), 0)
        elif ( dist >= bj_SMARTPAN_TRESHOLD_PAN ):
            PanCameraToTimed(GetLocationX(loc), GetLocationY(loc), duration)
    pass

def SetCinematicCameraForPlayer(whichPlayer:"player", cameraModelFile:"string")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        SetCinematicCamera(cameraModelFile)
    pass

def ResetToGameCameraForPlayer(whichPlayer:"player", duration:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        ResetToGameCamera(duration)
    pass

def CameraSetSourceNoiseForPlayer(whichPlayer:"player", magnitude:"real", velocity:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        CameraSetSourceNoise(magnitude, velocity)
    pass

def CameraSetTargetNoiseForPlayer(whichPlayer:"player", magnitude:"real", velocity:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        CameraSetTargetNoise(magnitude, velocity)
    pass

def CameraSetEQNoiseForPlayer(whichPlayer:"player", magnitude:"real")->"nothing":
    richter = magnitude
    if ( richter > 5.0 ):
        richter = 5.0
    if ( richter < 2.0 ):
        richter = 2.0
    if ( GetLocalPlayer() == whichPlayer ):
        CameraSetTargetNoiseEx(magnitude * 2.0, magnitude * Pow(10, richter), True)
        CameraSetSourceNoiseEx(magnitude * 2.0, magnitude * Pow(10, richter), True)
    pass

def CameraClearNoiseForPlayer(whichPlayer:"player")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        CameraSetSourceNoise(0, 0)
        CameraSetTargetNoise(0, 0)
    pass

def GetCurrentCameraBoundsMapRectBJ()->"rect":
    return Rect(GetCameraBoundMinX(), GetCameraBoundMinY(), GetCameraBoundMaxX(), GetCameraBoundMaxY())
    pass

def GetCameraBoundsMapRect()->"rect":
    return bj_mapInitialCameraBounds
    pass

def GetPlayableMapRect()->"rect":
    return bj_mapInitialPlayableArea
    pass

def GetEntireMapRect()->"rect":
    return GetWorldBounds()
    pass

def SetCameraBoundsToRect(r:"rect")->"nothing":
    minX = GetRectMinX(r)
    minY = GetRectMinY(r)
    maxX = GetRectMaxX(r)
    maxY = GetRectMaxY(r)
    SetCameraBounds(minX, minY, minX, maxY, maxX, maxY, maxX, minY)
    pass

def SetCameraBoundsToRectForPlayerBJ(whichPlayer:"player", r:"rect")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        SetCameraBoundsToRect(r)
    pass

def AdjustCameraBoundsBJ(adjustMethod:"integer", dxWest:"real", dxEast:"real", dyNorth:"real", dySouth:"real")->"nothing":
    minX = 0
    minY = 0
    maxX = 0
    maxY = 0
    scale = 0
    if ( adjustMethod == bj_CAMERABOUNDS_ADJUST_ADD ):
        scale = 1
    elif ( adjustMethod == bj_CAMERABOUNDS_ADJUST_SUB ):
        scale = - 1
    minX = GetCameraBoundMinX() - scale * dxWest
    maxX = GetCameraBoundMaxX() + scale * dxEast
    minY = GetCameraBoundMinY() - scale * dySouth
    maxY = GetCameraBoundMaxY() + scale * dyNorth
    if ( maxX < minX ):
        minX = ( minX + maxX ) * 0.5
        maxX = minX
    if ( maxY < minY ):
        minY = ( minY + maxY ) * 0.5
        maxY = minY
    SetCameraBounds(minX, minY, minX, maxY, maxX, maxY, maxX, minY)
    pass

def AdjustCameraBoundsForPlayerBJ(adjustMethod:"integer", whichPlayer:"player", dxWest:"real", dxEast:"real", dyNorth:"real", dySouth:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        AdjustCameraBoundsBJ(adjustMethod, dxWest, dxEast, dyNorth, dySouth)
    pass

def SetCameraQuickPositionForPlayer(whichPlayer:"player", x:"real", y:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        SetCameraQuickPosition(x, y)
    pass

def SetCameraQuickPositionLocForPlayer(whichPlayer:"player", loc:"location")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        SetCameraQuickPosition(GetLocationX(loc), GetLocationY(loc))
    pass

def SetCameraQuickPositionLoc(loc:"location")->"nothing":
    SetCameraQuickPosition(GetLocationX(loc), GetLocationY(loc))
    pass

def StopCameraForPlayerBJ(whichPlayer:"player")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        StopCamera()
    pass

def SetCameraOrientControllerForPlayerBJ(whichPlayer:"player", whichUnit:"unit", xoffset:"real", yoffset:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        SetCameraOrientController(whichUnit, xoffset, yoffset)
    pass

def CameraSetSmoothingFactorBJ(factor:"real")->"nothing":
    CameraSetSmoothingFactor(factor)
    pass

def CameraResetSmoothingFactorBJ()->"nothing":
    CameraSetSmoothingFactor(0)
    pass

def DisplayTextToForce(toForce:"force", message:"string")->"nothing":
    if ( IsPlayerInForce(GetLocalPlayer(), toForce) ):
        DisplayTextToPlayer(GetLocalPlayer(), 0, 0, message)
    pass

def DisplayTimedTextToForce(toForce:"force", duration:"real", message:"string")->"nothing":
    if ( IsPlayerInForce(GetLocalPlayer(), toForce) ):
        DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, duration, message)
    pass

def ClearTextMessagesBJ(toForce:"force")->"nothing":
    if ( IsPlayerInForce(GetLocalPlayer(), toForce) ):
        ClearTextMessages()
    pass

def SubStringBJ(source:"string", start:"integer", end:"integer")->"string":
    return SubString(source, start-1, end)
    pass

def GetHandleIdBJ(h:"handle")->"integer":
    return GetHandleId(h)
    pass

def StringHashBJ(s:"string")->"integer":
    return StringHash(s)
    pass

def TriggerRegisterTimerEventPeriodic(trig:"trigger", timeout:"real")->"event":
    return TriggerRegisterTimerEvent(trig, timeout, True)
    pass

def TriggerRegisterTimerEventSingle(trig:"trigger", timeout:"real")->"event":
    return TriggerRegisterTimerEvent(trig, timeout, False)
    pass

def TriggerRegisterTimerExpireEventBJ(trig:"trigger", t:"timer")->"event":
    return TriggerRegisterTimerExpireEvent(trig, t)
    pass

def TriggerRegisterPlayerUnitEventSimple(trig:"trigger", whichPlayer:"player", whichEvent:"playerunitevent")->"event":
    return TriggerRegisterPlayerUnitEvent(trig, whichPlayer, whichEvent, None)
    pass

def TriggerRegisterAnyUnitEventBJ(trig:"trigger", whichEvent:"playerunitevent")->"nothing":
    index = None
    index = 0
    while True:
        TriggerRegisterPlayerUnitEvent(trig, Player(index), whichEvent, None)
        index = index + 1
        if index == bj_MAX_PLAYER_SLOTS:
            break
        pass

    pass

def TriggerRegisterPlayerSelectionEventBJ(trig:"trigger", whichPlayer:"player", selected:"boolean")->"event":
    if selected:
        return TriggerRegisterPlayerUnitEvent(trig, whichPlayer, EVENT_PLAYER_UNIT_SELECTED, None)
    else:
        return TriggerRegisterPlayerUnitEvent(trig, whichPlayer, EVENT_PLAYER_UNIT_DESELECTED, None)
    pass

def TriggerRegisterPlayerKeyEventBJ(trig:"trigger", whichPlayer:"player", keType:"integer", keKey:"integer")->"event":
    if ( keType == bj_KEYEVENTTYPE_DEPRESS ):
        if ( keKey == bj_KEYEVENTKEY_LEFT ):
            return TriggerRegisterPlayerEvent(trig, whichPlayer, EVENT_PLAYER_ARROW_LEFT_DOWN)
        elif ( keKey == bj_KEYEVENTKEY_RIGHT ):
            return TriggerRegisterPlayerEvent(trig, whichPlayer, EVENT_PLAYER_ARROW_RIGHT_DOWN)
        elif ( keKey == bj_KEYEVENTKEY_DOWN ):
            return TriggerRegisterPlayerEvent(trig, whichPlayer, EVENT_PLAYER_ARROW_DOWN_DOWN)
        elif ( keKey == bj_KEYEVENTKEY_UP ):
            return TriggerRegisterPlayerEvent(trig, whichPlayer, EVENT_PLAYER_ARROW_UP_DOWN)
        else:
            return None
    elif ( keType == bj_KEYEVENTTYPE_RELEASE ):
        if ( keKey == bj_KEYEVENTKEY_LEFT ):
            return TriggerRegisterPlayerEvent(trig, whichPlayer, EVENT_PLAYER_ARROW_LEFT_UP)
        elif ( keKey == bj_KEYEVENTKEY_RIGHT ):
            return TriggerRegisterPlayerEvent(trig, whichPlayer, EVENT_PLAYER_ARROW_RIGHT_UP)
        elif ( keKey == bj_KEYEVENTKEY_DOWN ):
            return TriggerRegisterPlayerEvent(trig, whichPlayer, EVENT_PLAYER_ARROW_DOWN_UP)
        elif ( keKey == bj_KEYEVENTKEY_UP ):
            return TriggerRegisterPlayerEvent(trig, whichPlayer, EVENT_PLAYER_ARROW_UP_UP)
        else:
            return None
    else:
        return None
    pass

def TriggerRegisterPlayerEventVictory(trig:"trigger", whichPlayer:"player")->"event":
    return TriggerRegisterPlayerEvent(trig, whichPlayer, EVENT_PLAYER_VICTORY)
    pass

def TriggerRegisterPlayerEventDefeat(trig:"trigger", whichPlayer:"player")->"event":
    return TriggerRegisterPlayerEvent(trig, whichPlayer, EVENT_PLAYER_DEFEAT)
    pass

def TriggerRegisterPlayerEventLeave(trig:"trigger", whichPlayer:"player")->"event":
    return TriggerRegisterPlayerEvent(trig, whichPlayer, EVENT_PLAYER_LEAVE)
    pass

def TriggerRegisterPlayerEventAllianceChanged(trig:"trigger", whichPlayer:"player")->"event":
    return TriggerRegisterPlayerEvent(trig, whichPlayer, EVENT_PLAYER_ALLIANCE_CHANGED)
    pass

def TriggerRegisterPlayerEventEndCinematic(trig:"trigger", whichPlayer:"player")->"event":
    return TriggerRegisterPlayerEvent(trig, whichPlayer, EVENT_PLAYER_END_CINEMATIC)
    pass

def TriggerRegisterGameStateEventTimeOfDay(trig:"trigger", opcode:"limitop", limitval:"real")->"event":
    return TriggerRegisterGameStateEvent(trig, GAME_STATE_TIME_OF_DAY, opcode, limitval)
    pass

def TriggerRegisterEnterRegionSimple(trig:"trigger", whichRegion:"region")->"event":
    return TriggerRegisterEnterRegion(trig, whichRegion, None)
    pass

def TriggerRegisterLeaveRegionSimple(trig:"trigger", whichRegion:"region")->"event":
    return TriggerRegisterLeaveRegion(trig, whichRegion, None)
    pass

def TriggerRegisterEnterRectSimple(trig:"trigger", r:"rect")->"event":
    rectRegion = CreateRegion()
    RegionAddRect(rectRegion, r)
    return TriggerRegisterEnterRegion(trig, rectRegion, None)
    pass

def TriggerRegisterLeaveRectSimple(trig:"trigger", r:"rect")->"event":
    rectRegion = CreateRegion()
    RegionAddRect(rectRegion, r)
    return TriggerRegisterLeaveRegion(trig, rectRegion, None)
    pass

def TriggerRegisterDistanceBetweenUnits(trig:"trigger", whichUnit:"unit", condition:"boolexpr", range:"real")->"event":
    return TriggerRegisterUnitInRange(trig, whichUnit, range, condition)
    pass

def TriggerRegisterUnitInRangeSimple(trig:"trigger", range:"real", whichUnit:"unit")->"event":
    return TriggerRegisterUnitInRange(trig, whichUnit, range, None)
    pass

def TriggerRegisterUnitLifeEvent(trig:"trigger", whichUnit:"unit", opcode:"limitop", limitval:"real")->"event":
    return TriggerRegisterUnitStateEvent(trig, whichUnit, UNIT_STATE_LIFE, opcode, limitval)
    pass

def TriggerRegisterUnitManaEvent(trig:"trigger", whichUnit:"unit", opcode:"limitop", limitval:"real")->"event":
    return TriggerRegisterUnitStateEvent(trig, whichUnit, UNIT_STATE_MANA, opcode, limitval)
    pass

def TriggerRegisterDialogEventBJ(trig:"trigger", whichDialog:"dialog")->"event":
    return TriggerRegisterDialogEvent(trig, whichDialog)
    pass

def TriggerRegisterShowSkillEventBJ(trig:"trigger")->"event":
    return TriggerRegisterGameEvent(trig, EVENT_GAME_SHOW_SKILL)
    pass

def TriggerRegisterBuildSubmenuEventBJ(trig:"trigger")->"event":
    return TriggerRegisterGameEvent(trig, EVENT_GAME_BUILD_SUBMENU)
    pass

def TriggerRegisterGameLoadedEventBJ(trig:"trigger")->"event":
    return TriggerRegisterGameEvent(trig, EVENT_GAME_LOADED)
    pass

def TriggerRegisterGameSavedEventBJ(trig:"trigger")->"event":
    return TriggerRegisterGameEvent(trig, EVENT_GAME_SAVE)
    pass

def RegisterDestDeathInRegionEnum()->"nothing":
    global bj_destInRegionDiesCount
    bj_destInRegionDiesCount = bj_destInRegionDiesCount + 1
    if ( bj_destInRegionDiesCount <= bj_MAX_DEST_IN_REGION_EVENTS ):
        TriggerRegisterDeathEvent(bj_destInRegionDiesTrig, GetEnumDestructable())
    pass

def TriggerRegisterDestDeathInRegionEvent(trig:"trigger", r:"rect")->"nothing":
    global bj_destInRegionDiesCount
    global bj_destInRegionDiesTrig
    bj_destInRegionDiesTrig = trig
    bj_destInRegionDiesCount = 0
    EnumDestructablesInRect(r, None, RegisterDestDeathInRegionEnum)
    pass

def AddWeatherEffectSaveLast(where:"rect", effectID:"integer")->"weathereffect":
    global bj_lastCreatedWeatherEffect
    bj_lastCreatedWeatherEffect = AddWeatherEffect(where, effectID)
    return bj_lastCreatedWeatherEffect
    pass

def GetLastCreatedWeatherEffect()->"weathereffect":
    return bj_lastCreatedWeatherEffect
    pass

def RemoveWeatherEffectBJ(whichWeatherEffect:"weathereffect")->"nothing":
    RemoveWeatherEffect(whichWeatherEffect)
    pass

def TerrainDeformationCraterBJ(duration:"real", permanent:"boolean", where:"location", radius:"real", depth:"real")->"terraindeformation":
    global bj_lastCreatedTerrainDeformation
    bj_lastCreatedTerrainDeformation = TerrainDeformCrater(GetLocationX(where), GetLocationY(where), radius, depth, R2I(duration * 1000), permanent)
    return bj_lastCreatedTerrainDeformation
    pass

def TerrainDeformationRippleBJ(duration:"real", limitNeg:"boolean", where:"location", startRadius:"real", endRadius:"real", depth:"real", wavePeriod:"real", waveWidth:"real")->"terraindeformation":
    global bj_lastCreatedTerrainDeformation
    spaceWave = None
    timeWave = None
    radiusRatio = None
    if ( endRadius <= 0 or waveWidth <= 0 or wavePeriod <= 0 ):
        return None
    timeWave = 2.0 * duration / wavePeriod
    spaceWave = 2.0 * endRadius / waveWidth
    radiusRatio = startRadius / endRadius
    bj_lastCreatedTerrainDeformation = TerrainDeformRipple(GetLocationX(where), GetLocationY(where), endRadius, depth, R2I(duration * 1000), 1, spaceWave, timeWave, radiusRatio, limitNeg)
    return bj_lastCreatedTerrainDeformation
    pass

def TerrainDeformationWaveBJ(duration:"real", source:"location", target:"location", radius:"real", depth:"real", trailDelay:"real")->"terraindeformation":
    global bj_lastCreatedTerrainDeformation
    distance = None
    dirX = None
    dirY = None
    speed = None
    distance = DistanceBetweenPoints(source, target)
    if ( distance == 0 or duration <= 0 ):
        return None
    dirX = ( GetLocationX(target) - GetLocationX(source) ) / distance
    dirY = ( GetLocationY(target) - GetLocationY(source) ) / distance
    speed = distance / duration
    bj_lastCreatedTerrainDeformation = TerrainDeformWave(GetLocationX(source), GetLocationY(source), dirX, dirY, distance, speed, radius, depth, R2I(trailDelay * 1000), 1)
    return bj_lastCreatedTerrainDeformation
    pass

def TerrainDeformationRandomBJ(duration:"real", where:"location", radius:"real", minDelta:"real", maxDelta:"real", updateInterval:"real")->"terraindeformation":
    global bj_lastCreatedTerrainDeformation
    bj_lastCreatedTerrainDeformation = TerrainDeformRandom(GetLocationX(where), GetLocationY(where), radius, minDelta, maxDelta, R2I(duration * 1000), R2I(updateInterval * 1000))
    return bj_lastCreatedTerrainDeformation
    pass

def TerrainDeformationStopBJ(deformation:"terraindeformation", duration:"real")->"nothing":
    TerrainDeformStop(deformation, R2I(duration * 1000))
    pass

def GetLastCreatedTerrainDeformation()->"terraindeformation":
    return bj_lastCreatedTerrainDeformation
    pass

def AddLightningLoc(codeName:"string", where1:"location", where2:"location")->"lightning":
    global bj_lastCreatedLightning
    bj_lastCreatedLightning = AddLightningEx(codeName, True, GetLocationX(where1), GetLocationY(where1), GetLocationZ(where1), GetLocationX(where2), GetLocationY(where2), GetLocationZ(where2))
    return bj_lastCreatedLightning
    pass

def DestroyLightningBJ(whichBolt:"lightning")->"boolean":
    return DestroyLightning(whichBolt)
    pass

def MoveLightningLoc(whichBolt:"lightning", where1:"location", where2:"location")->"boolean":
    return MoveLightningEx(whichBolt, True, GetLocationX(where1), GetLocationY(where1), GetLocationZ(where1), GetLocationX(where2), GetLocationY(where2), GetLocationZ(where2))
    pass

def GetLightningColorABJ(whichBolt:"lightning")->"real":
    return GetLightningColorA(whichBolt)
    pass

def GetLightningColorRBJ(whichBolt:"lightning")->"real":
    return GetLightningColorR(whichBolt)
    pass

def GetLightningColorGBJ(whichBolt:"lightning")->"real":
    return GetLightningColorG(whichBolt)
    pass

def GetLightningColorBBJ(whichBolt:"lightning")->"real":
    return GetLightningColorB(whichBolt)
    pass

def SetLightningColorBJ(whichBolt:"lightning", r:"real", g:"real", b:"real", a:"real")->"boolean":
    return SetLightningColor(whichBolt, r, g, b, a)
    pass

def GetLastCreatedLightningBJ()->"lightning":
    return bj_lastCreatedLightning
    pass

def GetAbilityEffectBJ(abilcode:"integer", t:"effecttype", index:"integer")->"string":
    return GetAbilityEffectById(abilcode, t, index)
    pass

def GetAbilitySoundBJ(abilcode:"integer", t:"soundtype")->"string":
    return GetAbilitySoundById(abilcode, t)
    pass

def GetTerrainCliffLevelBJ(where:"location")->"integer":
    return GetTerrainCliffLevel(GetLocationX(where), GetLocationY(where))
    pass

def GetTerrainTypeBJ(where:"location")->"integer":
    return GetTerrainType(GetLocationX(where), GetLocationY(where))
    pass

def GetTerrainVarianceBJ(where:"location")->"integer":
    return GetTerrainVariance(GetLocationX(where), GetLocationY(where))
    pass

def SetTerrainTypeBJ(where:"location", terrainType:"integer", variation:"integer", area:"integer", shape:"integer")->"nothing":
    SetTerrainType(GetLocationX(where), GetLocationY(where), terrainType, variation, area, shape)
    pass

def IsTerrainPathableBJ(where:"location", t:"pathingtype")->"boolean":
    return IsTerrainPathable(GetLocationX(where), GetLocationY(where), t)
    pass

def SetTerrainPathableBJ(where:"location", t:"pathingtype", flag:"boolean")->"nothing":
    SetTerrainPathable(GetLocationX(where), GetLocationY(where), t, flag)
    pass

def SetWaterBaseColorBJ(red:"real", green:"real", blue:"real", transparency:"real")->"nothing":
    SetWaterBaseColor(PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - transparency))
    pass

def CreateFogModifierRectSimple(whichPlayer:"player", whichFogState:"fogstate", r:"rect", afterUnits:"boolean")->"fogmodifier":
    global bj_lastCreatedFogModifier
    bj_lastCreatedFogModifier = CreateFogModifierRect(whichPlayer, whichFogState, r, True, afterUnits)
    return bj_lastCreatedFogModifier
    pass

def CreateFogModifierRadiusLocSimple(whichPlayer:"player", whichFogState:"fogstate", center:"location", radius:"real", afterUnits:"boolean")->"fogmodifier":
    global bj_lastCreatedFogModifier
    bj_lastCreatedFogModifier = CreateFogModifierRadiusLoc(whichPlayer, whichFogState, center, radius, True, afterUnits)
    return bj_lastCreatedFogModifier
    pass

def CreateFogModifierRectBJ(enabled:"boolean", whichPlayer:"player", whichFogState:"fogstate", r:"rect")->"fogmodifier":
    global bj_lastCreatedFogModifier
    bj_lastCreatedFogModifier = CreateFogModifierRect(whichPlayer, whichFogState, r, True, False)
    if enabled:
        FogModifierStart(bj_lastCreatedFogModifier)
    return bj_lastCreatedFogModifier
    pass

def CreateFogModifierRadiusLocBJ(enabled:"boolean", whichPlayer:"player", whichFogState:"fogstate", center:"location", radius:"real")->"fogmodifier":
    global bj_lastCreatedFogModifier
    bj_lastCreatedFogModifier = CreateFogModifierRadiusLoc(whichPlayer, whichFogState, center, radius, True, False)
    if enabled:
        FogModifierStart(bj_lastCreatedFogModifier)
    return bj_lastCreatedFogModifier
    pass

def GetLastCreatedFogModifier()->"fogmodifier":
    return bj_lastCreatedFogModifier
    pass

def FogEnableOn()->"nothing":
    FogEnable(True)
    pass

def FogEnableOff()->"nothing":
    FogEnable(False)
    pass

def FogMaskEnableOn()->"nothing":
    FogMaskEnable(True)
    pass

def FogMaskEnableOff()->"nothing":
    FogMaskEnable(False)
    pass

def UseTimeOfDayBJ(flag:"boolean")->"nothing":
    SuspendTimeOfDay(not  flag)
    pass

def SetTerrainFogExBJ(style:"integer", zstart:"real", zend:"real", density:"real", red:"real", green:"real", blue:"real")->"nothing":
    SetTerrainFogEx(style, zstart, zend, density, red * 0.01, green * 0.01, blue * 0.01)
    pass

def ResetTerrainFogBJ()->"nothing":
    ResetTerrainFog()
    pass

def SetDoodadAnimationBJ(animName:"string", doodadID:"integer", radius:"real", center:"location")->"nothing":
    SetDoodadAnimation(GetLocationX(center), GetLocationY(center), radius, doodadID, False, animName, False)
    pass

def SetDoodadAnimationRectBJ(animName:"string", doodadID:"integer", r:"rect")->"nothing":
    SetDoodadAnimationRect(r, doodadID, animName, False)
    pass

def AddUnitAnimationPropertiesBJ(add:"boolean", animProperties:"string", whichUnit:"unit")->"nothing":
    AddUnitAnimationProperties(whichUnit, animProperties, add)
    pass

def CreateImageBJ(file:"string", size:"real", where:"location", zOffset:"real", imageType:"integer")->"image":
    global bj_lastCreatedImage
    bj_lastCreatedImage = CreateImage(file, size, size, size, GetLocationX(where), GetLocationY(where), zOffset, 0, 0, 0, imageType)
    return bj_lastCreatedImage
    pass

def ShowImageBJ(flag:"boolean", whichImage:"image")->"nothing":
    ShowImage(whichImage, flag)
    pass

def SetImagePositionBJ(whichImage:"image", where:"location", zOffset:"real")->"nothing":
    SetImagePosition(whichImage, GetLocationX(where), GetLocationY(where), zOffset)
    pass

def SetImageColorBJ(whichImage:"image", red:"real", green:"real", blue:"real", alpha:"real")->"nothing":
    SetImageColor(whichImage, PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - alpha))
    pass

def GetLastCreatedImage()->"image":
    return bj_lastCreatedImage
    pass

def CreateUbersplatBJ(where:"location", name:"string", red:"real", green:"real", blue:"real", alpha:"real", forcePaused:"boolean", noBirthTime:"boolean")->"ubersplat":
    global bj_lastCreatedUbersplat
    bj_lastCreatedUbersplat = CreateUbersplat(GetLocationX(where), GetLocationY(where), name, PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - alpha), forcePaused, noBirthTime)
    return bj_lastCreatedUbersplat
    pass

def ShowUbersplatBJ(flag:"boolean", whichSplat:"ubersplat")->"nothing":
    ShowUbersplat(whichSplat, flag)
    pass

def GetLastCreatedUbersplat()->"ubersplat":
    return bj_lastCreatedUbersplat
    pass

def PlaySoundBJ(soundHandle:"sound")->"nothing":
    global bj_lastPlayedSound
    bj_lastPlayedSound = soundHandle
    if ( soundHandle != None ):
        StartSound(soundHandle)
    pass

def StopSoundBJ(soundHandle:"sound", fadeOut:"boolean")->"nothing":
    StopSound(soundHandle, False, fadeOut)
    pass

def SetSoundVolumeBJ(soundHandle:"sound", volumePercent:"real")->"nothing":
    SetSoundVolume(soundHandle, PercentToInt(volumePercent, 127))
    pass

def SetSoundOffsetBJ(newOffset:"real", soundHandle:"sound")->"nothing":
    SetSoundPlayPosition(soundHandle, R2I(newOffset * 1000))
    pass

def SetSoundDistanceCutoffBJ(soundHandle:"sound", cutoff:"real")->"nothing":
    SetSoundDistanceCutoff(soundHandle, cutoff)
    pass

def SetSoundPitchBJ(soundHandle:"sound", pitch:"real")->"nothing":
    SetSoundPitch(soundHandle, pitch)
    pass

def SetSoundPositionLocBJ(soundHandle:"sound", loc:"location", z:"real")->"nothing":
    SetSoundPosition(soundHandle, GetLocationX(loc), GetLocationY(loc), z)
    pass

def AttachSoundToUnitBJ(soundHandle:"sound", whichUnit:"unit")->"nothing":
    AttachSoundToUnit(soundHandle, whichUnit)
    pass

def SetSoundConeAnglesBJ(soundHandle:"sound", inside:"real", outside:"real", outsideVolumePercent:"real")->"nothing":
    SetSoundConeAngles(soundHandle, inside, outside, PercentToInt(outsideVolumePercent, 127))
    pass

def KillSoundWhenDoneBJ(soundHandle:"sound")->"nothing":
    KillSoundWhenDone(soundHandle)
    pass

def PlaySoundAtPointBJ(soundHandle:"sound", volumePercent:"real", loc:"location", z:"real")->"nothing":
    SetSoundPositionLocBJ(soundHandle, loc, z)
    SetSoundVolumeBJ(soundHandle, volumePercent)
    PlaySoundBJ(soundHandle)
    pass

def PlaySoundOnUnitBJ(soundHandle:"sound", volumePercent:"real", whichUnit:"unit")->"nothing":
    AttachSoundToUnitBJ(soundHandle, whichUnit)
    SetSoundVolumeBJ(soundHandle, volumePercent)
    PlaySoundBJ(soundHandle)
    pass

def PlaySoundFromOffsetBJ(soundHandle:"sound", volumePercent:"real", startingOffset:"real")->"nothing":
    SetSoundVolumeBJ(soundHandle, volumePercent)
    PlaySoundBJ(soundHandle)
    SetSoundOffsetBJ(startingOffset, soundHandle)
    pass

def PlayMusicBJ(musicFileName:"string")->"nothing":
    global bj_lastPlayedMusic
    bj_lastPlayedMusic = musicFileName
    PlayMusic(musicFileName)
    pass

def PlayMusicExBJ(musicFileName:"string", startingOffset:"real", fadeInTime:"real")->"nothing":
    global bj_lastPlayedMusic
    bj_lastPlayedMusic = musicFileName
    PlayMusicEx(musicFileName, R2I(startingOffset * 1000), R2I(fadeInTime * 1000))
    pass

def SetMusicOffsetBJ(newOffset:"real")->"nothing":
    SetMusicPlayPosition(R2I(newOffset * 1000))
    pass

def PlayThematicMusicBJ(musicName:"string")->"nothing":
    PlayThematicMusic(musicName)
    pass

def PlayThematicMusicExBJ(musicName:"string", startingOffset:"real")->"nothing":
    PlayThematicMusicEx(musicName, R2I(startingOffset * 1000))
    pass

def SetThematicMusicOffsetBJ(newOffset:"real")->"nothing":
    SetThematicMusicPlayPosition(R2I(newOffset * 1000))
    pass

def EndThematicMusicBJ()->"nothing":
    EndThematicMusic()
    pass

def StopMusicBJ(fadeOut:"boolean")->"nothing":
    StopMusic(fadeOut)
    pass

def ResumeMusicBJ()->"nothing":
    ResumeMusic()
    pass

def SetMusicVolumeBJ(volumePercent:"real")->"nothing":
    SetMusicVolume(PercentToInt(volumePercent, 127))
    pass

def GetSoundDurationBJ(soundHandle:"sound")->"real":
    if ( soundHandle == None ):
        return bj_NOTHING_SOUND_DURATION
    else:
        return I2R(GetSoundDuration(soundHandle)) * 0.001
    pass

def GetSoundFileDurationBJ(musicFileName:"string")->"real":
    return I2R(GetSoundFileDuration(musicFileName)) * 0.001
    pass

def GetLastPlayedSound()->"sound":
    return bj_lastPlayedSound
    pass

def GetLastPlayedMusic()->"string":
    return bj_lastPlayedMusic
    pass

def VolumeGroupSetVolumeBJ(vgroup:"volumegroup", percent:"real")->"nothing":
    VolumeGroupSetVolume(vgroup, percent * 0.01)
    pass

def SetCineModeVolumeGroupsImmediateBJ()->"nothing":
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_UNITMOVEMENT, bj_CINEMODE_VOLUME_UNITMOVEMENT)
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_UNITSOUNDS, bj_CINEMODE_VOLUME_UNITSOUNDS)
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_COMBAT, bj_CINEMODE_VOLUME_COMBAT)
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_SPELLS, bj_CINEMODE_VOLUME_SPELLS)
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_UI, bj_CINEMODE_VOLUME_UI)
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_MUSIC, bj_CINEMODE_VOLUME_MUSIC)
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_AMBIENTSOUNDS, bj_CINEMODE_VOLUME_AMBIENTSOUNDS)
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_FIRE, bj_CINEMODE_VOLUME_FIRE)
    pass

def SetCineModeVolumeGroupsBJ()->"nothing":
    if bj_gameStarted:
        SetCineModeVolumeGroupsImmediateBJ()
    else:
        TimerStart(bj_volumeGroupsTimer, bj_GAME_STARTED_THRESHOLD, False, SetCineModeVolumeGroupsImmediateBJ)
    pass

def SetSpeechVolumeGroupsImmediateBJ()->"nothing":
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_UNITMOVEMENT, bj_SPEECH_VOLUME_UNITMOVEMENT)
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_UNITSOUNDS, bj_SPEECH_VOLUME_UNITSOUNDS)
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_COMBAT, bj_SPEECH_VOLUME_COMBAT)
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_SPELLS, bj_SPEECH_VOLUME_SPELLS)
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_UI, bj_SPEECH_VOLUME_UI)
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_MUSIC, bj_SPEECH_VOLUME_MUSIC)
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_AMBIENTSOUNDS, bj_SPEECH_VOLUME_AMBIENTSOUNDS)
    VolumeGroupSetVolume(SOUND_VOLUMEGROUP_FIRE, bj_SPEECH_VOLUME_FIRE)
    pass

def SetSpeechVolumeGroupsBJ()->"nothing":
    if bj_gameStarted:
        SetSpeechVolumeGroupsImmediateBJ()
    else:
        TimerStart(bj_volumeGroupsTimer, bj_GAME_STARTED_THRESHOLD, False, SetSpeechVolumeGroupsImmediateBJ)
    pass

def VolumeGroupResetImmediateBJ()->"nothing":
    VolumeGroupReset()
    pass

def VolumeGroupResetBJ()->"nothing":
    if bj_gameStarted:
        VolumeGroupResetImmediateBJ()
    else:
        TimerStart(bj_volumeGroupsTimer, bj_GAME_STARTED_THRESHOLD, False, VolumeGroupResetImmediateBJ)
    pass

def GetSoundIsPlayingBJ(soundHandle:"sound")->"boolean":
    return GetSoundIsLoading(soundHandle) or GetSoundIsPlaying(soundHandle)
    pass

def WaitForSoundBJ(soundHandle:"sound", offset:"real")->"nothing":
    TriggerWaitForSound(soundHandle, offset)
    pass

def SetMapMusicIndexedBJ(musicName:"string", index:"integer")->"nothing":
    SetMapMusic(musicName, False, index)
    pass

def SetMapMusicRandomBJ(musicName:"string")->"nothing":
    SetMapMusic(musicName, True, 0)
    pass

def ClearMapMusicBJ()->"nothing":
    ClearMapMusic()
    pass

def SetStackedSoundBJ(add:"boolean", soundHandle:"sound", r:"rect")->"nothing":
    width = GetRectMaxX(r) - GetRectMinX(r)
    height = GetRectMaxY(r) - GetRectMinY(r)
    SetSoundPosition(soundHandle, GetRectCenterX(r), GetRectCenterY(r), 0)
    if add:
        RegisterStackedSound(soundHandle, True, width, height)
    else:
        UnregisterStackedSound(soundHandle, True, width, height)
    pass

def StartSoundForPlayerBJ(whichPlayer:"player", soundHandle:"sound")->"nothing":
    if ( whichPlayer == GetLocalPlayer() ):
        StartSound(soundHandle)
    pass

def VolumeGroupSetVolumeForPlayerBJ(whichPlayer:"player", vgroup:"volumegroup", scale:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        VolumeGroupSetVolume(vgroup, scale)
    pass

def EnableDawnDusk(flag:"boolean")->"nothing":
    global bj_useDawnDuskSounds
    bj_useDawnDuskSounds = flag
    pass

def IsDawnDuskEnabled()->"boolean":
    return bj_useDawnDuskSounds
    pass

def SetAmbientDaySound(inLabel:"string")->"nothing":
    global bj_dayAmbientSound
    ToD = None
    if ( bj_dayAmbientSound != None ):
        StopSound(bj_dayAmbientSound, True, True)
    bj_dayAmbientSound = CreateMIDISound(inLabel, 20, 20)
    ToD = GetTimeOfDay()
    if ( ToD >= bj_TOD_DAWN and ToD < bj_TOD_DUSK ):
        StartSound(bj_dayAmbientSound)
    pass

def SetAmbientNightSound(inLabel:"string")->"nothing":
    global bj_nightAmbientSound
    ToD = None
    if ( bj_nightAmbientSound != None ):
        StopSound(bj_nightAmbientSound, True, True)
    bj_nightAmbientSound = CreateMIDISound(inLabel, 20, 20)
    ToD = GetTimeOfDay()
    if ( ToD < bj_TOD_DAWN or ToD >= bj_TOD_DUSK ):
        StartSound(bj_nightAmbientSound)
    pass

def AddSpecialEffectLocBJ(where:"location", modelName:"string")->"effect":
    global bj_lastCreatedEffect
    bj_lastCreatedEffect = AddSpecialEffectLoc(modelName, where)
    return bj_lastCreatedEffect
    pass

def AddSpecialEffectTargetUnitBJ(attachPointName:"string", targetWidget:"widget", modelName:"string")->"effect":
    global bj_lastCreatedEffect
    bj_lastCreatedEffect = AddSpecialEffectTarget(modelName, targetWidget, attachPointName)
    return bj_lastCreatedEffect
    pass

def DestroyEffectBJ(whichEffect:"effect")->"nothing":
    DestroyEffect(whichEffect)
    pass

def GetLastCreatedEffectBJ()->"effect":
    return bj_lastCreatedEffect
    pass

def GetItemLoc(whichItem:"item")->"location":
    return Location(GetItemX(whichItem), GetItemY(whichItem))
    pass

def GetItemLifeBJ(whichWidget:"widget")->"real":
    return GetWidgetLife(whichWidget)
    pass

def SetItemLifeBJ(whichWidget:"widget", life:"real")->"nothing":
    SetWidgetLife(whichWidget, life)
    pass

def AddHeroXPSwapped(xpToAdd:"integer", whichHero:"unit", showEyeCandy:"boolean")->"nothing":
    AddHeroXP(whichHero, xpToAdd, showEyeCandy)
    pass

def SetHeroLevelBJ(whichHero:"unit", newLevel:"integer", showEyeCandy:"boolean")->"nothing":
    oldLevel = GetHeroLevel(whichHero)
    if ( newLevel > oldLevel ):
        SetHeroLevel(whichHero, newLevel, showEyeCandy)
    elif ( newLevel < oldLevel ):
        UnitStripHeroLevel(whichHero, oldLevel - newLevel)
    pass

def DecUnitAbilityLevelSwapped(abilcode:"integer", whichUnit:"unit")->"integer":
    return DecUnitAbilityLevel(whichUnit, abilcode)
    pass

def IncUnitAbilityLevelSwapped(abilcode:"integer", whichUnit:"unit")->"integer":
    return IncUnitAbilityLevel(whichUnit, abilcode)
    pass

def SetUnitAbilityLevelSwapped(abilcode:"integer", whichUnit:"unit", level:"integer")->"integer":
    return SetUnitAbilityLevel(whichUnit, abilcode, level)
    pass

def GetUnitAbilityLevelSwapped(abilcode:"integer", whichUnit:"unit")->"integer":
    return GetUnitAbilityLevel(whichUnit, abilcode)
    pass

def UnitHasBuffBJ(whichUnit:"unit", buffcode:"integer")->"boolean":
    return ( GetUnitAbilityLevel(whichUnit, buffcode) > 0 )
    pass

def UnitRemoveBuffBJ(buffcode:"integer", whichUnit:"unit")->"boolean":
    return UnitRemoveAbility(whichUnit, buffcode)
    pass

def UnitAddItemSwapped(whichItem:"item", whichHero:"unit")->"boolean":
    return UnitAddItem(whichHero, whichItem)
    pass

def UnitAddItemByIdSwapped(itemId:"integer", whichHero:"unit")->"item":
    global bj_lastCreatedItem
    bj_lastCreatedItem = CreateItem(itemId, GetUnitX(whichHero), GetUnitY(whichHero))
    UnitAddItem(whichHero, bj_lastCreatedItem)
    return bj_lastCreatedItem
    pass

def UnitRemoveItemSwapped(whichItem:"item", whichHero:"unit")->"nothing":
    global bj_lastRemovedItem
    bj_lastRemovedItem = whichItem
    UnitRemoveItem(whichHero, whichItem)
    pass

def UnitRemoveItemFromSlotSwapped(itemSlot:"integer", whichHero:"unit")->"item":
    global bj_lastRemovedItem
    bj_lastRemovedItem = UnitRemoveItemFromSlot(whichHero, itemSlot-1)
    return bj_lastRemovedItem
    pass

def CreateItemLoc(itemId:"integer", loc:"location")->"item":
    global bj_lastCreatedItem
    bj_lastCreatedItem = CreateItem(itemId, GetLocationX(loc), GetLocationY(loc))
    return bj_lastCreatedItem
    pass

def GetLastCreatedItem()->"item":
    return bj_lastCreatedItem
    pass

def GetLastRemovedItem()->"item":
    return bj_lastRemovedItem
    pass

def SetItemPositionLoc(whichItem:"item", loc:"location")->"nothing":
    SetItemPosition(whichItem, GetLocationX(loc), GetLocationY(loc))
    pass

def GetLearnedSkillBJ()->"integer":
    return GetLearnedSkill()
    pass

def SuspendHeroXPBJ(flag:"boolean", whichHero:"unit")->"nothing":
    SuspendHeroXP(whichHero, not  flag)
    pass

def SetPlayerHandicapXPBJ(whichPlayer:"player", handicapPercent:"real")->"nothing":
    SetPlayerHandicapXP(whichPlayer, handicapPercent * 0.01)
    pass

def GetPlayerHandicapXPBJ(whichPlayer:"player")->"real":
    return GetPlayerHandicapXP(whichPlayer) * 100
    pass

def SetPlayerHandicapBJ(whichPlayer:"player", handicapPercent:"real")->"nothing":
    SetPlayerHandicap(whichPlayer, handicapPercent * 0.01)
    pass

def GetPlayerHandicapBJ(whichPlayer:"player")->"real":
    return GetPlayerHandicap(whichPlayer) * 100
    pass

def GetHeroStatBJ(whichStat:"integer", whichHero:"unit", includeBonuses:"boolean")->"integer":
    if ( whichStat == bj_HEROSTAT_STR ):
        return GetHeroStr(whichHero, includeBonuses)
    elif ( whichStat == bj_HEROSTAT_AGI ):
        return GetHeroAgi(whichHero, includeBonuses)
    elif ( whichStat == bj_HEROSTAT_INT ):
        return GetHeroInt(whichHero, includeBonuses)
    else:
        return 0
    pass

def SetHeroStat(whichHero:"unit", whichStat:"integer", value:"integer")->"nothing":
    if ( value <= 0 ):
        pass

    if ( whichStat == bj_HEROSTAT_STR ):
        SetHeroStr(whichHero, value, True)
    elif ( whichStat == bj_HEROSTAT_AGI ):
        SetHeroAgi(whichHero, value, True)
    elif ( whichStat == bj_HEROSTAT_INT ):
        SetHeroInt(whichHero, value, True)
    pass

def ModifyHeroStat(whichStat:"integer", whichHero:"unit", modifyMethod:"integer", value:"integer")->"nothing":
    if ( modifyMethod == bj_MODIFYMETHOD_ADD ):
        SetHeroStat(whichHero, whichStat, GetHeroStatBJ(whichStat, whichHero, False) + value)
    elif ( modifyMethod == bj_MODIFYMETHOD_SUB ):
        SetHeroStat(whichHero, whichStat, GetHeroStatBJ(whichStat, whichHero, False) - value)
    elif ( modifyMethod == bj_MODIFYMETHOD_SET ):
        SetHeroStat(whichHero, whichStat, value)
    pass

def ModifyHeroSkillPoints(whichHero:"unit", modifyMethod:"integer", value:"integer")->"boolean":
    if ( modifyMethod == bj_MODIFYMETHOD_ADD ):
        return UnitModifySkillPoints(whichHero, value)
    elif ( modifyMethod == bj_MODIFYMETHOD_SUB ):
        return UnitModifySkillPoints(whichHero, - value)
    elif ( modifyMethod == bj_MODIFYMETHOD_SET ):
        return UnitModifySkillPoints(whichHero, value - GetHeroSkillPoints(whichHero))
    else:
        return False
    pass

def UnitDropItemPointBJ(whichUnit:"unit", whichItem:"item", x:"real", y:"real")->"boolean":
    return UnitDropItemPoint(whichUnit, whichItem, x, y)
    pass

def UnitDropItemPointLoc(whichUnit:"unit", whichItem:"item", loc:"location")->"boolean":
    return UnitDropItemPoint(whichUnit, whichItem, GetLocationX(loc), GetLocationY(loc))
    pass

def UnitDropItemSlotBJ(whichUnit:"unit", whichItem:"item", slot:"integer")->"boolean":
    return UnitDropItemSlot(whichUnit, whichItem, slot-1)
    pass

def UnitDropItemTargetBJ(whichUnit:"unit", whichItem:"item", target:"widget")->"boolean":
    return UnitDropItemTarget(whichUnit, whichItem, target)
    pass

def UnitUseItemDestructable(whichUnit:"unit", whichItem:"item", target:"widget")->"boolean":
    return UnitUseItemTarget(whichUnit, whichItem, target)
    pass

def UnitUseItemPointLoc(whichUnit:"unit", whichItem:"item", loc:"location")->"boolean":
    return UnitUseItemPoint(whichUnit, whichItem, GetLocationX(loc), GetLocationY(loc))
    pass

def UnitItemInSlotBJ(whichUnit:"unit", itemSlot:"integer")->"item":
    return UnitItemInSlot(whichUnit, itemSlot-1)
    pass

def GetInventoryIndexOfItemTypeBJ(whichUnit:"unit", itemId:"integer")->"integer":
    index = None
    indexItem = None
    index = 0
    while True:
        indexItem = UnitItemInSlot(whichUnit, index)
        if ( indexItem != None ) and ( GetItemTypeId(indexItem) == itemId ):
            return index + 1
        index = index + 1
        if index >= bj_MAX_INVENTORY:
            break
        pass

    return 0
    pass

def GetItemOfTypeFromUnitBJ(whichUnit:"unit", itemId:"integer")->"item":
    index = GetInventoryIndexOfItemTypeBJ(whichUnit, itemId)
    if ( index == 0 ):
        return None
    else:
        return UnitItemInSlot(whichUnit, index - 1)
    pass

def UnitHasItemOfTypeBJ(whichUnit:"unit", itemId:"integer")->"boolean":
    return GetInventoryIndexOfItemTypeBJ(whichUnit, itemId) > 0
    pass

def UnitInventoryCount(whichUnit:"unit")->"integer":
    index = 0
    count = 0
    while True:
        if ( UnitItemInSlot(whichUnit, index) != None ):
            count = count + 1
        index = index + 1
        if index >= bj_MAX_INVENTORY:
            break
        pass

    return count
    pass

def UnitInventorySizeBJ(whichUnit:"unit")->"integer":
    return UnitInventorySize(whichUnit)
    pass

def SetItemInvulnerableBJ(whichItem:"item", flag:"boolean")->"nothing":
    SetItemInvulnerable(whichItem, flag)
    pass

def SetItemDropOnDeathBJ(whichItem:"item", flag:"boolean")->"nothing":
    SetItemDropOnDeath(whichItem, flag)
    pass

def SetItemDroppableBJ(whichItem:"item", flag:"boolean")->"nothing":
    SetItemDroppable(whichItem, flag)
    pass

def SetItemPlayerBJ(whichItem:"item", whichPlayer:"player", changeColor:"boolean")->"nothing":
    SetItemPlayer(whichItem, whichPlayer, changeColor)
    pass

def SetItemVisibleBJ(show:"boolean", whichItem:"item")->"nothing":
    SetItemVisible(whichItem, show)
    pass

def IsItemHiddenBJ(whichItem:"item")->"boolean":
    return not  IsItemVisible(whichItem)
    pass

def ChooseRandomItemBJ(level:"integer")->"integer":
    return ChooseRandomItem(level)
    pass

def ChooseRandomItemExBJ(level:"integer", whichType:"itemtype")->"integer":
    return ChooseRandomItemEx(whichType, level)
    pass

def ChooseRandomNPBuildingBJ()->"integer":
    return ChooseRandomNPBuilding()
    pass

def ChooseRandomCreepBJ(level:"integer")->"integer":
    return ChooseRandomCreep(level)
    pass

def EnumItemsInRectBJ(r:"rect", actionFunc:"code")->"nothing":
    EnumItemsInRect(r, None, actionFunc)
    pass

def RandomItemInRectBJEnum()->"nothing":
    global bj_itemRandomCurrentPick
    global bj_itemRandomConsidered
    bj_itemRandomConsidered = bj_itemRandomConsidered + 1
    if ( GetRandomInt(1, bj_itemRandomConsidered) == 1 ):
        bj_itemRandomCurrentPick = GetEnumItem()
    pass

def RandomItemInRectBJ(r:"rect", filter:"boolexpr")->"item":
    global bj_itemRandomCurrentPick
    global bj_itemRandomConsidered
    bj_itemRandomConsidered = 0
    bj_itemRandomCurrentPick = None
    EnumItemsInRect(r, filter, RandomItemInRectBJEnum)
    DestroyBoolExpr(filter)
    return bj_itemRandomCurrentPick
    pass

def RandomItemInRectSimpleBJ(r:"rect")->"item":
    return RandomItemInRectBJ(r, None)
    pass

def CheckItemStatus(whichItem:"item", status:"integer")->"boolean":
    if ( status == bj_ITEM_STATUS_HIDDEN ):
        return not  IsItemVisible(whichItem)
    elif ( status == bj_ITEM_STATUS_OWNED ):
        return IsItemOwned(whichItem)
    elif ( status == bj_ITEM_STATUS_INVULNERABLE ):
        return IsItemInvulnerable(whichItem)
    elif ( status == bj_ITEM_STATUS_POWERUP ):
        return IsItemPowerup(whichItem)
    elif ( status == bj_ITEM_STATUS_SELLABLE ):
        return IsItemSellable(whichItem)
    elif ( status == bj_ITEM_STATUS_PAWNABLE ):
        return IsItemPawnable(whichItem)
    else:
        return False
    pass

def CheckItemcodeStatus(itemId:"integer", status:"integer")->"boolean":
    if ( status == bj_ITEMCODE_STATUS_POWERUP ):
        return IsItemIdPowerup(itemId)
    elif ( status == bj_ITEMCODE_STATUS_SELLABLE ):
        return IsItemIdSellable(itemId)
    elif ( status == bj_ITEMCODE_STATUS_PAWNABLE ):
        return IsItemIdPawnable(itemId)
    else:
        return False
    pass

def UnitId2OrderIdBJ(unitId:"integer")->"integer":
    return unitId
    pass

def String2UnitIdBJ(unitIdString:"string")->"integer":
    return UnitId(unitIdString)
    pass

def UnitId2StringBJ(unitId:"integer")->"string":
    unitString = UnitId2String(unitId)
    if ( unitString != None ):
        return unitString
    return ""
    pass

def String2OrderIdBJ(orderIdString:"string")->"integer":
    orderId = None
    orderId = OrderId(orderIdString)
    if ( orderId != 0 ):
        return orderId
    orderId = UnitId(orderIdString)
    if ( orderId != 0 ):
        return orderId
    return 0
    pass

def OrderId2StringBJ(orderId:"integer")->"string":
    orderString = None
    orderString = OrderId2String(orderId)
    if ( orderString != None ):
        return orderString
    orderString = UnitId2String(orderId)
    if ( orderString != None ):
        return orderString
    return ""
    pass

def GetIssuedOrderIdBJ()->"integer":
    return GetIssuedOrderId()
    pass

def GetKillingUnitBJ()->"unit":
    return GetKillingUnit()
    pass

def CreateUnitAtLocSaveLast(id:"player", unitid:"integer", loc:"location", face:"real")->"unit":
    global bj_lastCreatedUnit
    if ( unitid == 1969713004 ):
        bj_lastCreatedUnit = CreateBlightedGoldmine(id, GetLocationX(loc), GetLocationY(loc), face)
    else:
        bj_lastCreatedUnit = CreateUnitAtLoc(id, unitid, loc, face)
    return bj_lastCreatedUnit
    pass

def GetLastCreatedUnit()->"unit":
    return bj_lastCreatedUnit
    pass

def CreateNUnitsAtLoc(count:"integer", unitId:"integer", whichPlayer:"player", loc:"location", face:"real")->"group":
    GroupClear(bj_lastCreatedGroup)
    while True:
        count = count - 1
        if count < 0:
            break
        CreateUnitAtLocSaveLast(whichPlayer, unitId, loc, face)
        GroupAddUnit(bj_lastCreatedGroup, bj_lastCreatedUnit)
        pass

    return bj_lastCreatedGroup
    pass

def CreateNUnitsAtLocFacingLocBJ(count:"integer", unitId:"integer", whichPlayer:"player", loc:"location", lookAt:"location")->"group":
    return CreateNUnitsAtLoc(count, unitId, whichPlayer, loc, AngleBetweenPoints(loc, lookAt))
    pass

def GetLastCreatedGroupEnum()->"nothing":
    GroupAddUnit(bj_groupLastCreatedDest, GetEnumUnit())
    pass

def GetLastCreatedGroup()->"group":
    global bj_groupLastCreatedDest
    bj_groupLastCreatedDest = CreateGroup()
    ForGroup(bj_lastCreatedGroup, GetLastCreatedGroupEnum)
    return bj_groupLastCreatedDest
    pass

def CreateCorpseLocBJ(unitid:"integer", whichPlayer:"player", loc:"location")->"unit":
    global bj_lastCreatedUnit
    bj_lastCreatedUnit = CreateCorpse(whichPlayer, unitid, GetLocationX(loc), GetLocationY(loc), GetRandomReal(0, 360))
    return bj_lastCreatedUnit
    pass

def UnitSuspendDecayBJ(suspend:"boolean", whichUnit:"unit")->"nothing":
    UnitSuspendDecay(whichUnit, suspend)
    pass

def DelayedSuspendDecayStopAnimEnum()->"nothing":
    enumUnit = GetEnumUnit()
    if ( GetUnitState(enumUnit, UNIT_STATE_LIFE) <= 0 ):
        SetUnitTimeScale(enumUnit, 0.0001)
    pass

def DelayedSuspendDecayBoneEnum()->"nothing":
    enumUnit = GetEnumUnit()
    if ( GetUnitState(enumUnit, UNIT_STATE_LIFE) <= 0 ):
        UnitSuspendDecay(enumUnit, True)
        SetUnitTimeScale(enumUnit, 0.0001)
    pass

def DelayedSuspendDecayFleshEnum()->"nothing":
    enumUnit = GetEnumUnit()
    if ( GetUnitState(enumUnit, UNIT_STATE_LIFE) <= 0 ):
        UnitSuspendDecay(enumUnit, True)
        SetUnitTimeScale(enumUnit, 10.0)
        SetUnitAnimation(enumUnit, "decay flesh")
    pass

def DelayedSuspendDecay()->"nothing":
    global bj_suspendDecayBoneGroup
    global bj_suspendDecayFleshGroup
    boneGroup = None
    fleshGroup = None
    boneGroup = bj_suspendDecayBoneGroup
    fleshGroup = bj_suspendDecayFleshGroup
    bj_suspendDecayBoneGroup = CreateGroup()
    bj_suspendDecayFleshGroup = CreateGroup()
    ForGroup(fleshGroup, DelayedSuspendDecayStopAnimEnum)
    ForGroup(boneGroup, DelayedSuspendDecayStopAnimEnum)
    TriggerSleepAction(bj_CORPSE_MAX_DEATH_TIME)
    ForGroup(fleshGroup, DelayedSuspendDecayFleshEnum)
    ForGroup(boneGroup, DelayedSuspendDecayBoneEnum)
    TriggerSleepAction(0.05)
    ForGroup(fleshGroup, DelayedSuspendDecayStopAnimEnum)
    DestroyGroup(boneGroup)
    DestroyGroup(fleshGroup)
    pass

def DelayedSuspendDecayCreate()->"nothing":
    global bj_delayedSuspendDecayTrig
    bj_delayedSuspendDecayTrig = CreateTrigger()
    TriggerRegisterTimerExpireEvent(bj_delayedSuspendDecayTrig, bj_delayedSuspendDecayTimer)
    TriggerAddAction(bj_delayedSuspendDecayTrig, DelayedSuspendDecay)
    pass

def CreatePermanentCorpseLocBJ(style:"integer", unitid:"integer", whichPlayer:"player", loc:"location", facing:"real")->"unit":
    global bj_lastCreatedUnit
    bj_lastCreatedUnit = CreateCorpse(whichPlayer, unitid, GetLocationX(loc), GetLocationY(loc), facing)
    SetUnitBlendTime(bj_lastCreatedUnit, 0)
    if ( style == bj_CORPSETYPE_FLESH ):
        SetUnitAnimation(bj_lastCreatedUnit, "decay flesh")
        GroupAddUnit(bj_suspendDecayFleshGroup, bj_lastCreatedUnit)
    elif ( style == bj_CORPSETYPE_BONE ):
        SetUnitAnimation(bj_lastCreatedUnit, "decay bone")
        GroupAddUnit(bj_suspendDecayBoneGroup, bj_lastCreatedUnit)
    else:
        SetUnitAnimation(bj_lastCreatedUnit, "decay bone")
        GroupAddUnit(bj_suspendDecayBoneGroup, bj_lastCreatedUnit)
    TimerStart(bj_delayedSuspendDecayTimer, 0.05, False, None)
    return bj_lastCreatedUnit
    pass

def GetUnitStateSwap(whichState:"unitstate", whichUnit:"unit")->"real":
    return GetUnitState(whichUnit, whichState)
    pass

def GetUnitStatePercent(whichUnit:"unit", whichState:"unitstate", whichMaxState:"unitstate")->"real":
    value = GetUnitState(whichUnit, whichState)
    maxValue = GetUnitState(whichUnit, whichMaxState)
    if ( whichUnit == None ) or ( maxValue == 0 ):
        return 0.0
    return value / maxValue * 100.0
    pass

def GetUnitLifePercent(whichUnit:"unit")->"real":
    return GetUnitStatePercent(whichUnit, UNIT_STATE_LIFE, UNIT_STATE_MAX_LIFE)
    pass

def GetUnitManaPercent(whichUnit:"unit")->"real":
    return GetUnitStatePercent(whichUnit, UNIT_STATE_MANA, UNIT_STATE_MAX_MANA)
    pass

def SelectUnitSingle(whichUnit:"unit")->"nothing":
    ClearSelection()
    SelectUnit(whichUnit, True)
    pass

def SelectGroupBJEnum()->"nothing":
    SelectUnit(GetEnumUnit(), True)
    pass

def SelectGroupBJ(g:"group")->"nothing":
    ClearSelection()
    ForGroup(g, SelectGroupBJEnum)
    pass

def SelectUnitAdd(whichUnit:"unit")->"nothing":
    SelectUnit(whichUnit, True)
    pass

def SelectUnitRemove(whichUnit:"unit")->"nothing":
    SelectUnit(whichUnit, False)
    pass

def ClearSelectionForPlayer(whichPlayer:"player")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        ClearSelection()
    pass

def SelectUnitForPlayerSingle(whichUnit:"unit", whichPlayer:"player")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        ClearSelection()
        SelectUnit(whichUnit, True)
    pass

def SelectGroupForPlayerBJ(g:"group", whichPlayer:"player")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        ClearSelection()
        ForGroup(g, SelectGroupBJEnum)
    pass

def SelectUnitAddForPlayer(whichUnit:"unit", whichPlayer:"player")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        SelectUnit(whichUnit, True)
    pass

def SelectUnitRemoveForPlayer(whichUnit:"unit", whichPlayer:"player")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        SelectUnit(whichUnit, False)
    pass

def SetUnitLifeBJ(whichUnit:"unit", newValue:"real")->"nothing":
    SetUnitState(whichUnit, UNIT_STATE_LIFE, RMaxBJ(0, newValue))
    pass

def SetUnitManaBJ(whichUnit:"unit", newValue:"real")->"nothing":
    SetUnitState(whichUnit, UNIT_STATE_MANA, RMaxBJ(0, newValue))
    pass

def SetUnitLifePercentBJ(whichUnit:"unit", percent:"real")->"nothing":
    SetUnitState(whichUnit, UNIT_STATE_LIFE, GetUnitState(whichUnit, UNIT_STATE_MAX_LIFE) * RMaxBJ(0, percent) * 0.01)
    pass

def SetUnitManaPercentBJ(whichUnit:"unit", percent:"real")->"nothing":
    SetUnitState(whichUnit, UNIT_STATE_MANA, GetUnitState(whichUnit, UNIT_STATE_MAX_MANA) * RMaxBJ(0, percent) * 0.01)
    pass

def IsUnitDeadBJ(whichUnit:"unit")->"boolean":
    return GetUnitState(whichUnit, UNIT_STATE_LIFE) <= 0
    pass

def IsUnitAliveBJ(whichUnit:"unit")->"boolean":
    return not  IsUnitDeadBJ(whichUnit)
    pass

def IsUnitGroupDeadBJEnum()->"nothing":
    global bj_isUnitGroupDeadResult
    if not  IsUnitDeadBJ(GetEnumUnit()):
        bj_isUnitGroupDeadResult = False
    pass

def IsUnitGroupDeadBJ(g:"group")->"boolean":
    global bj_isUnitGroupDeadResult
    global bj_wantDestroyGroup
    wantDestroy = bj_wantDestroyGroup
    bj_wantDestroyGroup = False
    bj_isUnitGroupDeadResult = True
    ForGroup(g, IsUnitGroupDeadBJEnum)
    if ( wantDestroy ):
        DestroyGroup(g)
    return bj_isUnitGroupDeadResult
    pass

def IsUnitGroupEmptyBJEnum()->"nothing":
    global bj_isUnitGroupEmptyResult
    bj_isUnitGroupEmptyResult = False
    pass

def IsUnitGroupEmptyBJ(g:"group")->"boolean":
    global bj_isUnitGroupEmptyResult
    global bj_wantDestroyGroup
    wantDestroy = bj_wantDestroyGroup
    bj_wantDestroyGroup = False
    bj_isUnitGroupEmptyResult = True
    ForGroup(g, IsUnitGroupEmptyBJEnum)
    if ( wantDestroy ):
        DestroyGroup(g)
    return bj_isUnitGroupEmptyResult
    pass

def IsUnitGroupInRectBJEnum()->"nothing":
    global bj_isUnitGroupInRectResult
    if not  RectContainsUnit(bj_isUnitGroupInRectRect, GetEnumUnit()):
        bj_isUnitGroupInRectResult = False
    pass

def IsUnitGroupInRectBJ(g:"group", r:"rect")->"boolean":
    global bj_isUnitGroupInRectRect
    global bj_isUnitGroupInRectResult
    bj_isUnitGroupInRectResult = True
    bj_isUnitGroupInRectRect = r
    ForGroup(g, IsUnitGroupInRectBJEnum)
    return bj_isUnitGroupInRectResult
    pass

def IsUnitHiddenBJ(whichUnit:"unit")->"boolean":
    return IsUnitHidden(whichUnit)
    pass

def ShowUnitHide(whichUnit:"unit")->"nothing":
    ShowUnit(whichUnit, False)
    pass

def ShowUnitShow(whichUnit:"unit")->"nothing":
    if ( IsUnitType(whichUnit, UNIT_TYPE_HERO) and IsUnitDeadBJ(whichUnit) ):
        pass

    ShowUnit(whichUnit, True)
    pass

def IssueHauntOrderAtLocBJFilter()->"boolean":
    return GetUnitTypeId(GetFilterUnit()) == 1852272492
    pass

def IssueHauntOrderAtLocBJ(whichPeon:"unit", loc:"location")->"boolean":
    g = None
    goldMine = None
    g = CreateGroup()
    GroupEnumUnitsInRangeOfLoc(g, loc, 2 * bj_CELLWIDTH, filterIssueHauntOrderAtLocBJ)
    goldMine = FirstOfGroup(g)
    DestroyGroup(g)
    if ( goldMine == None ):
        return False
    return IssueTargetOrderById(whichPeon, 1969713004, goldMine)
    pass

def IssueBuildOrderByIdLocBJ(whichPeon:"unit", unitId:"integer", loc:"location")->"boolean":
    if ( unitId == 1969713004 ):
        return IssueHauntOrderAtLocBJ(whichPeon, loc)
    else:
        return IssueBuildOrderById(whichPeon, unitId, GetLocationX(loc), GetLocationY(loc))
    pass

def IssueTrainOrderByIdBJ(whichUnit:"unit", unitId:"integer")->"boolean":
    return IssueImmediateOrderById(whichUnit, unitId)
    pass

def GroupTrainOrderByIdBJ(g:"group", unitId:"integer")->"boolean":
    return GroupImmediateOrderById(g, unitId)
    pass

def IssueUpgradeOrderByIdBJ(whichUnit:"unit", techId:"integer")->"boolean":
    return IssueImmediateOrderById(whichUnit, techId)
    pass

def GetAttackedUnitBJ()->"unit":
    return GetTriggerUnit()
    pass

def SetUnitFlyHeightBJ(whichUnit:"unit", newHeight:"real", rate:"real")->"nothing":
    SetUnitFlyHeight(whichUnit, newHeight, rate)
    pass

def SetUnitTurnSpeedBJ(whichUnit:"unit", turnSpeed:"real")->"nothing":
    SetUnitTurnSpeed(whichUnit, turnSpeed)
    pass

def SetUnitPropWindowBJ(whichUnit:"unit", propWindow:"real")->"nothing":
    angle = propWindow
    if ( angle <= 0 ):
        angle = 1
    elif ( angle >= 360 ):
        angle = 359
    angle = angle * bj_DEGTORAD
    SetUnitPropWindow(whichUnit, angle)
    pass

def GetUnitPropWindowBJ(whichUnit:"unit")->"real":
    return GetUnitPropWindow(whichUnit) * bj_RADTODEG
    pass

def GetUnitDefaultPropWindowBJ(whichUnit:"unit")->"real":
    return GetUnitDefaultPropWindow(whichUnit)
    pass

def SetUnitBlendTimeBJ(whichUnit:"unit", blendTime:"real")->"nothing":
    SetUnitBlendTime(whichUnit, blendTime)
    pass

def SetUnitAcquireRangeBJ(whichUnit:"unit", acquireRange:"real")->"nothing":
    SetUnitAcquireRange(whichUnit, acquireRange)
    pass

def UnitSetCanSleepBJ(whichUnit:"unit", canSleep:"boolean")->"nothing":
    UnitAddSleep(whichUnit, canSleep)
    pass

def UnitCanSleepBJ(whichUnit:"unit")->"boolean":
    return UnitCanSleep(whichUnit)
    pass

def UnitWakeUpBJ(whichUnit:"unit")->"nothing":
    UnitWakeUp(whichUnit)
    pass

def UnitIsSleepingBJ(whichUnit:"unit")->"boolean":
    return UnitIsSleeping(whichUnit)
    pass

def WakePlayerUnitsEnum()->"nothing":
    UnitWakeUp(GetEnumUnit())
    pass

def WakePlayerUnits(whichPlayer:"player")->"nothing":
    g = CreateGroup()
    GroupEnumUnitsOfPlayer(g, whichPlayer, None)
    ForGroup(g, WakePlayerUnitsEnum)
    DestroyGroup(g)
    pass

def EnableCreepSleepBJ(enable:"boolean")->"nothing":
    SetPlayerState(Player(PLAYER_NEUTRAL_AGGRESSIVE), PLAYER_STATE_NO_CREEP_SLEEP, IntegerTertiaryOp(enable, 0, 1))
    if ( not  enable ):
        WakePlayerUnits(Player(PLAYER_NEUTRAL_AGGRESSIVE))
    pass

def UnitGenerateAlarms(whichUnit:"unit", generate:"boolean")->"boolean":
    return UnitIgnoreAlarm(whichUnit, not  generate)
    pass

def DoesUnitGenerateAlarms(whichUnit:"unit")->"boolean":
    return not  UnitIgnoreAlarmToggled(whichUnit)
    pass

def PauseAllUnitsBJEnum()->"nothing":
    PauseUnit(GetEnumUnit(), bj_pauseAllUnitsFlag)
    pass

def PauseAllUnitsBJ(pause:"boolean")->"nothing":
    global bj_pauseAllUnitsFlag
    index = None
    indexPlayer = None
    g = None
    bj_pauseAllUnitsFlag = pause
    g = CreateGroup()
    index = 0
    while True:
        indexPlayer = Player(index)
        if ( GetPlayerController(indexPlayer) == MAP_CONTROL_COMPUTER ):
            PauseCompAI(indexPlayer, pause)
        GroupEnumUnitsOfPlayer(g, indexPlayer, None)
        ForGroup(g, PauseAllUnitsBJEnum)
        GroupClear(g)
        index = index + 1
        if index == bj_MAX_PLAYER_SLOTS:
            break
        pass

    DestroyGroup(g)
    pass

def PauseUnitBJ(pause:"boolean", whichUnit:"unit")->"nothing":
    PauseUnit(whichUnit, pause)
    pass

def IsUnitPausedBJ(whichUnit:"unit")->"boolean":
    return IsUnitPaused(whichUnit)
    pass

def UnitPauseTimedLifeBJ(flag:"boolean", whichUnit:"unit")->"nothing":
    UnitPauseTimedLife(whichUnit, flag)
    pass

def UnitApplyTimedLifeBJ(duration:"real", buffId:"integer", whichUnit:"unit")->"nothing":
    UnitApplyTimedLife(whichUnit, buffId, duration)
    pass

def UnitShareVisionBJ(share:"boolean", whichUnit:"unit", whichPlayer:"player")->"nothing":
    UnitShareVision(whichUnit, whichPlayer, share)
    pass

def UnitRemoveBuffsBJ(buffType:"integer", whichUnit:"unit")->"nothing":
    if ( buffType == bj_REMOVEBUFFS_POSITIVE ):
        UnitRemoveBuffs(whichUnit, True, False)
    elif ( buffType == bj_REMOVEBUFFS_NEGATIVE ):
        UnitRemoveBuffs(whichUnit, False, True)
    elif ( buffType == bj_REMOVEBUFFS_ALL ):
        UnitRemoveBuffs(whichUnit, True, True)
    elif ( buffType == bj_REMOVEBUFFS_NONTLIFE ):
        UnitRemoveBuffsEx(whichUnit, True, True, False, False, False, True, False)
    pass

def UnitRemoveBuffsExBJ(polarity:"integer", resist:"integer", whichUnit:"unit", bTLife:"boolean", bAura:"boolean")->"nothing":
    bPos = ( polarity == bj_BUFF_POLARITY_EITHER ) or ( polarity == bj_BUFF_POLARITY_POSITIVE )
    bNeg = ( polarity == bj_BUFF_POLARITY_EITHER ) or ( polarity == bj_BUFF_POLARITY_NEGATIVE )
    bMagic = ( resist == bj_BUFF_RESIST_BOTH ) or ( resist == bj_BUFF_RESIST_MAGIC )
    bPhys = ( resist == bj_BUFF_RESIST_BOTH ) or ( resist == bj_BUFF_RESIST_PHYSICAL )
    UnitRemoveBuffsEx(whichUnit, bPos, bNeg, bMagic, bPhys, bTLife, bAura, False)
    pass

def UnitCountBuffsExBJ(polarity:"integer", resist:"integer", whichUnit:"unit", bTLife:"boolean", bAura:"boolean")->"integer":
    bPos = ( polarity == bj_BUFF_POLARITY_EITHER ) or ( polarity == bj_BUFF_POLARITY_POSITIVE )
    bNeg = ( polarity == bj_BUFF_POLARITY_EITHER ) or ( polarity == bj_BUFF_POLARITY_NEGATIVE )
    bMagic = ( resist == bj_BUFF_RESIST_BOTH ) or ( resist == bj_BUFF_RESIST_MAGIC )
    bPhys = ( resist == bj_BUFF_RESIST_BOTH ) or ( resist == bj_BUFF_RESIST_PHYSICAL )
    return UnitCountBuffsEx(whichUnit, bPos, bNeg, bMagic, bPhys, bTLife, bAura, False)
    pass

def UnitRemoveAbilityBJ(abilityId:"integer", whichUnit:"unit")->"boolean":
    return UnitRemoveAbility(whichUnit, abilityId)
    pass

def UnitAddAbilityBJ(abilityId:"integer", whichUnit:"unit")->"boolean":
    return UnitAddAbility(whichUnit, abilityId)
    pass

def UnitRemoveTypeBJ(whichType:"unittype", whichUnit:"unit")->"boolean":
    return UnitRemoveType(whichUnit, whichType)
    pass

def UnitAddTypeBJ(whichType:"unittype", whichUnit:"unit")->"boolean":
    return UnitAddType(whichUnit, whichType)
    pass

def UnitMakeAbilityPermanentBJ(permanent:"boolean", abilityId:"integer", whichUnit:"unit")->"boolean":
    return UnitMakeAbilityPermanent(whichUnit, permanent, abilityId)
    pass

def SetUnitExplodedBJ(whichUnit:"unit", exploded:"boolean")->"nothing":
    SetUnitExploded(whichUnit, exploded)
    pass

def ExplodeUnitBJ(whichUnit:"unit")->"nothing":
    SetUnitExploded(whichUnit, True)
    KillUnit(whichUnit)
    pass

def GetTransportUnitBJ()->"unit":
    return GetTransportUnit()
    pass

def GetLoadedUnitBJ()->"unit":
    return GetLoadedUnit()
    pass

def IsUnitInTransportBJ(whichUnit:"unit", whichTransport:"unit")->"boolean":
    return IsUnitInTransport(whichUnit, whichTransport)
    pass

def IsUnitLoadedBJ(whichUnit:"unit")->"boolean":
    return IsUnitLoaded(whichUnit)
    pass

def IsUnitIllusionBJ(whichUnit:"unit")->"boolean":
    return IsUnitIllusion(whichUnit)
    pass

def ReplaceUnitBJ(whichUnit:"unit", newUnitId:"integer", unitStateMethod:"integer")->"unit":
    global bj_lastReplacedUnit
    oldUnit = whichUnit
    newUnit = None
    wasHidden = None
    index = None
    indexItem = None
    oldRatio = None
    if ( oldUnit == None ):
        bj_lastReplacedUnit = oldUnit
        return oldUnit
    wasHidden = IsUnitHidden(oldUnit)
    ShowUnit(oldUnit, False)
    if ( newUnitId == 1969713004 ):
        newUnit = CreateBlightedGoldmine(GetOwningPlayer(oldUnit), GetUnitX(oldUnit), GetUnitY(oldUnit), GetUnitFacing(oldUnit))
    else:
        newUnit = CreateUnit(GetOwningPlayer(oldUnit), newUnitId, GetUnitX(oldUnit), GetUnitY(oldUnit), GetUnitFacing(oldUnit))
    if ( unitStateMethod == bj_UNIT_STATE_METHOD_RELATIVE ):
        if ( GetUnitState(oldUnit, UNIT_STATE_MAX_LIFE) > 0 ):
            oldRatio = GetUnitState(oldUnit, UNIT_STATE_LIFE) / GetUnitState(oldUnit, UNIT_STATE_MAX_LIFE)
            SetUnitState(newUnit, UNIT_STATE_LIFE, oldRatio * GetUnitState(newUnit, UNIT_STATE_MAX_LIFE))
        if ( GetUnitState(oldUnit, UNIT_STATE_MAX_MANA) > 0 ) and ( GetUnitState(newUnit, UNIT_STATE_MAX_MANA) > 0 ):
            oldRatio = GetUnitState(oldUnit, UNIT_STATE_MANA) / GetUnitState(oldUnit, UNIT_STATE_MAX_MANA)
            SetUnitState(newUnit, UNIT_STATE_MANA, oldRatio * GetUnitState(newUnit, UNIT_STATE_MAX_MANA))
    elif ( unitStateMethod == bj_UNIT_STATE_METHOD_ABSOLUTE ):
        SetUnitState(newUnit, UNIT_STATE_LIFE, GetUnitState(oldUnit, UNIT_STATE_LIFE))
        if ( GetUnitState(newUnit, UNIT_STATE_MAX_MANA) > 0 ):
            SetUnitState(newUnit, UNIT_STATE_MANA, GetUnitState(oldUnit, UNIT_STATE_MANA))
    elif ( unitStateMethod == bj_UNIT_STATE_METHOD_MAXIMUM ):
        SetUnitState(newUnit, UNIT_STATE_LIFE, GetUnitState(newUnit, UNIT_STATE_MAX_LIFE))
        SetUnitState(newUnit, UNIT_STATE_MANA, GetUnitState(newUnit, UNIT_STATE_MAX_MANA))
    SetResourceAmount(newUnit, GetResourceAmount(oldUnit))
    if ( IsUnitType(oldUnit, UNIT_TYPE_HERO) and IsUnitType(newUnit, UNIT_TYPE_HERO) ):
        SetHeroXP(newUnit, GetHeroXP(oldUnit), False)
        index = 0
        while True:
            indexItem = UnitItemInSlot(oldUnit, index)
            if ( indexItem != None ):
                UnitRemoveItem(oldUnit, indexItem)
                UnitAddItem(newUnit, indexItem)
            index = index + 1
            if index >= bj_MAX_INVENTORY:
                break
            pass

    if wasHidden:
        KillUnit(oldUnit)
        RemoveUnit(oldUnit)
    else:
        RemoveUnit(oldUnit)
    bj_lastReplacedUnit = newUnit
    return newUnit
    pass

def GetLastReplacedUnitBJ()->"unit":
    return bj_lastReplacedUnit
    pass

def SetUnitPositionLocFacingBJ(whichUnit:"unit", loc:"location", facing:"real")->"nothing":
    SetUnitPositionLoc(whichUnit, loc)
    SetUnitFacing(whichUnit, facing)
    pass

def SetUnitPositionLocFacingLocBJ(whichUnit:"unit", loc:"location", lookAt:"location")->"nothing":
    SetUnitPositionLoc(whichUnit, loc)
    SetUnitFacing(whichUnit, AngleBetweenPoints(loc, lookAt))
    pass

def AddItemToStockBJ(itemId:"integer", whichUnit:"unit", currentStock:"integer", stockMax:"integer")->"nothing":
    AddItemToStock(whichUnit, itemId, currentStock, stockMax)
    pass

def AddUnitToStockBJ(unitId:"integer", whichUnit:"unit", currentStock:"integer", stockMax:"integer")->"nothing":
    AddUnitToStock(whichUnit, unitId, currentStock, stockMax)
    pass

def RemoveItemFromStockBJ(itemId:"integer", whichUnit:"unit")->"nothing":
    RemoveItemFromStock(whichUnit, itemId)
    pass

def RemoveUnitFromStockBJ(unitId:"integer", whichUnit:"unit")->"nothing":
    RemoveUnitFromStock(whichUnit, unitId)
    pass

def SetUnitUseFoodBJ(enable:"boolean", whichUnit:"unit")->"nothing":
    SetUnitUseFood(whichUnit, enable)
    pass

def UnitDamagePointLoc(whichUnit:"unit", delay:"real", radius:"real", loc:"location", amount:"real", whichAttack:"attacktype", whichDamage:"damagetype")->"boolean":
    return UnitDamagePoint(whichUnit, delay, radius, GetLocationX(loc), GetLocationY(loc), amount, True, False, whichAttack, whichDamage, WEAPON_TYPE_WHOKNOWS)
    pass

def UnitDamageTargetBJ(whichUnit:"unit", target:"unit", amount:"real", whichAttack:"attacktype", whichDamage:"damagetype")->"boolean":
    return UnitDamageTarget(whichUnit, target, amount, True, False, whichAttack, whichDamage, WEAPON_TYPE_WHOKNOWS)
    pass

def CreateDestructableLoc(objectid:"integer", loc:"location", facing:"real", scale:"real", variation:"integer")->"destructable":
    global bj_lastCreatedDestructable
    bj_lastCreatedDestructable = CreateDestructable(objectid, GetLocationX(loc), GetLocationY(loc), facing, scale, variation)
    return bj_lastCreatedDestructable
    pass

def CreateDeadDestructableLocBJ(objectid:"integer", loc:"location", facing:"real", scale:"real", variation:"integer")->"destructable":
    global bj_lastCreatedDestructable
    bj_lastCreatedDestructable = CreateDeadDestructable(objectid, GetLocationX(loc), GetLocationY(loc), facing, scale, variation)
    return bj_lastCreatedDestructable
    pass

def GetLastCreatedDestructable()->"destructable":
    return bj_lastCreatedDestructable
    pass

def ShowDestructableBJ(flag:"boolean", d:"destructable")->"nothing":
    ShowDestructable(d, flag)
    pass

def SetDestructableInvulnerableBJ(d:"destructable", flag:"boolean")->"nothing":
    SetDestructableInvulnerable(d, flag)
    pass

def IsDestructableInvulnerableBJ(d:"destructable")->"boolean":
    return IsDestructableInvulnerable(d)
    pass

def GetDestructableLoc(whichDestructable:"destructable")->"location":
    return Location(GetDestructableX(whichDestructable), GetDestructableY(whichDestructable))
    pass

def EnumDestructablesInRectAll(r:"rect", actionFunc:"code")->"nothing":
    EnumDestructablesInRect(r, None, actionFunc)
    pass

def EnumDestructablesInCircleBJFilter()->"boolean":
    destLoc = GetDestructableLoc(GetFilterDestructable())
    result = None
    result = DistanceBetweenPoints(destLoc, bj_enumDestructableCenter) <= bj_enumDestructableRadius
    RemoveLocation(destLoc)
    return result
    pass

def IsDestructableDeadBJ(d:"destructable")->"boolean":
    return GetDestructableLife(d) <= 0
    pass

def IsDestructableAliveBJ(d:"destructable")->"boolean":
    return not  IsDestructableDeadBJ(d)
    pass

def RandomDestructableInRectBJEnum()->"nothing":
    global bj_destRandomConsidered
    global bj_destRandomCurrentPick
    bj_destRandomConsidered = bj_destRandomConsidered + 1
    if ( GetRandomInt(1, bj_destRandomConsidered) == 1 ):
        bj_destRandomCurrentPick = GetEnumDestructable()
    pass

def RandomDestructableInRectBJ(r:"rect", filter:"boolexpr")->"destructable":
    global bj_destRandomConsidered
    global bj_destRandomCurrentPick
    bj_destRandomConsidered = 0
    bj_destRandomCurrentPick = None
    EnumDestructablesInRect(r, filter, RandomDestructableInRectBJEnum)
    DestroyBoolExpr(filter)
    return bj_destRandomCurrentPick
    pass

def RandomDestructableInRectSimpleBJ(r:"rect")->"destructable":
    return RandomDestructableInRectBJ(r, None)
    pass

def EnumDestructablesInCircleBJ(radius:"real", loc:"location", actionFunc:"code")->"nothing":
    global bj_enumDestructableCenter
    global bj_enumDestructableRadius
    r = None
    if ( radius >= 0 ):
        bj_enumDestructableCenter = loc
        bj_enumDestructableRadius = radius
        r = GetRectFromCircleBJ(loc, radius)
        EnumDestructablesInRect(r, filterEnumDestructablesInCircleBJ, actionFunc)
        RemoveRect(r)
    pass

def SetDestructableLifePercentBJ(d:"destructable", percent:"real")->"nothing":
    SetDestructableLife(d, GetDestructableMaxLife(d) * percent * 0.01)
    pass

def SetDestructableMaxLifeBJ(d:"destructable", max:"real")->"nothing":
    SetDestructableMaxLife(d, max)
    pass

def ModifyGateBJ(gateOperation:"integer", d:"destructable")->"nothing":
    if ( gateOperation == bj_GATEOPERATION_CLOSE ):
        if ( GetDestructableLife(d) <= 0 ):
            DestructableRestoreLife(d, GetDestructableMaxLife(d), True)
        SetDestructableAnimation(d, "stand")
    elif ( gateOperation == bj_GATEOPERATION_OPEN ):
        if ( GetDestructableLife(d) > 0 ):
            KillDestructable(d)
        SetDestructableAnimation(d, "death alternate")
    elif ( gateOperation == bj_GATEOPERATION_DESTROY ):
        if ( GetDestructableLife(d) > 0 ):
            KillDestructable(d)
        SetDestructableAnimation(d, "death")
    pass

def GetElevatorHeight(d:"destructable")->"integer":
    height = None
    height = 1 + R2I(GetDestructableOccluderHeight(d) / bj_CLIFFHEIGHT)
    if ( height < 1 ) or ( height > 3 ):
        height = 1
    return height
    pass

def ChangeElevatorHeight(d:"destructable", newHeight:"integer")->"nothing":
    oldHeight = None
    newHeight = IMaxBJ(1, newHeight)
    newHeight = IMinBJ(3, newHeight)
    oldHeight = GetElevatorHeight(d)
    SetDestructableOccluderHeight(d, bj_CLIFFHEIGHT * ( newHeight-1 ))
    if ( newHeight == 1 ):
        if ( oldHeight == 2 ):
            SetDestructableAnimation(d, "birth")
            QueueDestructableAnimation(d, "stand")
        elif ( oldHeight == 3 ):
            SetDestructableAnimation(d, "birth third")
            QueueDestructableAnimation(d, "stand")
        else:
            SetDestructableAnimation(d, "stand")
    elif ( newHeight == 2 ):
        if ( oldHeight == 1 ):
            SetDestructableAnimation(d, "death")
            QueueDestructableAnimation(d, "stand second")
        elif ( oldHeight == 3 ):
            SetDestructableAnimation(d, "birth second")
            QueueDestructableAnimation(d, "stand second")
        else:
            SetDestructableAnimation(d, "stand second")
    elif ( newHeight == 3 ):
        if ( oldHeight == 1 ):
            SetDestructableAnimation(d, "death third")
            QueueDestructableAnimation(d, "stand third")
        elif ( oldHeight == 2 ):
            SetDestructableAnimation(d, "death second")
            QueueDestructableAnimation(d, "stand third")
        else:
            SetDestructableAnimation(d, "stand third")
    pass

def NudgeUnitsInRectEnum()->"nothing":
    nudgee = GetEnumUnit()
    SetUnitPosition(nudgee, GetUnitX(nudgee), GetUnitY(nudgee))
    pass

def NudgeItemsInRectEnum()->"nothing":
    nudgee = GetEnumItem()
    SetItemPosition(nudgee, GetItemX(nudgee), GetItemY(nudgee))
    pass

def NudgeObjectsInRect(nudgeArea:"rect")->"nothing":
    g = None
    g = CreateGroup()
    GroupEnumUnitsInRect(g, nudgeArea, None)
    ForGroup(g, NudgeUnitsInRectEnum)
    DestroyGroup(g)
    EnumItemsInRect(nudgeArea, None, NudgeItemsInRectEnum)
    pass

def NearbyElevatorExistsEnum()->"nothing":
    global bj_elevatorNeighbor
    d = GetEnumDestructable()
    dType = GetDestructableTypeId(d)
    if ( dType == bj_ELEVATOR_CODE01 ) or ( dType == bj_ELEVATOR_CODE02 ):
        bj_elevatorNeighbor = d
    pass

def NearbyElevatorExists(x:"real", y:"real")->"boolean":
    global bj_elevatorNeighbor
    findThreshold = 32
    r = None
    r = Rect(x - findThreshold, y - findThreshold, x + findThreshold, y + findThreshold)
    bj_elevatorNeighbor = None
    EnumDestructablesInRect(r, None, NearbyElevatorExistsEnum)
    RemoveRect(r)
    return bj_elevatorNeighbor != None
    pass

def FindElevatorWallBlockerEnum()->"nothing":
    global bj_elevatorWallBlocker
    bj_elevatorWallBlocker = GetEnumDestructable()
    pass

def ChangeElevatorWallBlocker(x:"real", y:"real", facing:"real", open:"boolean")->"nothing":
    global bj_elevatorWallBlocker
    blocker = None
    findThreshold = 32
    nudgeLength = 4.25 * bj_CELLWIDTH
    nudgeWidth = 1.25 * bj_CELLWIDTH
    r = None
    r = Rect(x - findThreshold, y - findThreshold, x + findThreshold, y + findThreshold)
    bj_elevatorWallBlocker = None
    EnumDestructablesInRect(r, None, FindElevatorWallBlockerEnum)
    RemoveRect(r)
    blocker = bj_elevatorWallBlocker
    if ( blocker == None ):
        blocker = CreateDeadDestructable(bj_ELEVATOR_BLOCKER_CODE, x, y, facing, 1, 0)
    if ( open ):
        if ( GetDestructableLife(blocker) > 0 ):
            KillDestructable(blocker)
    else:
        if ( GetDestructableLife(blocker) <= 0 ):
            DestructableRestoreLife(blocker, GetDestructableMaxLife(blocker), False)
        if ( facing == 0 ):
            r = Rect(x - nudgeWidth / 2, y - nudgeLength / 2, x + nudgeWidth / 2, y + nudgeLength / 2)
            NudgeObjectsInRect(r)
            RemoveRect(r)
        elif ( facing == 90 ):
            r = Rect(x - nudgeLength / 2, y - nudgeWidth / 2, x + nudgeLength / 2, y + nudgeWidth / 2)
            NudgeObjectsInRect(r)
            RemoveRect(r)
    pass

def ChangeElevatorWalls(open:"boolean", walls:"integer", d:"destructable")->"nothing":
    x = GetDestructableX(d)
    y = GetDestructableY(d)
    distToBlocker = 192
    distToNeighbor = 256
    if ( walls == bj_ELEVATOR_WALL_TYPE_ALL ) or ( walls == bj_ELEVATOR_WALL_TYPE_EAST ):
        if ( not  NearbyElevatorExists(x + distToNeighbor, y) ):
            ChangeElevatorWallBlocker(x + distToBlocker, y, 0, open)
    if ( walls == bj_ELEVATOR_WALL_TYPE_ALL ) or ( walls == bj_ELEVATOR_WALL_TYPE_NORTH ):
        if ( not  NearbyElevatorExists(x, y + distToNeighbor) ):
            ChangeElevatorWallBlocker(x, y + distToBlocker, 90, open)
    if ( walls == bj_ELEVATOR_WALL_TYPE_ALL ) or ( walls == bj_ELEVATOR_WALL_TYPE_SOUTH ):
        if ( not  NearbyElevatorExists(x, y - distToNeighbor) ):
            ChangeElevatorWallBlocker(x, y - distToBlocker, 90, open)
    if ( walls == bj_ELEVATOR_WALL_TYPE_ALL ) or ( walls == bj_ELEVATOR_WALL_TYPE_WEST ):
        if ( not  NearbyElevatorExists(x - distToNeighbor, y) ):
            ChangeElevatorWallBlocker(x - distToBlocker, y, 0, open)
    pass

def WaygateActivateBJ(activate:"boolean", waygate:"unit")->"nothing":
    WaygateActivate(waygate, activate)
    pass

def WaygateIsActiveBJ(waygate:"unit")->"boolean":
    return WaygateIsActive(waygate)
    pass

def WaygateSetDestinationLocBJ(waygate:"unit", loc:"location")->"nothing":
    WaygateSetDestination(waygate, GetLocationX(loc), GetLocationY(loc))
    pass

def WaygateGetDestinationLocBJ(waygate:"unit")->"location":
    return Location(WaygateGetDestinationX(waygate), WaygateGetDestinationY(waygate))
    pass

def UnitSetUsesAltIconBJ(flag:"boolean", whichUnit:"unit")->"nothing":
    UnitSetUsesAltIcon(whichUnit, flag)
    pass

def ForceUIKeyBJ(whichPlayer:"player", key:"string")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        ForceUIKey(key)
    pass

def ForceUICancelBJ(whichPlayer:"player")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        ForceUICancel()
    pass

def ForGroupBJ(whichGroup:"group", callback:"code")->"nothing":
    global bj_wantDestroyGroup
    wantDestroy = bj_wantDestroyGroup
    bj_wantDestroyGroup = False
    ForGroup(whichGroup, callback)
    if ( wantDestroy ):
        DestroyGroup(whichGroup)
    pass

def GroupAddUnitSimple(whichUnit:"unit", whichGroup:"group")->"nothing":
    GroupAddUnit(whichGroup, whichUnit)
    pass

def GroupRemoveUnitSimple(whichUnit:"unit", whichGroup:"group")->"nothing":
    GroupRemoveUnit(whichGroup, whichUnit)
    pass

def GroupAddGroupEnum()->"nothing":
    GroupAddUnit(bj_groupAddGroupDest, GetEnumUnit())
    pass

def GroupAddGroup(sourceGroup:"group", destGroup:"group")->"nothing":
    global bj_wantDestroyGroup
    global bj_groupAddGroupDest
    wantDestroy = bj_wantDestroyGroup
    bj_wantDestroyGroup = False
    bj_groupAddGroupDest = destGroup
    ForGroup(sourceGroup, GroupAddGroupEnum)
    if ( wantDestroy ):
        DestroyGroup(sourceGroup)
    pass

def GroupRemoveGroupEnum()->"nothing":
    GroupRemoveUnit(bj_groupRemoveGroupDest, GetEnumUnit())
    pass

def GroupRemoveGroup(sourceGroup:"group", destGroup:"group")->"nothing":
    global bj_wantDestroyGroup
    global bj_groupRemoveGroupDest
    wantDestroy = bj_wantDestroyGroup
    bj_wantDestroyGroup = False
    bj_groupRemoveGroupDest = destGroup
    ForGroup(sourceGroup, GroupRemoveGroupEnum)
    if ( wantDestroy ):
        DestroyGroup(sourceGroup)
    pass

def ForceAddPlayerSimple(whichPlayer:"player", whichForce:"force")->"nothing":
    ForceAddPlayer(whichForce, whichPlayer)
    pass

def ForceRemovePlayerSimple(whichPlayer:"player", whichForce:"force")->"nothing":
    ForceRemovePlayer(whichForce, whichPlayer)
    pass

def GroupPickRandomUnitEnum()->"nothing":
    global bj_groupRandomCurrentPick
    global bj_groupRandomConsidered
    bj_groupRandomConsidered = bj_groupRandomConsidered + 1
    if ( GetRandomInt(1, bj_groupRandomConsidered) == 1 ):
        bj_groupRandomCurrentPick = GetEnumUnit()
    pass

def GroupPickRandomUnit(whichGroup:"group")->"unit":
    global bj_wantDestroyGroup
    global bj_groupRandomCurrentPick
    global bj_groupRandomConsidered
    wantDestroy = bj_wantDestroyGroup
    bj_wantDestroyGroup = False
    bj_groupRandomConsidered = 0
    bj_groupRandomCurrentPick = None
    ForGroup(whichGroup, GroupPickRandomUnitEnum)
    if ( wantDestroy ):
        DestroyGroup(whichGroup)
    return bj_groupRandomCurrentPick
    pass

def ForcePickRandomPlayerEnum()->"nothing":
    global bj_forceRandomConsidered
    global bj_forceRandomCurrentPick
    bj_forceRandomConsidered = bj_forceRandomConsidered + 1
    if ( GetRandomInt(1, bj_forceRandomConsidered) == 1 ):
        bj_forceRandomCurrentPick = GetEnumPlayer()
    pass

def ForcePickRandomPlayer(whichForce:"force")->"player":
    global bj_forceRandomConsidered
    global bj_forceRandomCurrentPick
    bj_forceRandomConsidered = 0
    bj_forceRandomCurrentPick = None
    ForForce(whichForce, ForcePickRandomPlayerEnum)
    return bj_forceRandomCurrentPick
    pass

def EnumUnitsSelected(whichPlayer:"player", enumFilter:"boolexpr", enumAction:"code")->"nothing":
    g = CreateGroup()
    SyncSelections()
    GroupEnumUnitsSelected(g, whichPlayer, enumFilter)
    DestroyBoolExpr(enumFilter)
    ForGroup(g, enumAction)
    DestroyGroup(g)
    pass

def GetUnitsInRectMatching(r:"rect", filter:"boolexpr")->"group":
    g = CreateGroup()
    GroupEnumUnitsInRect(g, r, filter)
    DestroyBoolExpr(filter)
    return g
    pass

def GetUnitsInRectAll(r:"rect")->"group":
    return GetUnitsInRectMatching(r, None)
    pass

def GetUnitsInRectOfPlayerFilter()->"boolean":
    return GetOwningPlayer(GetFilterUnit()) == bj_groupEnumOwningPlayer
    pass

def GetUnitsInRectOfPlayer(r:"rect", whichPlayer:"player")->"group":
    global bj_groupEnumOwningPlayer
    g = CreateGroup()
    bj_groupEnumOwningPlayer = whichPlayer
    GroupEnumUnitsInRect(g, r, filterGetUnitsInRectOfPlayer)
    return g
    pass

def GetUnitsInRangeOfLocMatching(radius:"real", whichLocation:"location", filter:"boolexpr")->"group":
    g = CreateGroup()
    GroupEnumUnitsInRangeOfLoc(g, whichLocation, radius, filter)
    DestroyBoolExpr(filter)
    return g
    pass

def GetUnitsInRangeOfLocAll(radius:"real", whichLocation:"location")->"group":
    return GetUnitsInRangeOfLocMatching(radius, whichLocation, None)
    pass

def GetUnitsOfTypeIdAllFilter()->"boolean":
    return GetUnitTypeId(GetFilterUnit()) == bj_groupEnumTypeId
    pass

def GetUnitsOfTypeIdAll(unitid:"integer")->"group":
    global bj_groupEnumTypeId
    result = CreateGroup()
    g = CreateGroup()
    index = None
    index = 0
    while True:
        bj_groupEnumTypeId = unitid
        GroupClear(g)
        GroupEnumUnitsOfPlayer(g, Player(index), filterGetUnitsOfTypeIdAll)
        GroupAddGroup(g, result)
        index = index + 1
        if index == bj_MAX_PLAYER_SLOTS:
            break
        pass

    DestroyGroup(g)
    return result
    pass

def GetUnitsOfPlayerMatching(whichPlayer:"player", filter:"boolexpr")->"group":
    g = CreateGroup()
    GroupEnumUnitsOfPlayer(g, whichPlayer, filter)
    DestroyBoolExpr(filter)
    return g
    pass

def GetUnitsOfPlayerAll(whichPlayer:"player")->"group":
    return GetUnitsOfPlayerMatching(whichPlayer, None)
    pass

def GetUnitsOfPlayerAndTypeIdFilter()->"boolean":
    return GetUnitTypeId(GetFilterUnit()) == bj_groupEnumTypeId
    pass

def GetUnitsOfPlayerAndTypeId(whichPlayer:"player", unitid:"integer")->"group":
    global bj_groupEnumTypeId
    g = CreateGroup()
    bj_groupEnumTypeId = unitid
    GroupEnumUnitsOfPlayer(g, whichPlayer, filterGetUnitsOfPlayerAndTypeId)
    return g
    pass

def GetUnitsSelectedAll(whichPlayer:"player")->"group":
    g = CreateGroup()
    SyncSelections()
    GroupEnumUnitsSelected(g, whichPlayer, None)
    return g
    pass

def GetForceOfPlayer(whichPlayer:"player")->"force":
    f = CreateForce()
    ForceAddPlayer(f, whichPlayer)
    return f
    pass

def GetPlayersAll()->"force":
    return bj_FORCE_ALL_PLAYERS
    pass

def GetPlayersByMapControl(whichControl:"mapcontrol")->"force":
    f = CreateForce()
    playerIndex = None
    indexPlayer = None
    playerIndex = 0
    while True:
        indexPlayer = Player(playerIndex)
        if GetPlayerController(indexPlayer) == whichControl:
            ForceAddPlayer(f, indexPlayer)
        playerIndex = playerIndex + 1
        if playerIndex == bj_MAX_PLAYER_SLOTS:
            break
        pass

    return f
    pass

def GetPlayersAllies(whichPlayer:"player")->"force":
    f = CreateForce()
    ForceEnumAllies(f, whichPlayer, None)
    return f
    pass

def GetPlayersEnemies(whichPlayer:"player")->"force":
    f = CreateForce()
    ForceEnumEnemies(f, whichPlayer, None)
    return f
    pass

def GetPlayersMatching(filter:"boolexpr")->"force":
    f = CreateForce()
    ForceEnumPlayers(f, filter)
    DestroyBoolExpr(filter)
    return f
    pass

def CountUnitsInGroupEnum()->"nothing":
    global bj_groupCountUnits
    bj_groupCountUnits = bj_groupCountUnits + 1
    pass

def CountUnitsInGroup(g:"group")->"integer":
    global bj_groupCountUnits
    global bj_wantDestroyGroup
    wantDestroy = bj_wantDestroyGroup
    bj_wantDestroyGroup = False
    bj_groupCountUnits = 0
    ForGroup(g, CountUnitsInGroupEnum)
    if ( wantDestroy ):
        DestroyGroup(g)
    return bj_groupCountUnits
    pass

def CountPlayersInForceEnum()->"nothing":
    global bj_forceCountPlayers
    bj_forceCountPlayers = bj_forceCountPlayers + 1
    pass

def CountPlayersInForceBJ(f:"force")->"integer":
    global bj_forceCountPlayers
    bj_forceCountPlayers = 0
    ForForce(f, CountPlayersInForceEnum)
    return bj_forceCountPlayers
    pass

def GetRandomSubGroupEnum()->"nothing":
    global bj_randomSubGroupTotal
    global bj_randomSubGroupWant
    if ( bj_randomSubGroupWant > 0 ):
        if ( bj_randomSubGroupWant >= bj_randomSubGroupTotal ) or ( GetRandomReal(0, 1) < bj_randomSubGroupChance ):
            GroupAddUnit(bj_randomSubGroupGroup, GetEnumUnit())
            bj_randomSubGroupWant = bj_randomSubGroupWant - 1
    bj_randomSubGroupTotal = bj_randomSubGroupTotal - 1
    pass

def GetRandomSubGroup(count:"integer", sourceGroup:"group")->"group":
    global bj_randomSubGroupTotal
    global bj_randomSubGroupChance
    global bj_randomSubGroupGroup
    global bj_randomSubGroupWant
    g = CreateGroup()
    bj_randomSubGroupGroup = g
    bj_randomSubGroupWant = count
    bj_randomSubGroupTotal = CountUnitsInGroup(sourceGroup)
    if ( bj_randomSubGroupWant <= 0 or bj_randomSubGroupTotal <= 0 ):
        return g
    bj_randomSubGroupChance = I2R(bj_randomSubGroupWant) / I2R(bj_randomSubGroupTotal)
    ForGroup(sourceGroup, GetRandomSubGroupEnum)
    return g
    pass

def LivingPlayerUnitsOfTypeIdFilter()->"boolean":
    filterUnit = GetFilterUnit()
    return IsUnitAliveBJ(filterUnit) and GetUnitTypeId(filterUnit) == bj_livingPlayerUnitsTypeId
    pass

def CountLivingPlayerUnitsOfTypeId(unitId:"integer", whichPlayer:"player")->"integer":
    global bj_livingPlayerUnitsTypeId
    g = None
    matchedCount = None
    g = CreateGroup()
    bj_livingPlayerUnitsTypeId = unitId
    GroupEnumUnitsOfPlayer(g, whichPlayer, filterLivingPlayerUnitsOfTypeId)
    matchedCount = CountUnitsInGroup(g)
    DestroyGroup(g)
    return matchedCount
    pass

def ResetUnitAnimation(whichUnit:"unit")->"nothing":
    SetUnitAnimation(whichUnit, "stand")
    pass

def SetUnitTimeScalePercent(whichUnit:"unit", percentScale:"real")->"nothing":
    SetUnitTimeScale(whichUnit, percentScale * 0.01)
    pass

def SetUnitScalePercent(whichUnit:"unit", percentScaleX:"real", percentScaleY:"real", percentScaleZ:"real")->"nothing":
    SetUnitScale(whichUnit, percentScaleX * 0.01, percentScaleY * 0.01, percentScaleZ * 0.01)
    pass

def SetUnitVertexColorBJ(whichUnit:"unit", red:"real", green:"real", blue:"real", transparency:"real")->"nothing":
    SetUnitVertexColor(whichUnit, PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - transparency))
    pass

def UnitAddIndicatorBJ(whichUnit:"unit", red:"real", green:"real", blue:"real", transparency:"real")->"nothing":
    AddIndicator(whichUnit, PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - transparency))
    pass

def DestructableAddIndicatorBJ(whichDestructable:"destructable", red:"real", green:"real", blue:"real", transparency:"real")->"nothing":
    AddIndicator(whichDestructable, PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - transparency))
    pass

def ItemAddIndicatorBJ(whichItem:"item", red:"real", green:"real", blue:"real", transparency:"real")->"nothing":
    AddIndicator(whichItem, PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - transparency))
    pass

def SetUnitFacingToFaceLocTimed(whichUnit:"unit", target:"location", duration:"real")->"nothing":
    unitLoc = GetUnitLoc(whichUnit)
    SetUnitFacingTimed(whichUnit, AngleBetweenPoints(unitLoc, target), duration)
    RemoveLocation(unitLoc)
    pass

def SetUnitFacingToFaceUnitTimed(whichUnit:"unit", target:"unit", duration:"real")->"nothing":
    unitLoc = GetUnitLoc(target)
    SetUnitFacingToFaceLocTimed(whichUnit, unitLoc, duration)
    RemoveLocation(unitLoc)
    pass

def QueueUnitAnimationBJ(whichUnit:"unit", whichAnimation:"string")->"nothing":
    QueueUnitAnimation(whichUnit, whichAnimation)
    pass

def SetDestructableAnimationBJ(d:"destructable", whichAnimation:"string")->"nothing":
    SetDestructableAnimation(d, whichAnimation)
    pass

def QueueDestructableAnimationBJ(d:"destructable", whichAnimation:"string")->"nothing":
    QueueDestructableAnimation(d, whichAnimation)
    pass

def SetDestAnimationSpeedPercent(d:"destructable", percentScale:"real")->"nothing":
    SetDestructableAnimationSpeed(d, percentScale * 0.01)
    pass

def DialogDisplayBJ(flag:"boolean", whichDialog:"dialog", whichPlayer:"player")->"nothing":
    DialogDisplay(whichPlayer, whichDialog, flag)
    pass

def DialogSetMessageBJ(whichDialog:"dialog", message:"string")->"nothing":
    DialogSetMessage(whichDialog, message)
    pass

def DialogAddButtonBJ(whichDialog:"dialog", buttonText:"string")->"button":
    global bj_lastCreatedButton
    bj_lastCreatedButton = DialogAddButton(whichDialog, buttonText, 0)
    return bj_lastCreatedButton
    pass

def DialogAddButtonWithHotkeyBJ(whichDialog:"dialog", buttonText:"string", hotkey:"integer")->"button":
    global bj_lastCreatedButton
    bj_lastCreatedButton = DialogAddButton(whichDialog, buttonText, hotkey)
    return bj_lastCreatedButton
    pass

def DialogClearBJ(whichDialog:"dialog")->"nothing":
    DialogClear(whichDialog)
    pass

def GetLastCreatedButtonBJ()->"button":
    return bj_lastCreatedButton
    pass

def GetClickedButtonBJ()->"button":
    return GetClickedButton()
    pass

def GetClickedDialogBJ()->"dialog":
    return GetClickedDialog()
    pass

def SetPlayerAllianceBJ(sourcePlayer:"player", whichAllianceSetting:"alliancetype", value:"boolean", otherPlayer:"player")->"nothing":
    if ( sourcePlayer == otherPlayer ):
        pass

    SetPlayerAlliance(sourcePlayer, otherPlayer, whichAllianceSetting, value)
    pass

def SetPlayerAllianceStateAllyBJ(sourcePlayer:"player", otherPlayer:"player", flag:"boolean")->"nothing":
    SetPlayerAlliance(sourcePlayer, otherPlayer, ALLIANCE_PASSIVE, flag)
    SetPlayerAlliance(sourcePlayer, otherPlayer, ALLIANCE_HELP_REQUEST, flag)
    SetPlayerAlliance(sourcePlayer, otherPlayer, ALLIANCE_HELP_RESPONSE, flag)
    SetPlayerAlliance(sourcePlayer, otherPlayer, ALLIANCE_SHARED_XP, flag)
    SetPlayerAlliance(sourcePlayer, otherPlayer, ALLIANCE_SHARED_SPELLS, flag)
    pass

def SetPlayerAllianceStateVisionBJ(sourcePlayer:"player", otherPlayer:"player", flag:"boolean")->"nothing":
    SetPlayerAlliance(sourcePlayer, otherPlayer, ALLIANCE_SHARED_VISION, flag)
    pass

def SetPlayerAllianceStateControlBJ(sourcePlayer:"player", otherPlayer:"player", flag:"boolean")->"nothing":
    SetPlayerAlliance(sourcePlayer, otherPlayer, ALLIANCE_SHARED_CONTROL, flag)
    pass

def SetPlayerAllianceStateFullControlBJ(sourcePlayer:"player", otherPlayer:"player", flag:"boolean")->"nothing":
    SetPlayerAlliance(sourcePlayer, otherPlayer, ALLIANCE_SHARED_ADVANCED_CONTROL, flag)
    pass

def SetPlayerAllianceStateBJ(sourcePlayer:"player", otherPlayer:"player", allianceState:"integer")->"nothing":
    if ( sourcePlayer == otherPlayer ):
        pass

    if allianceState == bj_ALLIANCE_UNALLIED:
        SetPlayerAllianceStateAllyBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAllianceStateVisionBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAllianceStateControlBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAllianceStateFullControlBJ(sourcePlayer, otherPlayer, False)
    elif allianceState == bj_ALLIANCE_UNALLIED_VISION:
        SetPlayerAllianceStateAllyBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAllianceStateVisionBJ(sourcePlayer, otherPlayer, True)
        SetPlayerAllianceStateControlBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAllianceStateFullControlBJ(sourcePlayer, otherPlayer, False)
    elif allianceState == bj_ALLIANCE_ALLIED:
        SetPlayerAllianceStateAllyBJ(sourcePlayer, otherPlayer, True)
        SetPlayerAllianceStateVisionBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAllianceStateControlBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAllianceStateFullControlBJ(sourcePlayer, otherPlayer, False)
    elif allianceState == bj_ALLIANCE_ALLIED_VISION:
        SetPlayerAllianceStateAllyBJ(sourcePlayer, otherPlayer, True)
        SetPlayerAllianceStateVisionBJ(sourcePlayer, otherPlayer, True)
        SetPlayerAllianceStateControlBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAllianceStateFullControlBJ(sourcePlayer, otherPlayer, False)
    elif allianceState == bj_ALLIANCE_ALLIED_UNITS:
        SetPlayerAllianceStateAllyBJ(sourcePlayer, otherPlayer, True)
        SetPlayerAllianceStateVisionBJ(sourcePlayer, otherPlayer, True)
        SetPlayerAllianceStateControlBJ(sourcePlayer, otherPlayer, True)
        SetPlayerAllianceStateFullControlBJ(sourcePlayer, otherPlayer, False)
    elif allianceState == bj_ALLIANCE_ALLIED_ADVUNITS:
        SetPlayerAllianceStateAllyBJ(sourcePlayer, otherPlayer, True)
        SetPlayerAllianceStateVisionBJ(sourcePlayer, otherPlayer, True)
        SetPlayerAllianceStateControlBJ(sourcePlayer, otherPlayer, True)
        SetPlayerAllianceStateFullControlBJ(sourcePlayer, otherPlayer, True)
    elif allianceState == bj_ALLIANCE_NEUTRAL:
        SetPlayerAllianceStateAllyBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAllianceStateVisionBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAllianceStateControlBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAllianceStateFullControlBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAlliance(sourcePlayer, otherPlayer, ALLIANCE_PASSIVE, True)
    elif allianceState == bj_ALLIANCE_NEUTRAL_VISION:
        SetPlayerAllianceStateAllyBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAllianceStateVisionBJ(sourcePlayer, otherPlayer, True)
        SetPlayerAllianceStateControlBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAllianceStateFullControlBJ(sourcePlayer, otherPlayer, False)
        SetPlayerAlliance(sourcePlayer, otherPlayer, ALLIANCE_PASSIVE, True)
    pass

def SetForceAllianceStateBJ(sourceForce:"force", targetForce:"force", allianceState:"integer")->"nothing":
    sourceIndex = None
    targetIndex = None
    sourceIndex = 0
    while True:
        if ( sourceForce == bj_FORCE_ALL_PLAYERS or IsPlayerInForce(Player(sourceIndex), sourceForce) ):
            targetIndex = 0
            while True:
                if ( targetForce == bj_FORCE_ALL_PLAYERS or IsPlayerInForce(Player(targetIndex), targetForce) ):
                    SetPlayerAllianceStateBJ(Player(sourceIndex), Player(targetIndex), allianceState)
                targetIndex = targetIndex + 1
                if targetIndex == bj_MAX_PLAYER_SLOTS:
                    break
                pass

        sourceIndex = sourceIndex + 1
        if sourceIndex == bj_MAX_PLAYER_SLOTS:
            break
        pass

    pass

def PlayersAreCoAllied(playerA:"player", playerB:"player")->"boolean":
    if ( playerA == playerB ):
        return True
    if GetPlayerAlliance(playerA, playerB, ALLIANCE_PASSIVE):
        if GetPlayerAlliance(playerB, playerA, ALLIANCE_PASSIVE):
            return True
    return False
    pass

def ShareEverythingWithTeamAI(whichPlayer:"player")->"nothing":
    playerIndex = None
    indexPlayer = None
    playerIndex = 0
    while True:
        indexPlayer = Player(playerIndex)
        if ( PlayersAreCoAllied(whichPlayer, indexPlayer) and whichPlayer != indexPlayer ):
            if ( GetPlayerController(indexPlayer) == MAP_CONTROL_COMPUTER ):
                SetPlayerAlliance(whichPlayer, indexPlayer, ALLIANCE_SHARED_VISION, True)
                SetPlayerAlliance(whichPlayer, indexPlayer, ALLIANCE_SHARED_CONTROL, True)
                SetPlayerAlliance(whichPlayer, indexPlayer, ALLIANCE_SHARED_ADVANCED_CONTROL, True)
        playerIndex = playerIndex + 1
        if playerIndex == bj_MAX_PLAYERS:
            break
        pass

    pass

def ShareEverythingWithTeam(whichPlayer:"player")->"nothing":
    playerIndex = None
    indexPlayer = None
    playerIndex = 0
    while True:
        indexPlayer = Player(playerIndex)
        if ( PlayersAreCoAllied(whichPlayer, indexPlayer) and whichPlayer != indexPlayer ):
            SetPlayerAlliance(whichPlayer, indexPlayer, ALLIANCE_SHARED_VISION, True)
            SetPlayerAlliance(whichPlayer, indexPlayer, ALLIANCE_SHARED_CONTROL, True)
            SetPlayerAlliance(indexPlayer, whichPlayer, ALLIANCE_SHARED_CONTROL, True)
            SetPlayerAlliance(whichPlayer, indexPlayer, ALLIANCE_SHARED_ADVANCED_CONTROL, True)
        playerIndex = playerIndex + 1
        if playerIndex == bj_MAX_PLAYERS:
            break
        pass

    pass

def ConfigureNeutralVictim()->"nothing":
    index = None
    indexPlayer = None
    neutralVictim = Player(bj_PLAYER_NEUTRAL_VICTIM)
    index = 0
    while True:
        indexPlayer = Player(index)
        SetPlayerAlliance(neutralVictim, indexPlayer, ALLIANCE_PASSIVE, True)
        SetPlayerAlliance(indexPlayer, neutralVictim, ALLIANCE_PASSIVE, False)
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    indexPlayer = Player(PLAYER_NEUTRAL_AGGRESSIVE)
    SetPlayerAlliance(neutralVictim, indexPlayer, ALLIANCE_PASSIVE, True)
    SetPlayerAlliance(indexPlayer, neutralVictim, ALLIANCE_PASSIVE, True)
    SetPlayerState(neutralVictim, PLAYER_STATE_GIVES_BOUNTY, 0)
    pass

def MakeUnitsPassiveForPlayerEnum()->"nothing":
    SetUnitOwner(GetEnumUnit(), Player(bj_PLAYER_NEUTRAL_VICTIM), False)
    pass

def MakeUnitsPassiveForPlayer(whichPlayer:"player")->"nothing":
    playerUnits = CreateGroup()
    CachePlayerHeroData(whichPlayer)
    GroupEnumUnitsOfPlayer(playerUnits, whichPlayer, None)
    ForGroup(playerUnits, MakeUnitsPassiveForPlayerEnum)
    DestroyGroup(playerUnits)
    pass

def MakeUnitsPassiveForTeam(whichPlayer:"player")->"nothing":
    playerIndex = None
    indexPlayer = None
    playerIndex = 0
    while True:
        indexPlayer = Player(playerIndex)
        if PlayersAreCoAllied(whichPlayer, indexPlayer):
            MakeUnitsPassiveForPlayer(indexPlayer)
        playerIndex = playerIndex + 1
        if playerIndex == bj_MAX_PLAYERS:
            break
        pass

    pass

def AllowVictoryDefeat(gameResult:"playergameresult")->"boolean":
    if ( gameResult == PLAYER_GAME_RESULT_VICTORY ):
        return not  IsNoVictoryCheat()
    if ( gameResult == PLAYER_GAME_RESULT_DEFEAT ):
        return not  IsNoDefeatCheat()
    if ( gameResult == PLAYER_GAME_RESULT_NEUTRAL ):
        return ( not  IsNoVictoryCheat() ) and ( not  IsNoDefeatCheat() )
    return True
    pass

def EndGameBJ()->"nothing":
    EndGame(True)
    pass

def MeleeVictoryDialogBJ(whichPlayer:"player", leftGame:"boolean")->"nothing":
    t = CreateTrigger()
    d = DialogCreate()
    formatString = None
    if ( leftGame ):
        formatString = GetLocalizedString("PLAYER_LEFT_GAME" )
    else:
        formatString = GetLocalizedString("PLAYER_VICTORIOUS" )
    DisplayTimedTextFromPlayer(whichPlayer, 0, 0, 60, formatString)
    DialogSetMessage(d, GetLocalizedString("GAMEOVER_VICTORY_MSG" ))
    DialogAddButton(d, GetLocalizedString("GAMEOVER_CONTINUE_GAME" ), GetLocalizedHotkey("GAMEOVER_CONTINUE_GAME"))
    t = CreateTrigger()
    TriggerRegisterDialogButtonEvent(t, DialogAddQuitButton(d, True, GetLocalizedString("GAMEOVER_QUIT_GAME" ), GetLocalizedHotkey("GAMEOVER_QUIT_GAME")))
    DialogDisplay(whichPlayer, d, True)
    StartSoundForPlayerBJ(whichPlayer, bj_victoryDialogSound)
    pass

def MeleeDefeatDialogBJ(whichPlayer:"player", leftGame:"boolean")->"nothing":
    t = CreateTrigger()
    d = DialogCreate()
    formatString = None
    if ( leftGame ):
        formatString = GetLocalizedString("PLAYER_LEFT_GAME" )
    else:
        formatString = GetLocalizedString("PLAYER_DEFEATED" )
    DisplayTimedTextFromPlayer(whichPlayer, 0, 0, 60, formatString)
    DialogSetMessage(d, GetLocalizedString("GAMEOVER_DEFEAT_MSG" ))
    if ( not  bj_meleeGameOver and IsMapFlagSet(MAP_OBSERVERS_ON_DEATH) ):
        DialogAddButton(d, GetLocalizedString("GAMEOVER_CONTINUE_OBSERVING" ), GetLocalizedHotkey("GAMEOVER_CONTINUE_OBSERVING"))
    t = CreateTrigger()
    TriggerRegisterDialogButtonEvent(t, DialogAddQuitButton(d, True, GetLocalizedString("GAMEOVER_QUIT_GAME" ), GetLocalizedHotkey("GAMEOVER_QUIT_GAME")))
    DialogDisplay(whichPlayer, d, True)
    StartSoundForPlayerBJ(whichPlayer, bj_defeatDialogSound)
    pass

def GameOverDialogBJ(whichPlayer:"player", leftGame:"boolean")->"nothing":
    t = CreateTrigger()
    d = DialogCreate()
    s = None
    DisplayTimedTextFromPlayer(whichPlayer, 0, 0, 60, GetLocalizedString("PLAYER_LEFT_GAME" ))
    if ( GetIntegerGameState(GAME_STATE_DISCONNECTED) != 0 ):
        s = GetLocalizedString("GAMEOVER_DISCONNECTED" )
    else:
        s = GetLocalizedString("GAMEOVER_GAME_OVER" )
    DialogSetMessage(d, s)
    t = CreateTrigger()
    TriggerRegisterDialogButtonEvent(t, DialogAddQuitButton(d, True, GetLocalizedString("GAMEOVER_OK" ), GetLocalizedHotkey("GAMEOVER_OK")))
    DialogDisplay(whichPlayer, d, True)
    StartSoundForPlayerBJ(whichPlayer, bj_defeatDialogSound)
    pass

def RemovePlayerPreserveUnitsBJ(whichPlayer:"player", gameResult:"playergameresult", leftGame:"boolean")->"nothing":
    if AllowVictoryDefeat(gameResult):
        RemovePlayer(whichPlayer, gameResult)
        if ( gameResult == PLAYER_GAME_RESULT_VICTORY ):
            MeleeVictoryDialogBJ(whichPlayer, leftGame)
        elif ( gameResult == PLAYER_GAME_RESULT_DEFEAT ):
            MeleeDefeatDialogBJ(whichPlayer, leftGame)
        else:
            GameOverDialogBJ(whichPlayer, leftGame)
    pass

def CustomVictoryOkBJ()->"nothing":
    if bj_isSinglePlayer:
        PauseGame(False)
        SetGameDifficulty(GetDefaultDifficulty())
    if ( bj_changeLevelMapName == None ):
        EndGame(bj_changeLevelShowScores)
    else:
        ChangeLevel(bj_changeLevelMapName, bj_changeLevelShowScores)
    pass

def CustomVictoryQuitBJ()->"nothing":
    if bj_isSinglePlayer:
        PauseGame(False)
        SetGameDifficulty(GetDefaultDifficulty())
    EndGame(bj_changeLevelShowScores)
    pass

def CustomVictoryDialogBJ(whichPlayer:"player")->"nothing":
    t = CreateTrigger()
    d = DialogCreate()
    DialogSetMessage(d, GetLocalizedString("GAMEOVER_VICTORY_MSG" ))
    t = CreateTrigger()
    TriggerRegisterDialogButtonEvent(t, DialogAddButton(d, GetLocalizedString("GAMEOVER_CONTINUE" ), GetLocalizedHotkey("GAMEOVER_CONTINUE")))
    TriggerAddAction(t, CustomVictoryOkBJ)
    t = CreateTrigger()
    TriggerRegisterDialogButtonEvent(t, DialogAddButton(d, GetLocalizedString("GAMEOVER_QUIT_MISSION" ), GetLocalizedHotkey("GAMEOVER_QUIT_MISSION")))
    TriggerAddAction(t, CustomVictoryQuitBJ)
    if ( GetLocalPlayer() == whichPlayer ):
        EnableUserControl(True)
        if bj_isSinglePlayer:
            PauseGame(True)
        EnableUserUI(False)
    DialogDisplay(whichPlayer, d, True)
    VolumeGroupSetVolumeForPlayerBJ(whichPlayer, SOUND_VOLUMEGROUP_UI, 1.0)
    StartSoundForPlayerBJ(whichPlayer, bj_victoryDialogSound)
    pass

def CustomVictorySkipBJ(whichPlayer:"player")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        if bj_isSinglePlayer:
            SetGameDifficulty(GetDefaultDifficulty())
        if ( bj_changeLevelMapName == None ):
            EndGame(bj_changeLevelShowScores)
        else:
            ChangeLevel(bj_changeLevelMapName, bj_changeLevelShowScores)
    pass

def CustomVictoryBJ(whichPlayer:"player", showDialog:"boolean", showScores:"boolean")->"nothing":
    global bj_changeLevelShowScores
    if AllowVictoryDefeat(PLAYER_GAME_RESULT_VICTORY):
        RemovePlayer(whichPlayer, PLAYER_GAME_RESULT_VICTORY)
        if not  bj_isSinglePlayer:
            DisplayTimedTextFromPlayer(whichPlayer, 0, 0, 60, GetLocalizedString("PLAYER_VICTORIOUS" ))
        if ( GetPlayerController(whichPlayer) == MAP_CONTROL_USER ):
            bj_changeLevelShowScores = showScores
            if showDialog:
                CustomVictoryDialogBJ(whichPlayer)
            else:
                CustomVictorySkipBJ(whichPlayer)
    pass

def CustomDefeatRestartBJ()->"nothing":
    PauseGame(False)
    RestartGame(True)
    pass

def CustomDefeatReduceDifficultyBJ()->"nothing":
    diff = GetGameDifficulty()
    PauseGame(False)
    if ( diff == MAP_DIFFICULTY_EASY ):
        pass

    elif ( diff == MAP_DIFFICULTY_NORMAL ):
        SetGameDifficulty(MAP_DIFFICULTY_EASY)
    elif ( diff == MAP_DIFFICULTY_HARD ):
        SetGameDifficulty(MAP_DIFFICULTY_NORMAL)
    RestartGame(True)
    pass

def CustomDefeatLoadBJ()->"nothing":
    PauseGame(False)
    DisplayLoadDialog()
    pass

def CustomDefeatQuitBJ()->"nothing":
    if bj_isSinglePlayer:
        PauseGame(False)
    SetGameDifficulty(GetDefaultDifficulty())
    EndGame(True)
    pass

def CustomDefeatDialogBJ(whichPlayer:"player", message:"string")->"nothing":
    t = CreateTrigger()
    d = DialogCreate()
    DialogSetMessage(d, message)
    if bj_isSinglePlayer:
        t = CreateTrigger()
        TriggerRegisterDialogButtonEvent(t, DialogAddButton(d, GetLocalizedString("GAMEOVER_RESTART" ), GetLocalizedHotkey("GAMEOVER_RESTART")))
        TriggerAddAction(t, CustomDefeatRestartBJ)
        if ( GetGameDifficulty() != MAP_DIFFICULTY_EASY ):
            t = CreateTrigger()
            TriggerRegisterDialogButtonEvent(t, DialogAddButton(d, GetLocalizedString("GAMEOVER_REDUCE_DIFFICULTY" ), GetLocalizedHotkey("GAMEOVER_REDUCE_DIFFICULTY")))
            TriggerAddAction(t, CustomDefeatReduceDifficultyBJ)
        t = CreateTrigger()
        TriggerRegisterDialogButtonEvent(t, DialogAddButton(d, GetLocalizedString("GAMEOVER_LOAD" ), GetLocalizedHotkey("GAMEOVER_LOAD")))
        TriggerAddAction(t, CustomDefeatLoadBJ)
    t = CreateTrigger()
    TriggerRegisterDialogButtonEvent(t, DialogAddButton(d, GetLocalizedString("GAMEOVER_QUIT_MISSION" ), GetLocalizedHotkey("GAMEOVER_QUIT_MISSION")))
    TriggerAddAction(t, CustomDefeatQuitBJ)
    if ( GetLocalPlayer() == whichPlayer ):
        EnableUserControl(True)
        if bj_isSinglePlayer:
            PauseGame(True)
        EnableUserUI(False)
    DialogDisplay(whichPlayer, d, True)
    VolumeGroupSetVolumeForPlayerBJ(whichPlayer, SOUND_VOLUMEGROUP_UI, 1.0)
    StartSoundForPlayerBJ(whichPlayer, bj_defeatDialogSound)
    pass

def CustomDefeatBJ(whichPlayer:"player", message:"string")->"nothing":
    if AllowVictoryDefeat(PLAYER_GAME_RESULT_DEFEAT):
        RemovePlayer(whichPlayer, PLAYER_GAME_RESULT_DEFEAT)
        if not  bj_isSinglePlayer:
            DisplayTimedTextFromPlayer(whichPlayer, 0, 0, 60, GetLocalizedString("PLAYER_DEFEATED" ))
        if ( GetPlayerController(whichPlayer) == MAP_CONTROL_USER ):
            CustomDefeatDialogBJ(whichPlayer, message)
    pass

def SetNextLevelBJ(nextLevel:"string")->"nothing":
    global bj_changeLevelMapName
    if ( nextLevel == "" ):
        bj_changeLevelMapName = None
    else:
        bj_changeLevelMapName = nextLevel
    pass

def SetPlayerOnScoreScreenBJ(flag:"boolean", whichPlayer:"player")->"nothing":
    SetPlayerOnScoreScreen(whichPlayer, flag)
    pass

def CreateQuestBJ(questType:"integer", title:"string", description:"string", iconPath:"string")->"quest":
    global bj_lastCreatedQuest
    required = ( questType == bj_QUESTTYPE_REQ_DISCOVERED ) or ( questType == bj_QUESTTYPE_REQ_UNDISCOVERED )
    discovered = ( questType == bj_QUESTTYPE_REQ_DISCOVERED ) or ( questType == bj_QUESTTYPE_OPT_DISCOVERED )
    bj_lastCreatedQuest = CreateQuest()
    QuestSetTitle(bj_lastCreatedQuest, title)
    QuestSetDescription(bj_lastCreatedQuest, description)
    QuestSetIconPath(bj_lastCreatedQuest, iconPath)
    QuestSetRequired(bj_lastCreatedQuest, required)
    QuestSetDiscovered(bj_lastCreatedQuest, discovered)
    QuestSetCompleted(bj_lastCreatedQuest, False)
    return bj_lastCreatedQuest
    pass

def DestroyQuestBJ(whichQuest:"quest")->"nothing":
    DestroyQuest(whichQuest)
    pass

def QuestSetEnabledBJ(enabled:"boolean", whichQuest:"quest")->"nothing":
    QuestSetEnabled(whichQuest, enabled)
    pass

def QuestSetTitleBJ(whichQuest:"quest", title:"string")->"nothing":
    QuestSetTitle(whichQuest, title)
    pass

def QuestSetDescriptionBJ(whichQuest:"quest", description:"string")->"nothing":
    QuestSetDescription(whichQuest, description)
    pass

def QuestSetCompletedBJ(whichQuest:"quest", completed:"boolean")->"nothing":
    QuestSetCompleted(whichQuest, completed)
    pass

def QuestSetFailedBJ(whichQuest:"quest", failed:"boolean")->"nothing":
    QuestSetFailed(whichQuest, failed)
    pass

def QuestSetDiscoveredBJ(whichQuest:"quest", discovered:"boolean")->"nothing":
    QuestSetDiscovered(whichQuest, discovered)
    pass

def GetLastCreatedQuestBJ()->"quest":
    return bj_lastCreatedQuest
    pass

def CreateQuestItemBJ(whichQuest:"quest", description:"string")->"questitem":
    global bj_lastCreatedQuestItem
    bj_lastCreatedQuestItem = QuestCreateItem(whichQuest)
    QuestItemSetDescription(bj_lastCreatedQuestItem, description)
    QuestItemSetCompleted(bj_lastCreatedQuestItem, False)
    return bj_lastCreatedQuestItem
    pass

def QuestItemSetDescriptionBJ(whichQuestItem:"questitem", description:"string")->"nothing":
    QuestItemSetDescription(whichQuestItem, description)
    pass

def QuestItemSetCompletedBJ(whichQuestItem:"questitem", completed:"boolean")->"nothing":
    QuestItemSetCompleted(whichQuestItem, completed)
    pass

def GetLastCreatedQuestItemBJ()->"questitem":
    return bj_lastCreatedQuestItem
    pass

def CreateDefeatConditionBJ(description:"string")->"defeatcondition":
    global bj_lastCreatedDefeatCondition
    bj_lastCreatedDefeatCondition = CreateDefeatCondition()
    DefeatConditionSetDescription(bj_lastCreatedDefeatCondition, description)
    return bj_lastCreatedDefeatCondition
    pass

def DestroyDefeatConditionBJ(whichCondition:"defeatcondition")->"nothing":
    DestroyDefeatCondition(whichCondition)
    pass

def DefeatConditionSetDescriptionBJ(whichCondition:"defeatcondition", description:"string")->"nothing":
    DefeatConditionSetDescription(whichCondition, description)
    pass

def GetLastCreatedDefeatConditionBJ()->"defeatcondition":
    return bj_lastCreatedDefeatCondition
    pass

def FlashQuestDialogButtonBJ()->"nothing":
    FlashQuestDialogButton()
    pass

def QuestMessageBJ(f:"force", messageType:"integer", message:"string")->"nothing":
    if ( IsPlayerInForce(GetLocalPlayer(), f) ):
        if ( messageType == bj_QUESTMESSAGE_DISCOVERED ):
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_QUEST, " ")
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_QUEST, message)
            StartSound(bj_questDiscoveredSound)
            FlashQuestDialogButton()
        elif ( messageType == bj_QUESTMESSAGE_UPDATED ):
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_QUESTUPDATE, " ")
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_QUESTUPDATE, message)
            StartSound(bj_questUpdatedSound)
            FlashQuestDialogButton()
        elif ( messageType == bj_QUESTMESSAGE_COMPLETED ):
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_QUESTDONE, " ")
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_QUESTDONE, message)
            StartSound(bj_questCompletedSound)
            FlashQuestDialogButton()
        elif ( messageType == bj_QUESTMESSAGE_FAILED ):
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_QUESTFAILED, " ")
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_QUESTFAILED, message)
            StartSound(bj_questFailedSound)
            FlashQuestDialogButton()
        elif ( messageType == bj_QUESTMESSAGE_REQUIREMENT ):
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_QUESTREQUIREMENT, message)
        elif ( messageType == bj_QUESTMESSAGE_MISSIONFAILED ):
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_MISSIONFAILED, " ")
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_MISSIONFAILED, message)
            StartSound(bj_questFailedSound)
        elif ( messageType == bj_QUESTMESSAGE_HINT ):
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_HINT, " ")
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_HINT, message)
            StartSound(bj_questHintSound)
        elif ( messageType == bj_QUESTMESSAGE_ALWAYSHINT ):
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_ALWAYSHINT, " ")
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_ALWAYSHINT, message)
            StartSound(bj_questHintSound)
        elif ( messageType == bj_QUESTMESSAGE_SECRET ):
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_SECRET, " ")
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_SECRET, message)
            StartSound(bj_questSecretSound)
        elif ( messageType == bj_QUESTMESSAGE_UNITACQUIRED ):
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_UNITACQUIRED, " ")
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_UNITACQUIRED, message)
            StartSound(bj_questHintSound)
        elif ( messageType == bj_QUESTMESSAGE_UNITAVAILABLE ):
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_UNITAVAILABLE, " ")
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_UNITAVAILABLE, message)
            StartSound(bj_questHintSound)
        elif ( messageType == bj_QUESTMESSAGE_ITEMACQUIRED ):
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_ITEMACQUIRED, " ")
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_ITEMACQUIRED, message)
            StartSound(bj_questItemAcquiredSound)
        elif ( messageType == bj_QUESTMESSAGE_WARNING ):
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_WARNING, " ")
            DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_TEXT_DELAY_WARNING, message)
            StartSound(bj_questWarningSound)
    pass

def StartTimerBJ(t:"timer", periodic:"boolean", timeout:"real")->"timer":
    global bj_lastStartedTimer
    bj_lastStartedTimer = t
    TimerStart(t, timeout, periodic, None)
    return bj_lastStartedTimer
    pass

def CreateTimerBJ(periodic:"boolean", timeout:"real")->"timer":
    global bj_lastStartedTimer
    bj_lastStartedTimer = CreateTimer()
    TimerStart(bj_lastStartedTimer, timeout, periodic, None)
    return bj_lastStartedTimer
    pass

def DestroyTimerBJ(whichTimer:"timer")->"nothing":
    DestroyTimer(whichTimer)
    pass

def PauseTimerBJ(pause:"boolean", whichTimer:"timer")->"nothing":
    if pause:
        PauseTimer(whichTimer)
    else:
        ResumeTimer(whichTimer)
    pass

def GetLastCreatedTimerBJ()->"timer":
    return bj_lastStartedTimer
    pass

def CreateTimerDialogBJ(t:"timer", title:"string")->"timerdialog":
    global bj_lastCreatedTimerDialog
    bj_lastCreatedTimerDialog = CreateTimerDialog(t)
    TimerDialogSetTitle(bj_lastCreatedTimerDialog, title)
    TimerDialogDisplay(bj_lastCreatedTimerDialog, True)
    return bj_lastCreatedTimerDialog
    pass

def DestroyTimerDialogBJ(td:"timerdialog")->"nothing":
    DestroyTimerDialog(td)
    pass

def TimerDialogSetTitleBJ(td:"timerdialog", title:"string")->"nothing":
    TimerDialogSetTitle(td, title)
    pass

def TimerDialogSetTitleColorBJ(td:"timerdialog", red:"real", green:"real", blue:"real", transparency:"real")->"nothing":
    TimerDialogSetTitleColor(td, PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - transparency))
    pass

def TimerDialogSetTimeColorBJ(td:"timerdialog", red:"real", green:"real", blue:"real", transparency:"real")->"nothing":
    TimerDialogSetTimeColor(td, PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - transparency))
    pass

def TimerDialogSetSpeedBJ(td:"timerdialog", speedMultFactor:"real")->"nothing":
    TimerDialogSetSpeed(td, speedMultFactor)
    pass

def TimerDialogDisplayForPlayerBJ(show:"boolean", td:"timerdialog", whichPlayer:"player")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        TimerDialogDisplay(td, show)
    pass

def TimerDialogDisplayBJ(show:"boolean", td:"timerdialog")->"nothing":
    TimerDialogDisplay(td, show)
    pass

def GetLastCreatedTimerDialogBJ()->"timerdialog":
    return bj_lastCreatedTimerDialog
    pass

def LeaderboardResizeBJ(lb:"leaderboard")->"nothing":
    size = LeaderboardGetItemCount(lb)
    if ( LeaderboardGetLabelText(lb) == "" ):
        size = size - 1
    LeaderboardSetSizeByItemCount(lb, size)
    pass

def LeaderboardSetPlayerItemValueBJ(whichPlayer:"player", lb:"leaderboard", val:"integer")->"nothing":
    LeaderboardSetItemValue(lb, LeaderboardGetPlayerIndex(lb, whichPlayer), val)
    pass

def LeaderboardSetPlayerItemLabelBJ(whichPlayer:"player", lb:"leaderboard", val:"string")->"nothing":
    LeaderboardSetItemLabel(lb, LeaderboardGetPlayerIndex(lb, whichPlayer), val)
    pass

def LeaderboardSetPlayerItemStyleBJ(whichPlayer:"player", lb:"leaderboard", showLabel:"boolean", showValue:"boolean", showIcon:"boolean")->"nothing":
    LeaderboardSetItemStyle(lb, LeaderboardGetPlayerIndex(lb, whichPlayer), showLabel, showValue, showIcon)
    pass

def LeaderboardSetPlayerItemLabelColorBJ(whichPlayer:"player", lb:"leaderboard", red:"real", green:"real", blue:"real", transparency:"real")->"nothing":
    LeaderboardSetItemLabelColor(lb, LeaderboardGetPlayerIndex(lb, whichPlayer), PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - transparency))
    pass

def LeaderboardSetPlayerItemValueColorBJ(whichPlayer:"player", lb:"leaderboard", red:"real", green:"real", blue:"real", transparency:"real")->"nothing":
    LeaderboardSetItemValueColor(lb, LeaderboardGetPlayerIndex(lb, whichPlayer), PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - transparency))
    pass

def LeaderboardSetLabelColorBJ(lb:"leaderboard", red:"real", green:"real", blue:"real", transparency:"real")->"nothing":
    LeaderboardSetLabelColor(lb, PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - transparency))
    pass

def LeaderboardSetValueColorBJ(lb:"leaderboard", red:"real", green:"real", blue:"real", transparency:"real")->"nothing":
    LeaderboardSetValueColor(lb, PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - transparency))
    pass

def LeaderboardSetLabelBJ(lb:"leaderboard", label:"string")->"nothing":
    LeaderboardSetLabel(lb, label)
    LeaderboardResizeBJ(lb)
    pass

def LeaderboardSetStyleBJ(lb:"leaderboard", showLabel:"boolean", showNames:"boolean", showValues:"boolean", showIcons:"boolean")->"nothing":
    LeaderboardSetStyle(lb, showLabel, showNames, showValues, showIcons)
    pass

def LeaderboardGetItemCountBJ(lb:"leaderboard")->"integer":
    return LeaderboardGetItemCount(lb)
    pass

def LeaderboardHasPlayerItemBJ(lb:"leaderboard", whichPlayer:"player")->"boolean":
    return LeaderboardHasPlayerItem(lb, whichPlayer)
    pass

def ForceSetLeaderboardBJ(lb:"leaderboard", toForce:"force")->"nothing":
    index = None
    indexPlayer = None
    index = 0
    while True:
        indexPlayer = Player(index)
        if IsPlayerInForce(indexPlayer, toForce):
            PlayerSetLeaderboard(indexPlayer, lb)
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    pass

def CreateLeaderboardBJ(toForce:"force", label:"string")->"leaderboard":
    global bj_lastCreatedLeaderboard
    bj_lastCreatedLeaderboard = CreateLeaderboard()
    LeaderboardSetLabel(bj_lastCreatedLeaderboard, label)
    ForceSetLeaderboardBJ(bj_lastCreatedLeaderboard, toForce)
    LeaderboardDisplay(bj_lastCreatedLeaderboard, True)
    return bj_lastCreatedLeaderboard
    pass

def DestroyLeaderboardBJ(lb:"leaderboard")->"nothing":
    DestroyLeaderboard(lb)
    pass

def LeaderboardDisplayBJ(show:"boolean", lb:"leaderboard")->"nothing":
    LeaderboardDisplay(lb, show)
    pass

def LeaderboardAddItemBJ(whichPlayer:"player", lb:"leaderboard", label:"string", value:"integer")->"nothing":
    if ( LeaderboardHasPlayerItem(lb, whichPlayer) ):
        LeaderboardRemovePlayerItem(lb, whichPlayer)
    LeaderboardAddItem(lb, label, value, whichPlayer)
    LeaderboardResizeBJ(lb)
    pass

def LeaderboardRemovePlayerItemBJ(whichPlayer:"player", lb:"leaderboard")->"nothing":
    LeaderboardRemovePlayerItem(lb, whichPlayer)
    LeaderboardResizeBJ(lb)
    pass

def LeaderboardSortItemsBJ(lb:"leaderboard", sortType:"integer", ascending:"boolean")->"nothing":
    if ( sortType == bj_SORTTYPE_SORTBYVALUE ):
        LeaderboardSortItemsByValue(lb, ascending)
    elif ( sortType == bj_SORTTYPE_SORTBYPLAYER ):
        LeaderboardSortItemsByPlayer(lb, ascending)
    elif ( sortType == bj_SORTTYPE_SORTBYLABEL ):
        LeaderboardSortItemsByLabel(lb, ascending)
    pass

def LeaderboardSortItemsByPlayerBJ(lb:"leaderboard", ascending:"boolean")->"nothing":
    LeaderboardSortItemsByPlayer(lb, ascending)
    pass

def LeaderboardSortItemsByLabelBJ(lb:"leaderboard", ascending:"boolean")->"nothing":
    LeaderboardSortItemsByLabel(lb, ascending)
    pass

def LeaderboardGetPlayerIndexBJ(whichPlayer:"player", lb:"leaderboard")->"integer":
    return LeaderboardGetPlayerIndex(lb, whichPlayer) + 1
    pass

def LeaderboardGetIndexedPlayerBJ(position:"integer", lb:"leaderboard")->"player":
    index = None
    indexPlayer = None
    index = 0
    while True:
        indexPlayer = Player(index)
        if ( LeaderboardGetPlayerIndex(lb, indexPlayer) == position - 1 ):
            return indexPlayer
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    return Player(PLAYER_NEUTRAL_PASSIVE)
    pass

def PlayerGetLeaderboardBJ(whichPlayer:"player")->"leaderboard":
    return PlayerGetLeaderboard(whichPlayer)
    pass

def GetLastCreatedLeaderboard()->"leaderboard":
    return bj_lastCreatedLeaderboard
    pass

def CreateMultiboardBJ(cols:"integer", rows:"integer", title:"string")->"multiboard":
    global bj_lastCreatedMultiboard
    bj_lastCreatedMultiboard = CreateMultiboard()
    MultiboardSetRowCount(bj_lastCreatedMultiboard, rows)
    MultiboardSetColumnCount(bj_lastCreatedMultiboard, cols)
    MultiboardSetTitleText(bj_lastCreatedMultiboard, title)
    MultiboardDisplay(bj_lastCreatedMultiboard, True)
    return bj_lastCreatedMultiboard
    pass

def DestroyMultiboardBJ(mb:"multiboard")->"nothing":
    DestroyMultiboard(mb)
    pass

def GetLastCreatedMultiboard()->"multiboard":
    return bj_lastCreatedMultiboard
    pass

def MultiboardDisplayBJ(show:"boolean", mb:"multiboard")->"nothing":
    MultiboardDisplay(mb, show)
    pass

def MultiboardMinimizeBJ(minimize:"boolean", mb:"multiboard")->"nothing":
    MultiboardMinimize(mb, minimize)
    pass

def MultiboardSetTitleTextColorBJ(mb:"multiboard", red:"real", green:"real", blue:"real", transparency:"real")->"nothing":
    MultiboardSetTitleTextColor(mb, PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - transparency))
    pass

def MultiboardAllowDisplayBJ(flag:"boolean")->"nothing":
    MultiboardSuppressDisplay(not  flag)
    pass

def MultiboardSetItemStyleBJ(mb:"multiboard", col:"integer", row:"integer", showValue:"boolean", showIcon:"boolean")->"nothing":
    curRow = 0
    curCol = 0
    numRows = MultiboardGetRowCount(mb)
    numCols = MultiboardGetColumnCount(mb)
    mbitem = None
    while True:
        curRow = curRow + 1
        if curRow > numRows:
            break
        if ( row == 0 or row == curRow ):
            curCol = 0
            while True:
                curCol = curCol + 1
                if curCol > numCols:
                    break
                if ( col == 0 or col == curCol ):
                    mbitem = MultiboardGetItem(mb, curRow - 1, curCol - 1)
                    MultiboardSetItemStyle(mbitem, showValue, showIcon)
                    MultiboardReleaseItem(mbitem)
                pass

        pass

    pass

def MultiboardSetItemValueBJ(mb:"multiboard", col:"integer", row:"integer", val:"string")->"nothing":
    curRow = 0
    curCol = 0
    numRows = MultiboardGetRowCount(mb)
    numCols = MultiboardGetColumnCount(mb)
    mbitem = None
    while True:
        curRow = curRow + 1
        if curRow > numRows:
            break
        if ( row == 0 or row == curRow ):
            curCol = 0
            while True:
                curCol = curCol + 1
                if curCol > numCols:
                    break
                if ( col == 0 or col == curCol ):
                    mbitem = MultiboardGetItem(mb, curRow - 1, curCol - 1)
                    MultiboardSetItemValue(mbitem, val)
                    MultiboardReleaseItem(mbitem)
                pass

        pass

    pass

def MultiboardSetItemColorBJ(mb:"multiboard", col:"integer", row:"integer", red:"real", green:"real", blue:"real", transparency:"real")->"nothing":
    curRow = 0
    curCol = 0
    numRows = MultiboardGetRowCount(mb)
    numCols = MultiboardGetColumnCount(mb)
    mbitem = None
    while True:
        curRow = curRow + 1
        if curRow > numRows:
            break
        if ( row == 0 or row == curRow ):
            curCol = 0
            while True:
                curCol = curCol + 1
                if curCol > numCols:
                    break
                if ( col == 0 or col == curCol ):
                    mbitem = MultiboardGetItem(mb, curRow - 1, curCol - 1)
                    MultiboardSetItemValueColor(mbitem, PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - transparency))
                    MultiboardReleaseItem(mbitem)
                pass

        pass

    pass

def MultiboardSetItemWidthBJ(mb:"multiboard", col:"integer", row:"integer", width:"real")->"nothing":
    curRow = 0
    curCol = 0
    numRows = MultiboardGetRowCount(mb)
    numCols = MultiboardGetColumnCount(mb)
    mbitem = None
    while True:
        curRow = curRow + 1
        if curRow > numRows:
            break
        if ( row == 0 or row == curRow ):
            curCol = 0
            while True:
                curCol = curCol + 1
                if curCol > numCols:
                    break
                if ( col == 0 or col == curCol ):
                    mbitem = MultiboardGetItem(mb, curRow - 1, curCol - 1)
                    MultiboardSetItemWidth(mbitem, width / 100.0)
                    MultiboardReleaseItem(mbitem)
                pass

        pass

    pass

def MultiboardSetItemIconBJ(mb:"multiboard", col:"integer", row:"integer", iconFileName:"string")->"nothing":
    curRow = 0
    curCol = 0
    numRows = MultiboardGetRowCount(mb)
    numCols = MultiboardGetColumnCount(mb)
    mbitem = None
    while True:
        curRow = curRow + 1
        if curRow > numRows:
            break
        if ( row == 0 or row == curRow ):
            curCol = 0
            while True:
                curCol = curCol + 1
                if curCol > numCols:
                    break
                if ( col == 0 or col == curCol ):
                    mbitem = MultiboardGetItem(mb, curRow - 1, curCol - 1)
                    MultiboardSetItemIcon(mbitem, iconFileName)
                    MultiboardReleaseItem(mbitem)
                pass

        pass

    pass

def TextTagSize2Height(size:"real")->"real":
    return size * 0.023 / 10
    pass

def TextTagSpeed2Velocity(speed:"real")->"real":
    return speed * 0.071 / 128
    pass

def SetTextTagColorBJ(tt:"texttag", red:"real", green:"real", blue:"real", transparency:"real")->"nothing":
    SetTextTagColor(tt, PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100.0 - transparency))
    pass

def SetTextTagVelocityBJ(tt:"texttag", speed:"real", angle:"real")->"nothing":
    vel = TextTagSpeed2Velocity(speed)
    xvel = vel * Cos(angle * bj_DEGTORAD)
    yvel = vel * Sin(angle * bj_DEGTORAD)
    SetTextTagVelocity(tt, xvel, yvel)
    pass

def SetTextTagTextBJ(tt:"texttag", s:"string", size:"real")->"nothing":
    textHeight = TextTagSize2Height(size)
    SetTextTagText(tt, s, textHeight)
    pass

def SetTextTagPosBJ(tt:"texttag", loc:"location", zOffset:"real")->"nothing":
    SetTextTagPos(tt, GetLocationX(loc), GetLocationY(loc), zOffset)
    pass

def SetTextTagPosUnitBJ(tt:"texttag", whichUnit:"unit", zOffset:"real")->"nothing":
    SetTextTagPosUnit(tt, whichUnit, zOffset)
    pass

def SetTextTagSuspendedBJ(tt:"texttag", flag:"boolean")->"nothing":
    SetTextTagSuspended(tt, flag)
    pass

def SetTextTagPermanentBJ(tt:"texttag", flag:"boolean")->"nothing":
    SetTextTagPermanent(tt, flag)
    pass

def SetTextTagAgeBJ(tt:"texttag", age:"real")->"nothing":
    SetTextTagAge(tt, age)
    pass

def SetTextTagLifespanBJ(tt:"texttag", lifespan:"real")->"nothing":
    SetTextTagLifespan(tt, lifespan)
    pass

def SetTextTagFadepointBJ(tt:"texttag", fadepoint:"real")->"nothing":
    SetTextTagFadepoint(tt, fadepoint)
    pass

def CreateTextTagLocBJ(s:"string", loc:"location", zOffset:"real", size:"real", red:"real", green:"real", blue:"real", transparency:"real")->"texttag":
    global bj_lastCreatedTextTag
    bj_lastCreatedTextTag = CreateTextTag()
    SetTextTagTextBJ(bj_lastCreatedTextTag, s, size)
    SetTextTagPosBJ(bj_lastCreatedTextTag, loc, zOffset)
    SetTextTagColorBJ(bj_lastCreatedTextTag, red, green, blue, transparency)
    return bj_lastCreatedTextTag
    pass

def CreateTextTagUnitBJ(s:"string", whichUnit:"unit", zOffset:"real", size:"real", red:"real", green:"real", blue:"real", transparency:"real")->"texttag":
    global bj_lastCreatedTextTag
    bj_lastCreatedTextTag = CreateTextTag()
    SetTextTagTextBJ(bj_lastCreatedTextTag, s, size)
    SetTextTagPosUnitBJ(bj_lastCreatedTextTag, whichUnit, zOffset)
    SetTextTagColorBJ(bj_lastCreatedTextTag, red, green, blue, transparency)
    return bj_lastCreatedTextTag
    pass

def DestroyTextTagBJ(tt:"texttag")->"nothing":
    DestroyTextTag(tt)
    pass

def ShowTextTagForceBJ(show:"boolean", tt:"texttag", whichForce:"force")->"nothing":
    if ( IsPlayerInForce(GetLocalPlayer(), whichForce) ):
        SetTextTagVisibility(tt, show)
    pass

def GetLastCreatedTextTag()->"texttag":
    return bj_lastCreatedTextTag
    pass

def PauseGameOn()->"nothing":
    PauseGame(True)
    pass

def PauseGameOff()->"nothing":
    PauseGame(False)
    pass

def SetUserControlForceOn(whichForce:"force")->"nothing":
    if ( IsPlayerInForce(GetLocalPlayer(), whichForce) ):
        EnableUserControl(True)
    pass

def SetUserControlForceOff(whichForce:"force")->"nothing":
    if ( IsPlayerInForce(GetLocalPlayer(), whichForce) ):
        EnableUserControl(False)
    pass

def ShowInterfaceForceOn(whichForce:"force", fadeDuration:"real")->"nothing":
    if ( IsPlayerInForce(GetLocalPlayer(), whichForce) ):
        ShowInterface(True, fadeDuration)
    pass

def ShowInterfaceForceOff(whichForce:"force", fadeDuration:"real")->"nothing":
    if ( IsPlayerInForce(GetLocalPlayer(), whichForce) ):
        ShowInterface(False, fadeDuration)
    pass

def PingMinimapForForce(whichForce:"force", x:"real", y:"real", duration:"real")->"nothing":
    if ( IsPlayerInForce(GetLocalPlayer(), whichForce) ):
        PingMinimap(x, y, duration)
    pass

def PingMinimapLocForForce(whichForce:"force", loc:"location", duration:"real")->"nothing":
    PingMinimapForForce(whichForce, GetLocationX(loc), GetLocationY(loc), duration)
    pass

def PingMinimapForPlayer(whichPlayer:"player", x:"real", y:"real", duration:"real")->"nothing":
    if ( GetLocalPlayer() == whichPlayer ):
        PingMinimap(x, y, duration)
    pass

def PingMinimapLocForPlayer(whichPlayer:"player", loc:"location", duration:"real")->"nothing":
    PingMinimapForPlayer(whichPlayer, GetLocationX(loc), GetLocationY(loc), duration)
    pass

def PingMinimapForForceEx(whichForce:"force", x:"real", y:"real", duration:"real", style:"integer", red:"real", green:"real", blue:"real")->"nothing":
    red255 = PercentTo255(red)
    green255 = PercentTo255(green)
    blue255 = PercentTo255(blue)
    if ( IsPlayerInForce(GetLocalPlayer(), whichForce) ):
        if ( red255 == 255 ) and ( green255 == 0 ) and ( blue255 == 0 ):
            red255 = 254
        if ( style == bj_MINIMAPPINGSTYLE_SIMPLE ):
            PingMinimapEx(x, y, duration, red255, green255, blue255, False)
        elif ( style == bj_MINIMAPPINGSTYLE_FLASHY ):
            PingMinimapEx(x, y, duration, red255, green255, blue255, True)
        elif ( style == bj_MINIMAPPINGSTYLE_ATTACK ):
            PingMinimapEx(x, y, duration, 255, 0, 0, False)
    pass

def PingMinimapLocForForceEx(whichForce:"force", loc:"location", duration:"real", style:"integer", red:"real", green:"real", blue:"real")->"nothing":
    PingMinimapForForceEx(whichForce, GetLocationX(loc), GetLocationY(loc), duration, style, red, green, blue)
    pass

def EnableWorldFogBoundaryBJ(enable:"boolean", f:"force")->"nothing":
    if ( IsPlayerInForce(GetLocalPlayer(), f) ):
        EnableWorldFogBoundary(enable)
    pass

def EnableOcclusionBJ(enable:"boolean", f:"force")->"nothing":
    if ( IsPlayerInForce(GetLocalPlayer(), f) ):
        EnableOcclusion(enable)
    pass

def CancelCineSceneBJ()->"nothing":
    StopSoundBJ(bj_cineSceneLastSound, True)
    EndCinematicScene()
    pass

def TryInitCinematicBehaviorBJ()->"nothing":
    global bj_cineSceneBeingSkipped
    index = None
    if ( bj_cineSceneBeingSkipped == None ):
        bj_cineSceneBeingSkipped = CreateTrigger()
        index = 0
        while True:
            TriggerRegisterPlayerEvent(bj_cineSceneBeingSkipped, Player(index), EVENT_PLAYER_END_CINEMATIC)
            index = index + 1
            if index == bj_MAX_PLAYERS:
                break
            pass

        TriggerAddAction(bj_cineSceneBeingSkipped, CancelCineSceneBJ)
    pass

def SetCinematicSceneBJ(soundHandle:"sound", portraitUnitId:"integer", color:"playercolor", speakerTitle:"string", text:"string", sceneDuration:"real", voiceoverDuration:"real")->"nothing":
    global bj_cineSceneLastSound
    bj_cineSceneLastSound = soundHandle
    PlaySoundBJ(soundHandle)
    SetCinematicScene(portraitUnitId, color, speakerTitle, text, sceneDuration, voiceoverDuration)
    pass

def GetTransmissionDuration(soundHandle:"sound", timeType:"integer", timeVal:"real")->"real":
    duration = None
    if ( timeType == bj_TIMETYPE_ADD ):
        duration = GetSoundDurationBJ(soundHandle) + timeVal
    elif ( timeType == bj_TIMETYPE_SET ):
        duration = timeVal
    elif ( timeType == bj_TIMETYPE_SUB ):
        duration = GetSoundDurationBJ(soundHandle) - timeVal
    else:
        duration = GetSoundDurationBJ(soundHandle)
    if ( duration < 0 ):
        duration = 0
    return duration
    pass

def WaitTransmissionDuration(soundHandle:"sound", timeType:"integer", timeVal:"real")->"nothing":
    if ( timeType == bj_TIMETYPE_SET ):
        TriggerSleepAction(timeVal)
    elif ( soundHandle == None ):
        TriggerSleepAction(bj_NOTHING_SOUND_DURATION)
    elif ( timeType == bj_TIMETYPE_SUB ):
        WaitForSoundBJ(soundHandle, timeVal)
    elif ( timeType == bj_TIMETYPE_ADD ):
        WaitForSoundBJ(soundHandle, 0)
        TriggerSleepAction(timeVal)
    pass

def DoTransmissionBasicsXYBJ(unitId:"integer", color:"playercolor", x:"real", y:"real", soundHandle:"sound", unitName:"string", message:"string", duration:"real")->"nothing":
    SetCinematicSceneBJ(soundHandle, unitId, color, unitName, message, duration + bj_TRANSMISSION_PORT_HANGTIME, duration)
    if ( unitId != 0 ):
        PingMinimap(x, y, bj_TRANSMISSION_PING_TIME)
    pass

def TransmissionFromUnitWithNameBJ(toForce:"force", whichUnit:"unit", unitName:"string", soundHandle:"sound", message:"string", timeType:"integer", timeVal:"real", wait:"boolean")->"nothing":
    global bj_lastTransmissionDuration
    global bj_lastPlayedSound
    TryInitCinematicBehaviorBJ()
    timeVal = RMaxBJ(timeVal, 0)
    bj_lastTransmissionDuration = GetTransmissionDuration(soundHandle, timeType, timeVal)
    bj_lastPlayedSound = soundHandle
    if ( IsPlayerInForce(GetLocalPlayer(), toForce) ):
        if ( whichUnit == None ):
            DoTransmissionBasicsXYBJ(0, PLAYER_COLOR_RED, 0, 0, soundHandle, unitName, message, bj_lastTransmissionDuration)
        else:
            DoTransmissionBasicsXYBJ(GetUnitTypeId(whichUnit), GetPlayerColor(GetOwningPlayer(whichUnit)), GetUnitX(whichUnit), GetUnitY(whichUnit), soundHandle, unitName, message, bj_lastTransmissionDuration)
            if ( not  IsUnitHidden(whichUnit) ):
                UnitAddIndicator(whichUnit, bj_TRANSMISSION_IND_RED, bj_TRANSMISSION_IND_BLUE, bj_TRANSMISSION_IND_GREEN, bj_TRANSMISSION_IND_ALPHA)
    if wait and ( bj_lastTransmissionDuration > 0 ):
        WaitTransmissionDuration(soundHandle, timeType, timeVal)
    pass

def TransmissionFromUnitTypeWithNameBJ(toForce:"force", fromPlayer:"player", unitId:"integer", unitName:"string", loc:"location", soundHandle:"sound", message:"string", timeType:"integer", timeVal:"real", wait:"boolean")->"nothing":
    global bj_lastTransmissionDuration
    global bj_lastPlayedSound
    TryInitCinematicBehaviorBJ()
    timeVal = RMaxBJ(timeVal, 0)
    bj_lastTransmissionDuration = GetTransmissionDuration(soundHandle, timeType, timeVal)
    bj_lastPlayedSound = soundHandle
    if ( IsPlayerInForce(GetLocalPlayer(), toForce) ):
        DoTransmissionBasicsXYBJ(unitId, GetPlayerColor(fromPlayer), GetLocationX(loc), GetLocationY(loc), soundHandle, unitName, message, bj_lastTransmissionDuration)
    if wait and ( bj_lastTransmissionDuration > 0 ):
        WaitTransmissionDuration(soundHandle, timeType, timeVal)
    pass

def GetLastTransmissionDurationBJ()->"real":
    return bj_lastTransmissionDuration
    pass

def ForceCinematicSubtitlesBJ(flag:"boolean")->"nothing":
    ForceCinematicSubtitles(flag)
    pass

def CinematicModeExBJ(cineMode:"boolean", forForce:"force", interfaceFadeTime:"real")->"nothing":
    global bj_cineModePriorMaskSetting
    global bj_cineModePriorSpeed
    global bj_cineModePriorFogSetting
    global bj_cineModeSavedSeed
    global bj_cineModePriorDawnDusk
    global bj_cineModeAlreadyIn
    if ( not  bj_gameStarted ):
        interfaceFadeTime = 0
    if ( cineMode ):
        if ( not  bj_cineModeAlreadyIn ):
            bj_cineModeAlreadyIn = True
            bj_cineModePriorSpeed = GetGameSpeed()
            bj_cineModePriorFogSetting = IsFogEnabled()
            bj_cineModePriorMaskSetting = IsFogMaskEnabled()
            bj_cineModePriorDawnDusk = IsDawnDuskEnabled()
            bj_cineModeSavedSeed = GetRandomInt(0, 1000000)
        if ( IsPlayerInForce(GetLocalPlayer(), forForce) ):
            ClearTextMessages()
            ShowInterface(False, interfaceFadeTime)
            EnableUserControl(False)
            EnableOcclusion(False)
            SetCineModeVolumeGroupsBJ()
        SetGameSpeed(bj_CINEMODE_GAMESPEED)
        SetMapFlag(MAP_LOCK_SPEED, True)
        FogMaskEnable(False)
        FogEnable(False)
        EnableWorldFogBoundary(False)
        EnableDawnDusk(False)
        SetRandomSeed(0)
    else:
        bj_cineModeAlreadyIn = False
        if ( IsPlayerInForce(GetLocalPlayer(), forForce) ):
            ShowInterface(True, interfaceFadeTime)
            EnableUserControl(True)
            EnableOcclusion(True)
            VolumeGroupReset()
            EndThematicMusic()
            CameraResetSmoothingFactorBJ()
        SetMapFlag(MAP_LOCK_SPEED, False)
        SetGameSpeed(bj_cineModePriorSpeed)
        FogMaskEnable(bj_cineModePriorMaskSetting)
        FogEnable(bj_cineModePriorFogSetting)
        EnableWorldFogBoundary(True)
        EnableDawnDusk(bj_cineModePriorDawnDusk)
        SetRandomSeed(bj_cineModeSavedSeed)
    pass

def CinematicModeBJ(cineMode:"boolean", forForce:"force")->"nothing":
    CinematicModeExBJ(cineMode, forForce, bj_CINEMODE_INTERFACEFADE)
    pass

def DisplayCineFilterBJ(flag:"boolean")->"nothing":
    DisplayCineFilter(flag)
    pass

def CinematicFadeCommonBJ(red:"real", green:"real", blue:"real", duration:"real", tex:"string", startTrans:"real", endTrans:"real")->"nothing":
    if ( duration == 0 ):
        startTrans = endTrans
    EnableUserUI(False)
    SetCineFilterTexture(tex)
    SetCineFilterBlendMode(BLEND_MODE_BLEND)
    SetCineFilterTexMapFlags(TEXMAP_FLAG_NONE)
    SetCineFilterStartUV(0, 0, 1, 1)
    SetCineFilterEndUV(0, 0, 1, 1)
    SetCineFilterStartColor(PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100 - startTrans))
    SetCineFilterEndColor(PercentTo255(red), PercentTo255(green), PercentTo255(blue), PercentTo255(100 - endTrans))
    SetCineFilterDuration(duration)
    DisplayCineFilter(True)
    pass

def FinishCinematicFadeBJ()->"nothing":
    global bj_cineFadeFinishTimer
    DestroyTimer(bj_cineFadeFinishTimer)
    bj_cineFadeFinishTimer = None
    DisplayCineFilter(False)
    EnableUserUI(True)
    pass

def FinishCinematicFadeAfterBJ(duration:"real")->"nothing":
    global bj_cineFadeFinishTimer
    bj_cineFadeFinishTimer = CreateTimer()
    TimerStart(bj_cineFadeFinishTimer, duration, False, FinishCinematicFadeBJ)
    pass

def ContinueCinematicFadeBJ()->"nothing":
    global bj_cineFadeContinueTimer
    DestroyTimer(bj_cineFadeContinueTimer)
    bj_cineFadeContinueTimer = None
    CinematicFadeCommonBJ(bj_cineFadeContinueRed, bj_cineFadeContinueGreen, bj_cineFadeContinueBlue, bj_cineFadeContinueDuration, bj_cineFadeContinueTex, bj_cineFadeContinueTrans, 100)
    pass

def ContinueCinematicFadeAfterBJ(duration:"real", red:"real", green:"real", blue:"real", trans:"real", tex:"string")->"nothing":
    global bj_cineFadeContinueTrans
    global bj_cineFadeContinueGreen
    global bj_cineFadeContinueTex
    global bj_cineFadeContinueBlue
    global bj_cineFadeContinueRed
    global bj_cineFadeContinueDuration
    global bj_cineFadeContinueTimer
    bj_cineFadeContinueRed = red
    bj_cineFadeContinueGreen = green
    bj_cineFadeContinueBlue = blue
    bj_cineFadeContinueTrans = trans
    bj_cineFadeContinueDuration = duration
    bj_cineFadeContinueTex = tex
    bj_cineFadeContinueTimer = CreateTimer()
    TimerStart(bj_cineFadeContinueTimer, duration, False, ContinueCinematicFadeBJ)
    pass

def AbortCinematicFadeBJ()->"nothing":
    if ( bj_cineFadeContinueTimer != None ):
        DestroyTimer(bj_cineFadeContinueTimer)
    if ( bj_cineFadeFinishTimer != None ):
        DestroyTimer(bj_cineFadeFinishTimer)
    pass

def CinematicFadeBJ(fadetype:"integer", duration:"real", tex:"string", red:"real", green:"real", blue:"real", trans:"real")->"nothing":
    if ( fadetype == bj_CINEFADETYPE_FADEOUT ):
        AbortCinematicFadeBJ()
        CinematicFadeCommonBJ(red, green, blue, duration, tex, 100, trans)
    elif ( fadetype == bj_CINEFADETYPE_FADEIN ):
        AbortCinematicFadeBJ()
        CinematicFadeCommonBJ(red, green, blue, duration, tex, trans, 100)
        FinishCinematicFadeAfterBJ(duration)
    elif ( fadetype == bj_CINEFADETYPE_FADEOUTIN ):
        if ( duration > 0 ):
            AbortCinematicFadeBJ()
            CinematicFadeCommonBJ(red, green, blue, duration * 0.5, tex, 100, trans)
            ContinueCinematicFadeAfterBJ(duration * 0.5, red, green, blue, trans, tex)
            FinishCinematicFadeAfterBJ(duration)
    pass

def CinematicFilterGenericBJ(duration:"real", bmode:"blendmode", tex:"string", red0:"real", green0:"real", blue0:"real", trans0:"real", red1:"real", green1:"real", blue1:"real", trans1:"real")->"nothing":
    AbortCinematicFadeBJ()
    SetCineFilterTexture(tex)
    SetCineFilterBlendMode(bmode)
    SetCineFilterTexMapFlags(TEXMAP_FLAG_NONE)
    SetCineFilterStartUV(0, 0, 1, 1)
    SetCineFilterEndUV(0, 0, 1, 1)
    SetCineFilterStartColor(PercentTo255(red0), PercentTo255(green0), PercentTo255(blue0), PercentTo255(100 - trans0))
    SetCineFilterEndColor(PercentTo255(red1), PercentTo255(green1), PercentTo255(blue1), PercentTo255(100 - trans1))
    SetCineFilterDuration(duration)
    DisplayCineFilter(True)
    pass

def RescueUnitBJ(whichUnit:"unit", rescuer:"player", changeColor:"boolean")->"nothing":
    if IsUnitDeadBJ(whichUnit) or ( GetOwningPlayer(whichUnit) == rescuer ):
        pass

    StartSound(bj_rescueSound)
    SetUnitOwner(whichUnit, rescuer, changeColor)
    UnitAddIndicator(whichUnit, 0, 255, 0, 255)
    PingMinimapForPlayer(rescuer, GetUnitX(whichUnit), GetUnitY(whichUnit), bj_RESCUE_PING_TIME)
    pass

def TriggerActionUnitRescuedBJ()->"nothing":
    theUnit = GetTriggerUnit()
    if IsUnitType(theUnit, UNIT_TYPE_STRUCTURE):
        RescueUnitBJ(theUnit, GetOwningPlayer(GetRescuer()), bj_rescueChangeColorBldg)
    else:
        RescueUnitBJ(theUnit, GetOwningPlayer(GetRescuer()), bj_rescueChangeColorUnit)
    pass

def TryInitRescuableTriggersBJ()->"nothing":
    global bj_rescueUnitBehavior
    index = None
    if ( bj_rescueUnitBehavior == None ):
        bj_rescueUnitBehavior = CreateTrigger()
        index = 0
        while True:
            TriggerRegisterPlayerUnitEvent(bj_rescueUnitBehavior, Player(index), EVENT_PLAYER_UNIT_RESCUED, None)
            index = index + 1
            if index == bj_MAX_PLAYER_SLOTS:
                break
            pass

        TriggerAddAction(bj_rescueUnitBehavior, TriggerActionUnitRescuedBJ)
    pass

def SetRescueUnitColorChangeBJ(changeColor:"boolean")->"nothing":
    global bj_rescueChangeColorUnit
    bj_rescueChangeColorUnit = changeColor
    pass

def SetRescueBuildingColorChangeBJ(changeColor:"boolean")->"nothing":
    global bj_rescueChangeColorBldg
    bj_rescueChangeColorBldg = changeColor
    pass

def MakeUnitRescuableToForceBJEnum()->"nothing":
    TryInitRescuableTriggersBJ()
    SetUnitRescuable(bj_makeUnitRescuableUnit, GetEnumPlayer(), bj_makeUnitRescuableFlag)
    pass

def MakeUnitRescuableToForceBJ(whichUnit:"unit", isRescuable:"boolean", whichForce:"force")->"nothing":
    global bj_makeUnitRescuableFlag
    global bj_makeUnitRescuableUnit
    bj_makeUnitRescuableUnit = whichUnit
    bj_makeUnitRescuableFlag = isRescuable
    ForForce(whichForce, MakeUnitRescuableToForceBJEnum)
    pass

def InitRescuableBehaviorBJ()->"nothing":
    index = None
    index = 0
    while True:
        if ( GetPlayerController(Player(index)) == MAP_CONTROL_RESCUABLE ):
            TryInitRescuableTriggersBJ()
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    pass

def SetPlayerTechResearchedSwap(techid:"integer", levels:"integer", whichPlayer:"player")->"nothing":
    SetPlayerTechResearched(whichPlayer, techid, levels)
    pass

def SetPlayerTechMaxAllowedSwap(techid:"integer", maximum:"integer", whichPlayer:"player")->"nothing":
    SetPlayerTechMaxAllowed(whichPlayer, techid, maximum)
    pass

def SetPlayerMaxHeroesAllowed(maximum:"integer", whichPlayer:"player")->"nothing":
    SetPlayerTechMaxAllowed(whichPlayer, 1212502607, maximum)
    pass

def GetPlayerTechCountSimple(techid:"integer", whichPlayer:"player")->"integer":
    return GetPlayerTechCount(whichPlayer, techid, True)
    pass

def GetPlayerTechMaxAllowedSwap(techid:"integer", whichPlayer:"player")->"integer":
    return GetPlayerTechMaxAllowed(whichPlayer, techid)
    pass

def SetPlayerAbilityAvailableBJ(avail:"boolean", abilid:"integer", whichPlayer:"player")->"nothing":
    SetPlayerAbilityAvailable(whichPlayer, abilid, avail)
    pass

def SetCampaignMenuRaceBJ(campaignNumber:"integer")->"nothing":
    if ( campaignNumber == bj_CAMPAIGN_INDEX_T ):
        SetCampaignMenuRace(RACE_OTHER)
    elif ( campaignNumber == bj_CAMPAIGN_INDEX_H ):
        SetCampaignMenuRace(RACE_HUMAN)
    elif ( campaignNumber == bj_CAMPAIGN_INDEX_U ):
        SetCampaignMenuRace(RACE_UNDEAD)
    elif ( campaignNumber == bj_CAMPAIGN_INDEX_O ):
        SetCampaignMenuRace(RACE_ORC)
    elif ( campaignNumber == bj_CAMPAIGN_INDEX_N ):
        SetCampaignMenuRace(RACE_NIGHTELF)
    elif ( campaignNumber == bj_CAMPAIGN_INDEX_XN ):
        SetCampaignMenuRaceEx(bj_CAMPAIGN_OFFSET_XN)
    elif ( campaignNumber == bj_CAMPAIGN_INDEX_XH ):
        SetCampaignMenuRaceEx(bj_CAMPAIGN_OFFSET_XH)
    elif ( campaignNumber == bj_CAMPAIGN_INDEX_XU ):
        SetCampaignMenuRaceEx(bj_CAMPAIGN_OFFSET_XU)
    elif ( campaignNumber == bj_CAMPAIGN_INDEX_XO ):
        SetCampaignMenuRaceEx(bj_CAMPAIGN_OFFSET_XO)
    pass

def SetMissionAvailableBJ(available:"boolean", missionIndex:"integer")->"nothing":
    campaignNumber = missionIndex / 1000
    missionNumber = missionIndex - campaignNumber * 1000
    SetMissionAvailable(campaignNumber, missionNumber, available)
    pass

def SetCampaignAvailableBJ(available:"boolean", campaignNumber:"integer")->"nothing":
    campaignOffset = None
    if ( campaignNumber == bj_CAMPAIGN_INDEX_H ):
        SetTutorialCleared(True)
    if ( campaignNumber == bj_CAMPAIGN_INDEX_XN ):
        campaignOffset = bj_CAMPAIGN_OFFSET_XN
    elif ( campaignNumber == bj_CAMPAIGN_INDEX_XH ):
        campaignOffset = bj_CAMPAIGN_OFFSET_XH
    elif ( campaignNumber == bj_CAMPAIGN_INDEX_XU ):
        campaignOffset = bj_CAMPAIGN_OFFSET_XU
    elif ( campaignNumber == bj_CAMPAIGN_INDEX_XO ):
        campaignOffset = bj_CAMPAIGN_OFFSET_XO
    else:
        campaignOffset = campaignNumber
    SetCampaignAvailable(campaignOffset, available)
    SetCampaignMenuRaceBJ(campaignNumber)
    ForceCampaignSelectScreen()
    pass

def SetCinematicAvailableBJ(available:"boolean", cinematicIndex:"integer")->"nothing":
    if ( cinematicIndex == bj_CINEMATICINDEX_TOP ):
        SetOpCinematicAvailable(bj_CAMPAIGN_INDEX_T, available)
        PlayCinematic("TutorialOp" )
    elif ( cinematicIndex == bj_CINEMATICINDEX_HOP ):
        SetOpCinematicAvailable(bj_CAMPAIGN_INDEX_H, available)
        PlayCinematic("HumanOp" )
    elif ( cinematicIndex == bj_CINEMATICINDEX_HED ):
        SetEdCinematicAvailable(bj_CAMPAIGN_INDEX_H, available)
        PlayCinematic("HumanEd" )
    elif ( cinematicIndex == bj_CINEMATICINDEX_OOP ):
        SetOpCinematicAvailable(bj_CAMPAIGN_INDEX_O, available)
        PlayCinematic("OrcOp" )
    elif ( cinematicIndex == bj_CINEMATICINDEX_OED ):
        SetEdCinematicAvailable(bj_CAMPAIGN_INDEX_O, available)
        PlayCinematic("OrcEd" )
    elif ( cinematicIndex == bj_CINEMATICINDEX_UOP ):
        SetEdCinematicAvailable(bj_CAMPAIGN_INDEX_U, available)
        PlayCinematic("UndeadOp" )
    elif ( cinematicIndex == bj_CINEMATICINDEX_UED ):
        SetEdCinematicAvailable(bj_CAMPAIGN_INDEX_U, available)
        PlayCinematic("UndeadEd" )
    elif ( cinematicIndex == bj_CINEMATICINDEX_NOP ):
        SetEdCinematicAvailable(bj_CAMPAIGN_INDEX_N, available)
        PlayCinematic("NightElfOp" )
    elif ( cinematicIndex == bj_CINEMATICINDEX_NED ):
        SetEdCinematicAvailable(bj_CAMPAIGN_INDEX_N, available)
        PlayCinematic("NightElfEd" )
    elif ( cinematicIndex == bj_CINEMATICINDEX_XOP ):
        SetOpCinematicAvailable(bj_CAMPAIGN_OFFSET_XN, available)
        PlayCinematic("IntroX" )
    elif ( cinematicIndex == bj_CINEMATICINDEX_XED ):
        SetEdCinematicAvailable(bj_CAMPAIGN_OFFSET_XU, available)
        PlayCinematic("OutroX" )
    pass

def InitGameCacheBJ(campaignFile:"string")->"gamecache":
    global bj_lastCreatedGameCache
    bj_lastCreatedGameCache = InitGameCache(campaignFile)
    return bj_lastCreatedGameCache
    pass

def SaveGameCacheBJ(cache:"gamecache")->"boolean":
    return SaveGameCache(cache)
    pass

def GetLastCreatedGameCacheBJ()->"gamecache":
    return bj_lastCreatedGameCache
    pass

def InitHashtableBJ()->"hashtable":
    global bj_lastCreatedHashtable
    bj_lastCreatedHashtable = InitHashtable()
    return bj_lastCreatedHashtable
    pass

def GetLastCreatedHashtableBJ()->"hashtable":
    return bj_lastCreatedHashtable
    pass

def StoreRealBJ(value:"real", key:"string", missionKey:"string", cache:"gamecache")->"nothing":
    StoreReal(cache, missionKey, key, value)
    pass

def StoreIntegerBJ(value:"integer", key:"string", missionKey:"string", cache:"gamecache")->"nothing":
    StoreInteger(cache, missionKey, key, value)
    pass

def StoreBooleanBJ(value:"boolean", key:"string", missionKey:"string", cache:"gamecache")->"nothing":
    StoreBoolean(cache, missionKey, key, value)
    pass

def StoreStringBJ(value:"string", key:"string", missionKey:"string", cache:"gamecache")->"boolean":
    return StoreString(cache, missionKey, key, value)
    pass

def StoreUnitBJ(whichUnit:"unit", key:"string", missionKey:"string", cache:"gamecache")->"boolean":
    return StoreUnit(cache, missionKey, key, whichUnit)
    pass

def SaveRealBJ(value:"real", key:"integer", missionKey:"integer", table:"hashtable")->"nothing":
    SaveReal(table, missionKey, key, value)
    pass

def SaveIntegerBJ(value:"integer", key:"integer", missionKey:"integer", table:"hashtable")->"nothing":
    SaveInteger(table, missionKey, key, value)
    pass

def SaveBooleanBJ(value:"boolean", key:"integer", missionKey:"integer", table:"hashtable")->"nothing":
    SaveBoolean(table, missionKey, key, value)
    pass

def SaveStringBJ(value:"string", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveStr(table, missionKey, key, value)
    pass

def SavePlayerHandleBJ(whichPlayer:"player", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SavePlayerHandle(table, missionKey, key, whichPlayer)
    pass

def SaveWidgetHandleBJ(whichWidget:"widget", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveWidgetHandle(table, missionKey, key, whichWidget)
    pass

def SaveDestructableHandleBJ(whichDestructable:"destructable", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveDestructableHandle(table, missionKey, key, whichDestructable)
    pass

def SaveItemHandleBJ(whichItem:"item", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveItemHandle(table, missionKey, key, whichItem)
    pass

def SaveUnitHandleBJ(whichUnit:"unit", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveUnitHandle(table, missionKey, key, whichUnit)
    pass

def SaveAbilityHandleBJ(whichAbility:"ability", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveAbilityHandle(table, missionKey, key, whichAbility)
    pass

def SaveTimerHandleBJ(whichTimer:"timer", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveTimerHandle(table, missionKey, key, whichTimer)
    pass

def SaveTriggerHandleBJ(whichTrigger:"trigger", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveTriggerHandle(table, missionKey, key, whichTrigger)
    pass

def SaveTriggerConditionHandleBJ(whichTriggercondition:"triggercondition", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveTriggerConditionHandle(table, missionKey, key, whichTriggercondition)
    pass

def SaveTriggerActionHandleBJ(whichTriggeraction:"triggeraction", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveTriggerActionHandle(table, missionKey, key, whichTriggeraction)
    pass

def SaveTriggerEventHandleBJ(whichEvent:"event", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveTriggerEventHandle(table, missionKey, key, whichEvent)
    pass

def SaveForceHandleBJ(whichForce:"force", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveForceHandle(table, missionKey, key, whichForce)
    pass

def SaveGroupHandleBJ(whichGroup:"group", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveGroupHandle(table, missionKey, key, whichGroup)
    pass

def SaveLocationHandleBJ(whichLocation:"location", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveLocationHandle(table, missionKey, key, whichLocation)
    pass

def SaveRectHandleBJ(whichRect:"rect", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveRectHandle(table, missionKey, key, whichRect)
    pass

def SaveBooleanExprHandleBJ(whichBoolexpr:"boolexpr", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveBooleanExprHandle(table, missionKey, key, whichBoolexpr)
    pass

def SaveSoundHandleBJ(whichSound:"sound", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveSoundHandle(table, missionKey, key, whichSound)
    pass

def SaveEffectHandleBJ(whichEffect:"effect", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveEffectHandle(table, missionKey, key, whichEffect)
    pass

def SaveUnitPoolHandleBJ(whichUnitpool:"unitpool", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveUnitPoolHandle(table, missionKey, key, whichUnitpool)
    pass

def SaveItemPoolHandleBJ(whichItempool:"itempool", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveItemPoolHandle(table, missionKey, key, whichItempool)
    pass

def SaveQuestHandleBJ(whichQuest:"quest", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveQuestHandle(table, missionKey, key, whichQuest)
    pass

def SaveQuestItemHandleBJ(whichQuestitem:"questitem", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveQuestItemHandle(table, missionKey, key, whichQuestitem)
    pass

def SaveDefeatConditionHandleBJ(whichDefeatcondition:"defeatcondition", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveDefeatConditionHandle(table, missionKey, key, whichDefeatcondition)
    pass

def SaveTimerDialogHandleBJ(whichTimerdialog:"timerdialog", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveTimerDialogHandle(table, missionKey, key, whichTimerdialog)
    pass

def SaveLeaderboardHandleBJ(whichLeaderboard:"leaderboard", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveLeaderboardHandle(table, missionKey, key, whichLeaderboard)
    pass

def SaveMultiboardHandleBJ(whichMultiboard:"multiboard", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveMultiboardHandle(table, missionKey, key, whichMultiboard)
    pass

def SaveMultiboardItemHandleBJ(whichMultiboarditem:"multiboarditem", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveMultiboardItemHandle(table, missionKey, key, whichMultiboarditem)
    pass

def SaveTrackableHandleBJ(whichTrackable:"trackable", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveTrackableHandle(table, missionKey, key, whichTrackable)
    pass

def SaveDialogHandleBJ(whichDialog:"dialog", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveDialogHandle(table, missionKey, key, whichDialog)
    pass

def SaveButtonHandleBJ(whichButton:"button", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveButtonHandle(table, missionKey, key, whichButton)
    pass

def SaveTextTagHandleBJ(whichTexttag:"texttag", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveTextTagHandle(table, missionKey, key, whichTexttag)
    pass

def SaveLightningHandleBJ(whichLightning:"lightning", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveLightningHandle(table, missionKey, key, whichLightning)
    pass

def SaveImageHandleBJ(whichImage:"image", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveImageHandle(table, missionKey, key, whichImage)
    pass

def SaveUbersplatHandleBJ(whichUbersplat:"ubersplat", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveUbersplatHandle(table, missionKey, key, whichUbersplat)
    pass

def SaveRegionHandleBJ(whichRegion:"region", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveRegionHandle(table, missionKey, key, whichRegion)
    pass

def SaveFogStateHandleBJ(whichFogState:"fogstate", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveFogStateHandle(table, missionKey, key, whichFogState)
    pass

def SaveFogModifierHandleBJ(whichFogModifier:"fogmodifier", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveFogModifierHandle(table, missionKey, key, whichFogModifier)
    pass

def SaveAgentHandleBJ(whichAgent:"agent", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveAgentHandle(table, missionKey, key, whichAgent)
    pass

def SaveHashtableHandleBJ(whichHashtable:"hashtable", key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return SaveHashtableHandle(table, missionKey, key, whichHashtable)
    pass

def GetStoredRealBJ(key:"string", missionKey:"string", cache:"gamecache")->"real":
    return GetStoredReal(cache, missionKey, key)
    pass

def GetStoredIntegerBJ(key:"string", missionKey:"string", cache:"gamecache")->"integer":
    return GetStoredInteger(cache, missionKey, key)
    pass

def GetStoredBooleanBJ(key:"string", missionKey:"string", cache:"gamecache")->"boolean":
    return GetStoredBoolean(cache, missionKey, key)
    pass

def GetStoredStringBJ(key:"string", missionKey:"string", cache:"gamecache")->"string":
    s = None
    s = GetStoredString(cache, missionKey, key)
    if ( s == None ):
        return ""
    else:
        return s
    pass

def LoadRealBJ(key:"integer", missionKey:"integer", table:"hashtable")->"real":
    return LoadReal(table, missionKey, key)
    pass

def LoadIntegerBJ(key:"integer", missionKey:"integer", table:"hashtable")->"integer":
    return LoadInteger(table, missionKey, key)
    pass

def LoadBooleanBJ(key:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    return LoadBoolean(table, missionKey, key)
    pass

def LoadStringBJ(key:"integer", missionKey:"integer", table:"hashtable")->"string":
    s = None
    s = LoadStr(table, missionKey, key)
    if ( s == None ):
        return ""
    else:
        return s
    pass

def LoadPlayerHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"player":
    return LoadPlayerHandle(table, missionKey, key)
    pass

def LoadWidgetHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"widget":
    return LoadWidgetHandle(table, missionKey, key)
    pass

def LoadDestructableHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"destructable":
    return LoadDestructableHandle(table, missionKey, key)
    pass

def LoadItemHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"item":
    return LoadItemHandle(table, missionKey, key)
    pass

def LoadUnitHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"unit":
    return LoadUnitHandle(table, missionKey, key)
    pass

def LoadAbilityHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"ability":
    return LoadAbilityHandle(table, missionKey, key)
    pass

def LoadTimerHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"timer":
    return LoadTimerHandle(table, missionKey, key)
    pass

def LoadTriggerHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"trigger":
    return LoadTriggerHandle(table, missionKey, key)
    pass

def LoadTriggerConditionHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"triggercondition":
    return LoadTriggerConditionHandle(table, missionKey, key)
    pass

def LoadTriggerActionHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"triggeraction":
    return LoadTriggerActionHandle(table, missionKey, key)
    pass

def LoadTriggerEventHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"event":
    return LoadTriggerEventHandle(table, missionKey, key)
    pass

def LoadForceHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"force":
    return LoadForceHandle(table, missionKey, key)
    pass

def LoadGroupHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"group":
    return LoadGroupHandle(table, missionKey, key)
    pass

def LoadLocationHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"location":
    return LoadLocationHandle(table, missionKey, key)
    pass

def LoadRectHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"rect":
    return LoadRectHandle(table, missionKey, key)
    pass

def LoadBooleanExprHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"boolexpr":
    return LoadBooleanExprHandle(table, missionKey, key)
    pass

def LoadSoundHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"sound":
    return LoadSoundHandle(table, missionKey, key)
    pass

def LoadEffectHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"effect":
    return LoadEffectHandle(table, missionKey, key)
    pass

def LoadUnitPoolHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"unitpool":
    return LoadUnitPoolHandle(table, missionKey, key)
    pass

def LoadItemPoolHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"itempool":
    return LoadItemPoolHandle(table, missionKey, key)
    pass

def LoadQuestHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"quest":
    return LoadQuestHandle(table, missionKey, key)
    pass

def LoadQuestItemHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"questitem":
    return LoadQuestItemHandle(table, missionKey, key)
    pass

def LoadDefeatConditionHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"defeatcondition":
    return LoadDefeatConditionHandle(table, missionKey, key)
    pass

def LoadTimerDialogHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"timerdialog":
    return LoadTimerDialogHandle(table, missionKey, key)
    pass

def LoadLeaderboardHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"leaderboard":
    return LoadLeaderboardHandle(table, missionKey, key)
    pass

def LoadMultiboardHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"multiboard":
    return LoadMultiboardHandle(table, missionKey, key)
    pass

def LoadMultiboardItemHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"multiboarditem":
    return LoadMultiboardItemHandle(table, missionKey, key)
    pass

def LoadTrackableHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"trackable":
    return LoadTrackableHandle(table, missionKey, key)
    pass

def LoadDialogHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"dialog":
    return LoadDialogHandle(table, missionKey, key)
    pass

def LoadButtonHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"button":
    return LoadButtonHandle(table, missionKey, key)
    pass

def LoadTextTagHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"texttag":
    return LoadTextTagHandle(table, missionKey, key)
    pass

def LoadLightningHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"lightning":
    return LoadLightningHandle(table, missionKey, key)
    pass

def LoadImageHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"image":
    return LoadImageHandle(table, missionKey, key)
    pass

def LoadUbersplatHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"ubersplat":
    return LoadUbersplatHandle(table, missionKey, key)
    pass

def LoadRegionHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"region":
    return LoadRegionHandle(table, missionKey, key)
    pass

def LoadFogStateHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"fogstate":
    return LoadFogStateHandle(table, missionKey, key)
    pass

def LoadFogModifierHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"fogmodifier":
    return LoadFogModifierHandle(table, missionKey, key)
    pass

def LoadHashtableHandleBJ(key:"integer", missionKey:"integer", table:"hashtable")->"hashtable":
    return LoadHashtableHandle(table, missionKey, key)
    pass

def RestoreUnitLocFacingAngleBJ(key:"string", missionKey:"string", cache:"gamecache", forWhichPlayer:"player", loc:"location", facing:"real")->"unit":
    global bj_lastLoadedUnit
    bj_lastLoadedUnit = RestoreUnit(cache, missionKey, key, forWhichPlayer, GetLocationX(loc), GetLocationY(loc), facing)
    return bj_lastLoadedUnit
    pass

def RestoreUnitLocFacingPointBJ(key:"string", missionKey:"string", cache:"gamecache", forWhichPlayer:"player", loc:"location", lookAt:"location")->"unit":
    return RestoreUnitLocFacingAngleBJ(key, missionKey, cache, forWhichPlayer, loc, AngleBetweenPoints(loc, lookAt))
    pass

def GetLastRestoredUnitBJ()->"unit":
    return bj_lastLoadedUnit
    pass

def FlushGameCacheBJ(cache:"gamecache")->"nothing":
    FlushGameCache(cache)
    pass

def FlushStoredMissionBJ(missionKey:"string", cache:"gamecache")->"nothing":
    FlushStoredMission(cache, missionKey)
    pass

def FlushParentHashtableBJ(table:"hashtable")->"nothing":
    FlushParentHashtable(table)
    pass

def FlushChildHashtableBJ(missionKey:"integer", table:"hashtable")->"nothing":
    FlushChildHashtable(table, missionKey)
    pass

def HaveStoredValue(key:"string", valueType:"integer", missionKey:"string", cache:"gamecache")->"boolean":
    if ( valueType == bj_GAMECACHE_BOOLEAN ):
        return HaveStoredBoolean(cache, missionKey, key)
    elif ( valueType == bj_GAMECACHE_INTEGER ):
        return HaveStoredInteger(cache, missionKey, key)
    elif ( valueType == bj_GAMECACHE_REAL ):
        return HaveStoredReal(cache, missionKey, key)
    elif ( valueType == bj_GAMECACHE_UNIT ):
        return HaveStoredUnit(cache, missionKey, key)
    elif ( valueType == bj_GAMECACHE_STRING ):
        return HaveStoredString(cache, missionKey, key)
    else:
        return False
    pass

def HaveSavedValue(key:"integer", valueType:"integer", missionKey:"integer", table:"hashtable")->"boolean":
    if ( valueType == bj_HASHTABLE_BOOLEAN ):
        return HaveSavedBoolean(table, missionKey, key)
    elif ( valueType == bj_HASHTABLE_INTEGER ):
        return HaveSavedInteger(table, missionKey, key)
    elif ( valueType == bj_HASHTABLE_REAL ):
        return HaveSavedReal(table, missionKey, key)
    elif ( valueType == bj_HASHTABLE_STRING ):
        return HaveSavedString(table, missionKey, key)
    elif ( valueType == bj_HASHTABLE_HANDLE ):
        return HaveSavedHandle(table, missionKey, key)
    else:
        return False
    pass

def ShowCustomCampaignButton(show:"boolean", whichButton:"integer")->"nothing":
    SetCustomCampaignButtonVisible(whichButton - 1, show)
    pass

def IsCustomCampaignButtonVisibile(whichButton:"integer")->"boolean":
    return GetCustomCampaignButtonVisible(whichButton - 1)
    pass

def LoadGameBJ(loadFileName:"string", doScoreScreen:"boolean")->"nothing":
    LoadGame(loadFileName, doScoreScreen)
    pass

def SaveAndChangeLevelBJ(saveFileName:"string", newLevel:"string", doScoreScreen:"boolean")->"nothing":
    SaveGame(saveFileName)
    ChangeLevel(newLevel, doScoreScreen)
    pass

def SaveAndLoadGameBJ(saveFileName:"string", loadFileName:"string", doScoreScreen:"boolean")->"nothing":
    SaveGame(saveFileName)
    LoadGame(loadFileName, doScoreScreen)
    pass

def RenameSaveDirectoryBJ(sourceDirName:"string", destDirName:"string")->"boolean":
    return RenameSaveDirectory(sourceDirName, destDirName)
    pass

def RemoveSaveDirectoryBJ(sourceDirName:"string")->"boolean":
    return RemoveSaveDirectory(sourceDirName)
    pass

def CopySaveGameBJ(sourceSaveName:"string", destSaveName:"string")->"boolean":
    return CopySaveGame(sourceSaveName, destSaveName)
    pass

def GetPlayerStartLocationX(whichPlayer:"player")->"real":
    return GetStartLocationX(GetPlayerStartLocation(whichPlayer))
    pass

def GetPlayerStartLocationY(whichPlayer:"player")->"real":
    return GetStartLocationY(GetPlayerStartLocation(whichPlayer))
    pass

def GetPlayerStartLocationLoc(whichPlayer:"player")->"location":
    return GetStartLocationLoc(GetPlayerStartLocation(whichPlayer))
    pass

def GetRectCenter(whichRect:"rect")->"location":
    return Location(GetRectCenterX(whichRect), GetRectCenterY(whichRect))
    pass

def IsPlayerSlotState(whichPlayer:"player", whichState:"playerslotstate")->"boolean":
    return GetPlayerSlotState(whichPlayer) == whichState
    pass

def GetFadeFromSeconds(seconds:"real")->"integer":
    if ( seconds != 0 ):
        return 128 / R2I(seconds)
    return 10000
    pass

def GetFadeFromSecondsAsReal(seconds:"real")->"real":
    if ( seconds != 0 ):
        return 128.0 / seconds
    return 10000.0
    pass

def AdjustPlayerStateSimpleBJ(whichPlayer:"player", whichPlayerState:"playerstate", delta:"integer")->"nothing":
    SetPlayerState(whichPlayer, whichPlayerState, GetPlayerState(whichPlayer, whichPlayerState) + delta)
    pass

def AdjustPlayerStateBJ(delta:"integer", whichPlayer:"player", whichPlayerState:"playerstate")->"nothing":
    if ( delta > 0 ):
        if ( whichPlayerState == PLAYER_STATE_RESOURCE_GOLD ):
            AdjustPlayerStateSimpleBJ(whichPlayer, PLAYER_STATE_GOLD_GATHERED, delta)
        elif ( whichPlayerState == PLAYER_STATE_RESOURCE_LUMBER ):
            AdjustPlayerStateSimpleBJ(whichPlayer, PLAYER_STATE_LUMBER_GATHERED, delta)
    AdjustPlayerStateSimpleBJ(whichPlayer, whichPlayerState, delta)
    pass

def SetPlayerStateBJ(whichPlayer:"player", whichPlayerState:"playerstate", value:"integer")->"nothing":
    oldValue = GetPlayerState(whichPlayer, whichPlayerState)
    AdjustPlayerStateBJ(value - oldValue, whichPlayer, whichPlayerState)
    pass

def SetPlayerFlagBJ(whichPlayerFlag:"playerstate", flag:"boolean", whichPlayer:"player")->"nothing":
    SetPlayerState(whichPlayer, whichPlayerFlag, IntegerTertiaryOp(flag, 1, 0))
    pass

def SetPlayerTaxRateBJ(rate:"integer", whichResource:"playerstate", sourcePlayer:"player", otherPlayer:"player")->"nothing":
    SetPlayerTaxRate(sourcePlayer, otherPlayer, whichResource, rate)
    pass

def GetPlayerTaxRateBJ(whichResource:"playerstate", sourcePlayer:"player", otherPlayer:"player")->"integer":
    return GetPlayerTaxRate(sourcePlayer, otherPlayer, whichResource)
    pass

def IsPlayerFlagSetBJ(whichPlayerFlag:"playerstate", whichPlayer:"player")->"boolean":
    return GetPlayerState(whichPlayer, whichPlayerFlag) == 1
    pass

def AddResourceAmountBJ(delta:"integer", whichUnit:"unit")->"nothing":
    AddResourceAmount(whichUnit, delta)
    pass

def GetConvertedPlayerId(whichPlayer:"player")->"integer":
    return GetPlayerId(whichPlayer) + 1
    pass

def ConvertedPlayer(convertedPlayerId:"integer")->"player":
    return Player(convertedPlayerId - 1)
    pass

def GetRectWidthBJ(r:"rect")->"real":
    return GetRectMaxX(r) - GetRectMinX(r)
    pass

def GetRectHeightBJ(r:"rect")->"real":
    return GetRectMaxY(r) - GetRectMinY(r)
    pass

def BlightGoldMineForPlayerBJ(goldMine:"unit", whichPlayer:"player")->"unit":
    mineX = None
    mineY = None
    mineGold = None
    newMine = None
    if GetUnitTypeId(goldMine) != 1852272492:
        return None
    mineX = GetUnitX(goldMine)
    mineY = GetUnitY(goldMine)
    mineGold = GetResourceAmount(goldMine)
    RemoveUnit(goldMine)
    newMine = CreateBlightedGoldmine(whichPlayer, mineX, mineY, bj_UNIT_FACING)
    SetResourceAmount(newMine, mineGold)
    return newMine
    pass

def BlightGoldMineForPlayer(goldMine:"unit", whichPlayer:"player")->"unit":
    global bj_lastHauntedGoldMine
    bj_lastHauntedGoldMine = BlightGoldMineForPlayerBJ(goldMine, whichPlayer)
    return bj_lastHauntedGoldMine
    pass

def GetLastHauntedGoldMine()->"unit":
    return bj_lastHauntedGoldMine
    pass

def IsPointBlightedBJ(where:"location")->"boolean":
    return IsPointBlighted(GetLocationX(where), GetLocationY(where))
    pass

def SetPlayerColorBJEnum()->"nothing":
    SetUnitColor(GetEnumUnit(), bj_setPlayerTargetColor)
    pass

def SetPlayerColorBJ(whichPlayer:"player", color:"playercolor", changeExisting:"boolean")->"nothing":
    global bj_setPlayerTargetColor
    g = None
    SetPlayerColor(whichPlayer, color)
    if changeExisting:
        bj_setPlayerTargetColor = color
        g = CreateGroup()
        GroupEnumUnitsOfPlayer(g, whichPlayer, None)
        ForGroup(g, SetPlayerColorBJEnum)
        DestroyGroup(g)
    pass

def SetPlayerUnitAvailableBJ(unitId:"integer", allowed:"boolean", whichPlayer:"player")->"nothing":
    if allowed:
        SetPlayerTechMaxAllowed(whichPlayer, unitId, - 1)
    else:
        SetPlayerTechMaxAllowed(whichPlayer, unitId, 0)
    pass

def LockGameSpeedBJ()->"nothing":
    SetMapFlag(MAP_LOCK_SPEED, True)
    pass

def UnlockGameSpeedBJ()->"nothing":
    SetMapFlag(MAP_LOCK_SPEED, False)
    pass

def IssueTargetOrderBJ(whichUnit:"unit", order:"string", targetWidget:"widget")->"boolean":
    return IssueTargetOrder(whichUnit, order, targetWidget)
    pass

def IssuePointOrderLocBJ(whichUnit:"unit", order:"string", whichLocation:"location")->"boolean":
    return IssuePointOrderLoc(whichUnit, order, whichLocation)
    pass

def IssueTargetDestructableOrder(whichUnit:"unit", order:"string", targetWidget:"widget")->"boolean":
    return IssueTargetOrder(whichUnit, order, targetWidget)
    pass

def IssueTargetItemOrder(whichUnit:"unit", order:"string", targetWidget:"widget")->"boolean":
    return IssueTargetOrder(whichUnit, order, targetWidget)
    pass

def IssueImmediateOrderBJ(whichUnit:"unit", order:"string")->"boolean":
    return IssueImmediateOrder(whichUnit, order)
    pass

def GroupTargetOrderBJ(whichGroup:"group", order:"string", targetWidget:"widget")->"boolean":
    return GroupTargetOrder(whichGroup, order, targetWidget)
    pass

def GroupPointOrderLocBJ(whichGroup:"group", order:"string", whichLocation:"location")->"boolean":
    return GroupPointOrderLoc(whichGroup, order, whichLocation)
    pass

def GroupImmediateOrderBJ(whichGroup:"group", order:"string")->"boolean":
    return GroupImmediateOrder(whichGroup, order)
    pass

def GroupTargetDestructableOrder(whichGroup:"group", order:"string", targetWidget:"widget")->"boolean":
    return GroupTargetOrder(whichGroup, order, targetWidget)
    pass

def GroupTargetItemOrder(whichGroup:"group", order:"string", targetWidget:"widget")->"boolean":
    return GroupTargetOrder(whichGroup, order, targetWidget)
    pass

def GetDyingDestructable()->"destructable":
    return GetTriggerDestructable()
    pass

def SetUnitRallyPoint(whichUnit:"unit", targPos:"location")->"nothing":
    IssuePointOrderLocBJ(whichUnit, "setrally", targPos)
    pass

def SetUnitRallyUnit(whichUnit:"unit", targUnit:"unit")->"nothing":
    IssueTargetOrder(whichUnit, "setrally", targUnit)
    pass

def SetUnitRallyDestructable(whichUnit:"unit", targDest:"destructable")->"nothing":
    IssueTargetOrder(whichUnit, "setrally", targDest)
    pass

def SaveDyingWidget()->"nothing":
    global bj_lastDyingWidget
    bj_lastDyingWidget = GetTriggerWidget()
    pass

def SetBlightRectBJ(addBlight:"boolean", whichPlayer:"player", r:"rect")->"nothing":
    SetBlightRect(whichPlayer, r, addBlight)
    pass

def SetBlightRadiusLocBJ(addBlight:"boolean", whichPlayer:"player", loc:"location", radius:"real")->"nothing":
    SetBlightLoc(whichPlayer, loc, radius, addBlight)
    pass

def GetAbilityName(abilcode:"integer")->"string":
    return GetObjectName(abilcode)
    pass

def MeleeStartingVisibility()->"nothing":
    SetFloatGameState(GAME_STATE_TIME_OF_DAY, bj_MELEE_STARTING_TOD)
    pass

def MeleeStartingResources()->"nothing":
    index = None
    indexPlayer = None
    v = None
    startingGold = None
    startingLumber = None
    v = VersionGet()
    if ( v == VERSION_REIGN_OF_CHAOS ):
        startingGold = bj_MELEE_STARTING_GOLD_V0
        startingLumber = bj_MELEE_STARTING_LUMBER_V0
    else:
        startingGold = bj_MELEE_STARTING_GOLD_V1
        startingLumber = bj_MELEE_STARTING_LUMBER_V1
    index = 0
    while True:
        indexPlayer = Player(index)
        if ( GetPlayerSlotState(indexPlayer) == PLAYER_SLOT_STATE_PLAYING ):
            SetPlayerState(indexPlayer, PLAYER_STATE_RESOURCE_GOLD, startingGold)
            SetPlayerState(indexPlayer, PLAYER_STATE_RESOURCE_LUMBER, startingLumber)
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    pass

def ReducePlayerTechMaxAllowed(whichPlayer:"player", techId:"integer", limit:"integer")->"nothing":
    oldMax = GetPlayerTechMaxAllowed(whichPlayer, techId)
    if ( oldMax < 0 or oldMax > limit ):
        SetPlayerTechMaxAllowed(whichPlayer, techId, limit)
    pass

def MeleeStartingHeroLimit()->"nothing":
    index = None
    index = 0
    while True:
        SetPlayerMaxHeroesAllowed(bj_MELEE_HERO_LIMIT, Player(index))
        ReducePlayerTechMaxAllowed(Player(index), 1214344551, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1215130471, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1215324524, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1214409837, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1331850337, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1332109682, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1333027688, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1332963428, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1164207469, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1164666213, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1164799855, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1165451634, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1432642913, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1432646245, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1433168227, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1432580716, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1315988077, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1315074670, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1315858291, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1315990632, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1315074932, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1315007587, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1316252014, bj_MELEE_HERO_TYPE_LIMIT)
        ReducePlayerTechMaxAllowed(Player(index), 1315334514, bj_MELEE_HERO_TYPE_LIMIT)
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    pass

def MeleeTrainedUnitIsHeroBJFilter()->"boolean":
    return IsUnitType(GetFilterUnit(), UNIT_TYPE_HERO)
    pass

def MeleeGrantItemsToHero(whichUnit:"unit")->"nothing":
    owner = GetPlayerId(GetOwningPlayer(whichUnit))
    if ( bj_meleeTwinkedHeroes[owner] < bj_MELEE_MAX_TWINKED_HEROES ):
        UnitAddItemById(whichUnit, 1937012592)
        bj_meleeTwinkedHeroes[owner] = bj_meleeTwinkedHeroes[owner] + 1
    pass

def MeleeGrantItemsToTrainedHero()->"nothing":
    MeleeGrantItemsToHero(GetTrainedUnit())
    pass

def MeleeGrantItemsToHiredHero()->"nothing":
    MeleeGrantItemsToHero(GetSoldUnit())
    pass

def MeleeGrantHeroItems()->"nothing":
    global bj_meleeGrantHeroItems
    index = None
    trig = None
    index = 0
    while True:
        bj_meleeTwinkedHeroes[index] = 0
        index = index + 1
        if index == bj_MAX_PLAYER_SLOTS:
            break
        pass

    index = 0
    while True:
        trig = CreateTrigger()
        TriggerRegisterPlayerUnitEvent(trig, Player(index), EVENT_PLAYER_UNIT_TRAIN_FINISH, filterMeleeTrainedUnitIsHeroBJ)
        TriggerAddAction(trig, MeleeGrantItemsToTrainedHero)
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    trig = CreateTrigger()
    TriggerRegisterPlayerUnitEvent(trig, Player(PLAYER_NEUTRAL_PASSIVE), EVENT_PLAYER_UNIT_SELL, filterMeleeTrainedUnitIsHeroBJ)
    TriggerAddAction(trig, MeleeGrantItemsToHiredHero)
    bj_meleeGrantHeroItems = True
    pass

def MeleeClearExcessUnit()->"nothing":
    theUnit = GetEnumUnit()
    owner = GetPlayerId(GetOwningPlayer(theUnit))
    if ( owner == PLAYER_NEUTRAL_AGGRESSIVE ):
        RemoveUnit(GetEnumUnit())
    elif ( owner == PLAYER_NEUTRAL_PASSIVE ):
        if not  IsUnitType(theUnit, UNIT_TYPE_STRUCTURE):
            RemoveUnit(GetEnumUnit())
    pass

def MeleeClearNearbyUnits(x:"real", y:"real", range:"real")->"nothing":
    nearbyUnits = None
    nearbyUnits = CreateGroup()
    GroupEnumUnitsInRange(nearbyUnits, x, y, range, None)
    ForGroup(nearbyUnits, MeleeClearExcessUnit)
    DestroyGroup(nearbyUnits)
    pass

def MeleeClearExcessUnits()->"nothing":
    index = None
    locX = None
    locY = None
    indexPlayer = None
    index = 0
    while True:
        indexPlayer = Player(index)
        if ( GetPlayerSlotState(indexPlayer) == PLAYER_SLOT_STATE_PLAYING ):
            locX = GetStartLocationX(GetPlayerStartLocation(indexPlayer))
            locY = GetStartLocationY(GetPlayerStartLocation(indexPlayer))
            MeleeClearNearbyUnits(locX, locY, bj_MELEE_CLEAR_UNITS_RADIUS)
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    pass

def MeleeEnumFindNearestMine()->"nothing":
    global bj_meleeNearestMine
    global bj_meleeNearestMineDist
    enumUnit = GetEnumUnit()
    dist = None
    unitLoc = None
    if ( GetUnitTypeId(enumUnit) == 1852272492 ):
        unitLoc = GetUnitLoc(enumUnit)
        dist = DistanceBetweenPoints(unitLoc, bj_meleeNearestMineToLoc)
        RemoveLocation(unitLoc)
        if ( bj_meleeNearestMineDist < 0 ) or ( dist < bj_meleeNearestMineDist ):
            bj_meleeNearestMine = enumUnit
            bj_meleeNearestMineDist = dist
    pass

def MeleeFindNearestMine(src:"location", range:"real")->"unit":
    global bj_meleeNearestMineToLoc
    global bj_meleeNearestMine
    global bj_meleeNearestMineDist
    nearbyMines = None
    bj_meleeNearestMine = None
    bj_meleeNearestMineDist = - 1
    bj_meleeNearestMineToLoc = src
    nearbyMines = CreateGroup()
    GroupEnumUnitsInRangeOfLoc(nearbyMines, src, range, None)
    ForGroup(nearbyMines, MeleeEnumFindNearestMine)
    DestroyGroup(nearbyMines)
    return bj_meleeNearestMine
    pass

def MeleeRandomHeroLoc(p:"player", id1:"integer", id2:"integer", id3:"integer", id4:"integer", loc:"location")->"unit":
    hero = None
    roll = None
    pick = None
    v = None
    v = VersionGet()
    if ( v == VERSION_REIGN_OF_CHAOS ):
        roll = GetRandomInt(1, 3)
    else:
        roll = GetRandomInt(1, 4)
    if roll == 1:
        pick = id1
    elif roll == 2:
        pick = id2
    elif roll == 3:
        pick = id3
    elif roll == 4:
        pick = id4
    else:
        pick = id1
    hero = CreateUnitAtLoc(p, pick, loc, bj_UNIT_FACING)
    if bj_meleeGrantHeroItems:
        MeleeGrantItemsToHero(hero)
    return hero
    pass

def MeleeGetProjectedLoc(src:"location", targ:"location", distance:"real", deltaAngle:"real")->"location":
    srcX = GetLocationX(src)
    srcY = GetLocationY(src)
    direction = Atan2(GetLocationY(targ) - srcY, GetLocationX(targ) - srcX) + deltaAngle
    return Location(srcX + distance * Cos(direction), srcY + distance * Sin(direction))
    pass

def MeleeGetNearestValueWithin(val:"real", minVal:"real", maxVal:"real")->"real":
    if ( val < minVal ):
        return minVal
    elif ( val > maxVal ):
        return maxVal
    else:
        return val
    pass

def MeleeGetLocWithinRect(src:"location", r:"rect")->"location":
    withinX = MeleeGetNearestValueWithin(GetLocationX(src), GetRectMinX(r), GetRectMaxX(r))
    withinY = MeleeGetNearestValueWithin(GetLocationY(src), GetRectMinY(r), GetRectMaxY(r))
    return Location(withinX, withinY)
    pass

def MeleeStartingUnitsHuman(whichPlayer:"player", startLoc:"location", doHeroes:"boolean", doCamera:"boolean", doPreload:"boolean")->"nothing":
    useRandomHero = IsMapFlagSet(MAP_RANDOM_HERO)
    unitSpacing = 64.0
    nearestMine = None
    nearMineLoc = None
    heroLoc = None
    peonX = None
    peonY = None
    townHall = None
    if ( doPreload ):
        Preloader("scripts\\HumanMelee.pld" )
    nearestMine = MeleeFindNearestMine(startLoc, bj_MELEE_MINE_SEARCH_RADIUS)
    if ( nearestMine != None ):
        townHall = CreateUnitAtLoc(whichPlayer, 1752461175, startLoc, bj_UNIT_FACING)
        nearMineLoc = MeleeGetProjectedLoc(GetUnitLoc(nearestMine), startLoc, 320, 0)
        peonX = GetLocationX(nearMineLoc)
        peonY = GetLocationY(nearMineLoc)
        CreateUnit(whichPlayer, 1752196449, peonX + 0.0 * unitSpacing, peonY + 1.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1752196449, peonX + 1.0 * unitSpacing, peonY + 0.15 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1752196449, peonX - 1.0 * unitSpacing, peonY + 0.15 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1752196449, peonX + 0.6 * unitSpacing, peonY - 1.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1752196449, peonX - 0.6 * unitSpacing, peonY - 1.0 * unitSpacing, bj_UNIT_FACING)
        heroLoc = MeleeGetProjectedLoc(GetUnitLoc(nearestMine), startLoc, 384, 45)
    else:
        townHall = CreateUnitAtLoc(whichPlayer, 1752461175, startLoc, bj_UNIT_FACING)
        peonX = GetLocationX(startLoc)
        peonY = GetLocationY(startLoc) - 224.0
        CreateUnit(whichPlayer, 1752196449, peonX + 2.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1752196449, peonX + 1.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1752196449, peonX + 0.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1752196449, peonX - 1.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1752196449, peonX - 2.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        heroLoc = Location(peonX, peonY - 2.0 * unitSpacing)
    if ( townHall != None ):
        UnitAddAbilityBJ(1097689443, townHall)
        UnitMakeAbilityPermanentBJ(True, 1097689443, townHall)
    if ( doHeroes ):
        if useRandomHero:
            MeleeRandomHeroLoc(whichPlayer, 1214344551, 1215130471, 1215324524, 1214409837, heroLoc)
        else:
            SetPlayerState(whichPlayer, PLAYER_STATE_RESOURCE_HERO_TOKENS, bj_MELEE_STARTING_HERO_TOKENS)
    if ( doCamera ):
        SetCameraPositionForPlayer(whichPlayer, peonX, peonY)
        SetCameraQuickPositionForPlayer(whichPlayer, peonX, peonY)
    pass

def MeleeStartingUnitsOrc(whichPlayer:"player", startLoc:"location", doHeroes:"boolean", doCamera:"boolean", doPreload:"boolean")->"nothing":
    useRandomHero = IsMapFlagSet(MAP_RANDOM_HERO)
    unitSpacing = 64.0
    nearestMine = None
    nearMineLoc = None
    heroLoc = None
    peonX = None
    peonY = None
    if ( doPreload ):
        Preloader("scripts\\OrcMelee.pld" )
    nearestMine = MeleeFindNearestMine(startLoc, bj_MELEE_MINE_SEARCH_RADIUS)
    if ( nearestMine != None ):
        CreateUnitAtLoc(whichPlayer, 1869050469, startLoc, bj_UNIT_FACING)
        nearMineLoc = MeleeGetProjectedLoc(GetUnitLoc(nearestMine), startLoc, 320, 0)
        peonX = GetLocationX(nearMineLoc)
        peonY = GetLocationY(nearMineLoc)
        CreateUnit(whichPlayer, 1869636975, peonX + 0.0 * unitSpacing, peonY + 1.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1869636975, peonX + 1.0 * unitSpacing, peonY + 0.15 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1869636975, peonX - 1.0 * unitSpacing, peonY + 0.15 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1869636975, peonX + 0.6 * unitSpacing, peonY - 1.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1869636975, peonX - 0.6 * unitSpacing, peonY - 1.0 * unitSpacing, bj_UNIT_FACING)
        heroLoc = MeleeGetProjectedLoc(GetUnitLoc(nearestMine), startLoc, 384, 45)
    else:
        CreateUnitAtLoc(whichPlayer, 1869050469, startLoc, bj_UNIT_FACING)
        peonX = GetLocationX(startLoc)
        peonY = GetLocationY(startLoc) - 224.0
        CreateUnit(whichPlayer, 1869636975, peonX + 2.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1869636975, peonX + 1.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1869636975, peonX + 0.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1869636975, peonX - 1.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1869636975, peonX - 2.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        heroLoc = Location(peonX, peonY - 2.0 * unitSpacing)
    if ( doHeroes ):
        if useRandomHero:
            MeleeRandomHeroLoc(whichPlayer, 1331850337, 1332109682, 1333027688, 1332963428, heroLoc)
        else:
            SetPlayerState(whichPlayer, PLAYER_STATE_RESOURCE_HERO_TOKENS, bj_MELEE_STARTING_HERO_TOKENS)
    if ( doCamera ):
        SetCameraPositionForPlayer(whichPlayer, peonX, peonY)
        SetCameraQuickPositionForPlayer(whichPlayer, peonX, peonY)
    pass

def MeleeStartingUnitsUndead(whichPlayer:"player", startLoc:"location", doHeroes:"boolean", doCamera:"boolean", doPreload:"boolean")->"nothing":
    useRandomHero = IsMapFlagSet(MAP_RANDOM_HERO)
    unitSpacing = 64.0
    nearestMine = None
    nearMineLoc = None
    nearTownLoc = None
    heroLoc = None
    peonX = None
    peonY = None
    ghoulX = None
    ghoulY = None
    if ( doPreload ):
        Preloader("scripts\\UndeadMelee.pld" )
    nearestMine = MeleeFindNearestMine(startLoc, bj_MELEE_MINE_SEARCH_RADIUS)
    if ( nearestMine != None ):
        CreateUnitAtLoc(whichPlayer, 1970172012, startLoc, bj_UNIT_FACING)
        nearestMine = BlightGoldMineForPlayerBJ(nearestMine, whichPlayer)
        nearTownLoc = MeleeGetProjectedLoc(startLoc, GetUnitLoc(nearestMine), 288, 0)
        ghoulX = GetLocationX(nearTownLoc)
        ghoulY = GetLocationY(nearTownLoc)
        bj_ghoul[GetPlayerId(whichPlayer)] = CreateUnit(whichPlayer, 1969711215, ghoulX + 0.0 * unitSpacing, ghoulY + 0.0 * unitSpacing, bj_UNIT_FACING)
        nearMineLoc = MeleeGetProjectedLoc(GetUnitLoc(nearestMine), startLoc, 320, 0)
        peonX = GetLocationX(nearMineLoc)
        peonY = GetLocationY(nearMineLoc)
        CreateUnit(whichPlayer, 1969316719, peonX + 0.0 * unitSpacing, peonY + 0.5 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1969316719, peonX + 0.65 * unitSpacing, peonY - 0.5 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1969316719, peonX - 0.65 * unitSpacing, peonY - 0.5 * unitSpacing, bj_UNIT_FACING)
        SetBlightLoc(whichPlayer, nearMineLoc, 768, True)
        heroLoc = MeleeGetProjectedLoc(GetUnitLoc(nearestMine), startLoc, 384, 45)
    else:
        CreateUnitAtLoc(whichPlayer, 1970172012, startLoc, bj_UNIT_FACING)
        peonX = GetLocationX(startLoc)
        peonY = GetLocationY(startLoc) - 224.0
        CreateUnit(whichPlayer, 1969316719, peonX - 1.5 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1969316719, peonX - 0.5 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1969316719, peonX + 0.5 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1969711215, peonX + 1.5 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        SetBlightLoc(whichPlayer, startLoc, 768, True)
        heroLoc = Location(peonX, peonY - 2.0 * unitSpacing)
    if ( doHeroes ):
        if useRandomHero:
            MeleeRandomHeroLoc(whichPlayer, 1432642913, 1432646245, 1433168227, 1432580716, heroLoc)
        else:
            SetPlayerState(whichPlayer, PLAYER_STATE_RESOURCE_HERO_TOKENS, bj_MELEE_STARTING_HERO_TOKENS)
    if ( doCamera ):
        SetCameraPositionForPlayer(whichPlayer, peonX, peonY)
        SetCameraQuickPositionForPlayer(whichPlayer, peonX, peonY)
    pass

def MeleeStartingUnitsNightElf(whichPlayer:"player", startLoc:"location", doHeroes:"boolean", doCamera:"boolean", doPreload:"boolean")->"nothing":
    useRandomHero = IsMapFlagSet(MAP_RANDOM_HERO)
    unitSpacing = 64.0
    minTreeDist = 3.5 * bj_CELLWIDTH
    minWispDist = 1.75 * bj_CELLWIDTH
    nearestMine = None
    nearMineLoc = None
    wispLoc = None
    heroLoc = None
    peonX = None
    peonY = None
    tree = None
    if ( doPreload ):
        Preloader("scripts\\NightElfMelee.pld" )
    nearestMine = MeleeFindNearestMine(startLoc, bj_MELEE_MINE_SEARCH_RADIUS)
    if ( nearestMine != None ):
        nearMineLoc = MeleeGetProjectedLoc(GetUnitLoc(nearestMine), startLoc, 650, 0)
        nearMineLoc = MeleeGetLocWithinRect(nearMineLoc, GetRectFromCircleBJ(GetUnitLoc(nearestMine), minTreeDist))
        tree = CreateUnitAtLoc(whichPlayer, 1702129516, nearMineLoc, bj_UNIT_FACING)
        IssueTargetOrder(tree, "entangleinstant", nearestMine)
        wispLoc = MeleeGetProjectedLoc(GetUnitLoc(nearestMine), startLoc, 320, 0)
        wispLoc = MeleeGetLocWithinRect(wispLoc, GetRectFromCircleBJ(GetUnitLoc(nearestMine), minWispDist))
        peonX = GetLocationX(wispLoc)
        peonY = GetLocationY(wispLoc)
        CreateUnit(whichPlayer, 1702327152, peonX + 0.0 * unitSpacing, peonY + 1.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1702327152, peonX + 1.0 * unitSpacing, peonY + 0.15 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1702327152, peonX - 1.0 * unitSpacing, peonY + 0.15 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1702327152, peonX + 0.58 * unitSpacing, peonY - 1.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1702327152, peonX - 0.58 * unitSpacing, peonY - 1.0 * unitSpacing, bj_UNIT_FACING)
        heroLoc = MeleeGetProjectedLoc(GetUnitLoc(nearestMine), startLoc, 384, 45)
    else:
        CreateUnitAtLoc(whichPlayer, 1702129516, startLoc, bj_UNIT_FACING)
        peonX = GetLocationX(startLoc)
        peonY = GetLocationY(startLoc) - 224.0
        CreateUnit(whichPlayer, 1702327152, peonX - 2.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1702327152, peonX - 1.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1702327152, peonX + 0.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1702327152, peonX + 1.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        CreateUnit(whichPlayer, 1702327152, peonX + 2.0 * unitSpacing, peonY + 0.0 * unitSpacing, bj_UNIT_FACING)
        heroLoc = Location(peonX, peonY - 2.0 * unitSpacing)
    if ( doHeroes ):
        if useRandomHero:
            MeleeRandomHeroLoc(whichPlayer, 1164207469, 1164666213, 1164799855, 1165451634, heroLoc)
        else:
            SetPlayerState(whichPlayer, PLAYER_STATE_RESOURCE_HERO_TOKENS, bj_MELEE_STARTING_HERO_TOKENS)
    if ( doCamera ):
        SetCameraPositionForPlayer(whichPlayer, peonX, peonY)
        SetCameraQuickPositionForPlayer(whichPlayer, peonX, peonY)
    pass

def MeleeStartingUnitsUnknownRace(whichPlayer:"player", startLoc:"location", doHeroes:"boolean", doCamera:"boolean", doPreload:"boolean")->"nothing":
    index = None
    if ( doPreload ):
        pass

    index = 0
    while True:
        CreateUnit(whichPlayer, 1853057125, GetLocationX(startLoc) + GetRandomReal(- 256, 256), GetLocationY(startLoc) + GetRandomReal(- 256, 256), GetRandomReal(0, 360))
        index = index + 1
        if index == 12:
            break
        pass

    if ( doHeroes ):
        SetPlayerState(whichPlayer, PLAYER_STATE_RESOURCE_HERO_TOKENS, bj_MELEE_STARTING_HERO_TOKENS)
    if ( doCamera ):
        SetCameraPositionLocForPlayer(whichPlayer, startLoc)
        SetCameraQuickPositionLocForPlayer(whichPlayer, startLoc)
    pass

def MeleeStartingUnits()->"nothing":
    index = None
    indexPlayer = None
    indexStartLoc = None
    indexRace = None
    Preloader("scripts\\SharedMelee.pld" )
    index = 0
    while True:
        indexPlayer = Player(index)
        if ( GetPlayerSlotState(indexPlayer) == PLAYER_SLOT_STATE_PLAYING ):
            indexStartLoc = GetStartLocationLoc(GetPlayerStartLocation(indexPlayer))
            indexRace = GetPlayerRace(indexPlayer)
            if ( indexRace == RACE_HUMAN ):
                MeleeStartingUnitsHuman(indexPlayer, indexStartLoc, True, True, True)
            elif ( indexRace == RACE_ORC ):
                MeleeStartingUnitsOrc(indexPlayer, indexStartLoc, True, True, True)
            elif ( indexRace == RACE_UNDEAD ):
                MeleeStartingUnitsUndead(indexPlayer, indexStartLoc, True, True, True)
            elif ( indexRace == RACE_NIGHTELF ):
                MeleeStartingUnitsNightElf(indexPlayer, indexStartLoc, True, True, True)
            else:
                MeleeStartingUnitsUnknownRace(indexPlayer, indexStartLoc, True, True, True)
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    pass

def MeleeStartingUnitsForPlayer(whichRace:"race", whichPlayer:"player", loc:"location", doHeroes:"boolean")->"nothing":
    if ( whichRace == RACE_HUMAN ):
        MeleeStartingUnitsHuman(whichPlayer, loc, doHeroes, False, False)
    elif ( whichRace == RACE_ORC ):
        MeleeStartingUnitsOrc(whichPlayer, loc, doHeroes, False, False)
    elif ( whichRace == RACE_UNDEAD ):
        MeleeStartingUnitsUndead(whichPlayer, loc, doHeroes, False, False)
    elif ( whichRace == RACE_NIGHTELF ):
        MeleeStartingUnitsNightElf(whichPlayer, loc, doHeroes, False, False)
    pass

def PickMeleeAI(num:"player", s1:"string", s2:"string", s3:"string")->"nothing":
    pick = None
    if GetAIDifficulty(num) == AI_DIFFICULTY_NEWBIE:
        StartMeleeAI(num, s1)
    if s2 == None:
        pick = 1
    elif s3 == None:
        pick = GetRandomInt(1, 2)
    else:
        pick = GetRandomInt(1, 3)
    if pick == 1:
        StartMeleeAI(num, s1)
    elif pick == 2:
        StartMeleeAI(num, s2)
    else:
        StartMeleeAI(num, s3)
    pass

def MeleeStartingAI()->"nothing":
    index = None
    indexPlayer = None
    indexRace = None
    index = 0
    while True:
        indexPlayer = Player(index)
        if ( GetPlayerSlotState(indexPlayer) == PLAYER_SLOT_STATE_PLAYING ):
            indexRace = GetPlayerRace(indexPlayer)
            if ( GetPlayerController(indexPlayer) == MAP_CONTROL_COMPUTER ):
                if ( indexRace == RACE_HUMAN ):
                    PickMeleeAI(indexPlayer, "human.ai", None, None)
                elif ( indexRace == RACE_ORC ):
                    PickMeleeAI(indexPlayer, "orc.ai", None, None)
                elif ( indexRace == RACE_UNDEAD ):
                    PickMeleeAI(indexPlayer, "undead.ai", None, None)
                    RecycleGuardPosition(bj_ghoul[index])
                elif ( indexRace == RACE_NIGHTELF ):
                    PickMeleeAI(indexPlayer, "elf.ai", None, None)
                ShareEverythingWithTeamAI(indexPlayer)
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    pass

def LockGuardPosition(targ:"unit")->"nothing":
    SetUnitCreepGuard(targ, True)
    pass

def MeleePlayerIsOpponent(playerIndex:"integer", opponentIndex:"integer")->"boolean":
    thePlayer = Player(playerIndex)
    theOpponent = Player(opponentIndex)
    if ( playerIndex == opponentIndex ):
        return False
    if ( GetPlayerSlotState(theOpponent) != PLAYER_SLOT_STATE_PLAYING ):
        return False
    if ( bj_meleeDefeated[opponentIndex] ):
        return False
    if GetPlayerAlliance(thePlayer, theOpponent, ALLIANCE_PASSIVE):
        if GetPlayerAlliance(theOpponent, thePlayer, ALLIANCE_PASSIVE):
            if ( GetPlayerState(thePlayer, PLAYER_STATE_ALLIED_VICTORY) == 1 ):
                if ( GetPlayerState(theOpponent, PLAYER_STATE_ALLIED_VICTORY) == 1 ):
                    return False
    return True
    pass

def MeleeGetAllyStructureCount(whichPlayer:"player")->"integer":
    playerIndex = None
    buildingCount = None
    indexPlayer = None
    buildingCount = 0
    playerIndex = 0
    while True:
        indexPlayer = Player(playerIndex)
        if ( PlayersAreCoAllied(whichPlayer, indexPlayer) ):
            buildingCount = buildingCount + GetPlayerStructureCount(indexPlayer, True)
        playerIndex = playerIndex + 1
        if playerIndex == bj_MAX_PLAYERS:
            break
        pass

    return buildingCount
    pass

def MeleeGetAllyCount(whichPlayer:"player")->"integer":
    playerIndex = None
    playerCount = None
    indexPlayer = None
    playerCount = 0
    playerIndex = 0
    while True:
        indexPlayer = Player(playerIndex)
        if PlayersAreCoAllied(whichPlayer, indexPlayer) and not  bj_meleeDefeated[playerIndex] and ( whichPlayer != indexPlayer ):
            playerCount = playerCount + 1
        playerIndex = playerIndex + 1
        if playerIndex == bj_MAX_PLAYERS:
            break
        pass

    return playerCount
    pass

def MeleeGetAllyKeyStructureCount(whichPlayer:"player")->"integer":
    playerIndex = None
    indexPlayer = None
    keyStructs = None
    keyStructs = 0
    playerIndex = 0
    while True:
        indexPlayer = Player(playerIndex)
        if ( PlayersAreCoAllied(whichPlayer, indexPlayer) ):
            keyStructs = keyStructs + GetPlayerTypedUnitCount(indexPlayer, "townhall", True, True)
            keyStructs = keyStructs + GetPlayerTypedUnitCount(indexPlayer, "greathall", True, True)
            keyStructs = keyStructs + GetPlayerTypedUnitCount(indexPlayer, "treeoflife", True, True)
            keyStructs = keyStructs + GetPlayerTypedUnitCount(indexPlayer, "necropolis", True, True)
        playerIndex = playerIndex + 1
        if playerIndex == bj_MAX_PLAYERS:
            break
        pass

    return keyStructs
    pass

def MeleeDoDrawEnum()->"nothing":
    thePlayer = GetEnumPlayer()
    CachePlayerHeroData(thePlayer)
    RemovePlayerPreserveUnitsBJ(thePlayer, PLAYER_GAME_RESULT_TIE, False)
    pass

def MeleeDoVictoryEnum()->"nothing":
    thePlayer = GetEnumPlayer()
    playerIndex = GetPlayerId(thePlayer)
    if ( not  bj_meleeVictoried[playerIndex] ):
        bj_meleeVictoried[playerIndex] = True
        CachePlayerHeroData(thePlayer)
        RemovePlayerPreserveUnitsBJ(thePlayer, PLAYER_GAME_RESULT_VICTORY, False)
    pass

def MeleeDoDefeat(whichPlayer:"player")->"nothing":
    bj_meleeDefeated[GetPlayerId(whichPlayer)] = True
    RemovePlayerPreserveUnitsBJ(whichPlayer, PLAYER_GAME_RESULT_DEFEAT, False)
    pass

def MeleeDoDefeatEnum()->"nothing":
    thePlayer = GetEnumPlayer()
    CachePlayerHeroData(thePlayer)
    MakeUnitsPassiveForTeam(thePlayer)
    MeleeDoDefeat(thePlayer)
    pass

def MeleeDoLeave(whichPlayer:"player")->"nothing":
    if ( GetIntegerGameState(GAME_STATE_DISCONNECTED) != 0 ):
        GameOverDialogBJ(whichPlayer, True)
    else:
        bj_meleeDefeated[GetPlayerId(whichPlayer)] = True
        RemovePlayerPreserveUnitsBJ(whichPlayer, PLAYER_GAME_RESULT_DEFEAT, True)
    pass

def MeleeRemoveObservers()->"nothing":
    playerIndex = None
    indexPlayer = None
    playerIndex = 0
    while True:
        indexPlayer = Player(playerIndex)
        if ( IsPlayerObserver(indexPlayer) ):
            RemovePlayerPreserveUnitsBJ(indexPlayer, PLAYER_GAME_RESULT_NEUTRAL, False)
        playerIndex = playerIndex + 1
        if playerIndex == bj_MAX_PLAYERS:
            break
        pass

    pass

def MeleeCheckForVictors()->"force":
    global bj_meleeGameOver
    playerIndex = None
    opponentIndex = None
    opponentlessPlayers = CreateForce()
    gameOver = False
    playerIndex = 0
    while True:
        if ( not  bj_meleeDefeated[playerIndex] ):
            opponentIndex = 0
            while True:
                if MeleePlayerIsOpponent(playerIndex, opponentIndex):
                    return CreateForce()
                opponentIndex = opponentIndex + 1
                if opponentIndex == bj_MAX_PLAYERS:
                    break
                pass

            ForceAddPlayer(opponentlessPlayers, Player(playerIndex))
            gameOver = True
        playerIndex = playerIndex + 1
        if playerIndex == bj_MAX_PLAYERS:
            break
        pass

    bj_meleeGameOver = gameOver
    return opponentlessPlayers
    pass

def MeleeCheckForLosersAndVictors()->"nothing":
    global bj_meleeGameOver
    playerIndex = None
    indexPlayer = None
    defeatedPlayers = CreateForce()
    victoriousPlayers = None
    gameOver = False
    if ( bj_meleeGameOver ):
        pass

    if ( GetIntegerGameState(GAME_STATE_DISCONNECTED) != 0 ):
        bj_meleeGameOver = True
    playerIndex = 0
    while True:
        indexPlayer = Player(playerIndex)
        if ( not  bj_meleeDefeated[playerIndex] and not  bj_meleeVictoried[playerIndex] ):
            if ( MeleeGetAllyStructureCount(indexPlayer) <= 0 ):
                ForceAddPlayer(defeatedPlayers, Player(playerIndex))
                bj_meleeDefeated[playerIndex] = True
        playerIndex = playerIndex + 1
        if playerIndex == bj_MAX_PLAYERS:
            break
        pass

    victoriousPlayers = MeleeCheckForVictors()
    ForForce(defeatedPlayers, MeleeDoDefeatEnum)
    ForForce(victoriousPlayers, MeleeDoVictoryEnum)
    if ( bj_meleeGameOver ):
        MeleeRemoveObservers()
    pass

def MeleeGetCrippledWarningMessage(whichPlayer:"player")->"string":
    r = GetPlayerRace(whichPlayer)
    if ( r == RACE_HUMAN ):
        return GetLocalizedString("CRIPPLE_WARNING_HUMAN")
    elif ( r == RACE_ORC ):
        return GetLocalizedString("CRIPPLE_WARNING_ORC")
    elif ( r == RACE_NIGHTELF ):
        return GetLocalizedString("CRIPPLE_WARNING_NIGHTELF")
    elif ( r == RACE_UNDEAD ):
        return GetLocalizedString("CRIPPLE_WARNING_UNDEAD")
    else:
        return ""
    pass

def MeleeGetCrippledTimerMessage(whichPlayer:"player")->"string":
    r = GetPlayerRace(whichPlayer)
    if ( r == RACE_HUMAN ):
        return GetLocalizedString("CRIPPLE_TIMER_HUMAN")
    elif ( r == RACE_ORC ):
        return GetLocalizedString("CRIPPLE_TIMER_ORC")
    elif ( r == RACE_NIGHTELF ):
        return GetLocalizedString("CRIPPLE_TIMER_NIGHTELF")
    elif ( r == RACE_UNDEAD ):
        return GetLocalizedString("CRIPPLE_TIMER_UNDEAD")
    else:
        return ""
    pass

def MeleeGetCrippledRevealedMessage(whichPlayer:"player")->"string":
    return GetLocalizedString("CRIPPLE_REVEALING_PREFIX") + GetPlayerName(whichPlayer) + GetLocalizedString("CRIPPLE_REVEALING_POSTFIX")
    pass

def MeleeExposePlayer(whichPlayer:"player", expose:"boolean")->"nothing":
    playerIndex = None
    indexPlayer = None
    toExposeTo = CreateForce()
    CripplePlayer(whichPlayer, toExposeTo, False)
    bj_playerIsExposed[GetPlayerId(whichPlayer)] = expose
    playerIndex = 0
    while True:
        indexPlayer = Player(playerIndex)
        if ( not  PlayersAreCoAllied(whichPlayer, indexPlayer) ):
            ForceAddPlayer(toExposeTo, indexPlayer)
        playerIndex = playerIndex + 1
        if playerIndex == bj_MAX_PLAYERS:
            break
        pass

    CripplePlayer(whichPlayer, toExposeTo, expose)
    DestroyForce(toExposeTo)
    pass

def MeleeExposeAllPlayers()->"nothing":
    playerIndex = None
    indexPlayer = None
    playerIndex2 = None
    indexPlayer2 = None
    toExposeTo = CreateForce()
    playerIndex = 0
    while True:
        indexPlayer = Player(playerIndex)
        ForceClear(toExposeTo)
        CripplePlayer(indexPlayer, toExposeTo, False)
        playerIndex2 = 0
        while True:
            indexPlayer2 = Player(playerIndex2)
            if playerIndex != playerIndex2:
                if ( not  PlayersAreCoAllied(indexPlayer, indexPlayer2) ):
                    ForceAddPlayer(toExposeTo, indexPlayer2)
            playerIndex2 = playerIndex2 + 1
            if playerIndex2 == bj_MAX_PLAYERS:
                break
            pass

        CripplePlayer(indexPlayer, toExposeTo, True)
        playerIndex = playerIndex + 1
        if playerIndex == bj_MAX_PLAYERS:
            break
        pass

    DestroyForce(toExposeTo)
    pass

def MeleeCrippledPlayerTimeout()->"nothing":
    expiredTimer = GetExpiredTimer()
    playerIndex = None
    exposedPlayer = None
    playerIndex = 0
    while True:
        if ( bj_crippledTimer[playerIndex] == expiredTimer ):
            if True:
                break
        playerIndex = playerIndex + 1
        if playerIndex == bj_MAX_PLAYERS:
            break
        pass

    if ( playerIndex == bj_MAX_PLAYERS ):
        pass

    exposedPlayer = Player(playerIndex)
    if ( GetLocalPlayer() == exposedPlayer ):
        TimerDialogDisplay(bj_crippledTimerWindows[playerIndex], False)
    DisplayTimedTextToPlayer(GetLocalPlayer(), 0, 0, bj_MELEE_CRIPPLE_MSG_DURATION, MeleeGetCrippledRevealedMessage(exposedPlayer))
    MeleeExposePlayer(exposedPlayer, True)
    pass

def MeleePlayerIsCrippled(whichPlayer:"player")->"boolean":
    allyStructures = MeleeGetAllyStructureCount(whichPlayer)
    allyKeyStructures = MeleeGetAllyKeyStructureCount(whichPlayer)
    return ( allyStructures > 0 ) and ( allyKeyStructures <= 0 )
    pass

def MeleeCheckForCrippledPlayers()->"nothing":
    playerIndex = None
    indexPlayer = None
    crippledPlayers = CreateForce()
    isNowCrippled = None
    indexRace = None
    if bj_finishSoonAllExposed:
        pass

    playerIndex = 0
    while True:
        indexPlayer = Player(playerIndex)
        isNowCrippled = MeleePlayerIsCrippled(indexPlayer)
        if ( not  bj_playerIsCrippled[playerIndex] and isNowCrippled ):
            bj_playerIsCrippled[playerIndex] = True
            TimerStart(bj_crippledTimer[playerIndex], bj_MELEE_CRIPPLE_TIMEOUT, False, MeleeCrippledPlayerTimeout)
            if ( GetLocalPlayer() == indexPlayer ):
                TimerDialogDisplay(bj_crippledTimerWindows[playerIndex], True)
                DisplayTimedTextToPlayer(indexPlayer, 0, 0, bj_MELEE_CRIPPLE_MSG_DURATION, MeleeGetCrippledWarningMessage(indexPlayer))
        elif ( bj_playerIsCrippled[playerIndex] and not  isNowCrippled ):
            bj_playerIsCrippled[playerIndex] = False
            PauseTimer(bj_crippledTimer[playerIndex])
            if ( GetLocalPlayer() == indexPlayer ):
                TimerDialogDisplay(bj_crippledTimerWindows[playerIndex], False)
                if ( MeleeGetAllyStructureCount(indexPlayer) > 0 ):
                    if ( bj_playerIsExposed[playerIndex] ):
                        DisplayTimedTextToPlayer(indexPlayer, 0, 0, bj_MELEE_CRIPPLE_MSG_DURATION, GetLocalizedString("CRIPPLE_UNREVEALED"))
                    else:
                        DisplayTimedTextToPlayer(indexPlayer, 0, 0, bj_MELEE_CRIPPLE_MSG_DURATION, GetLocalizedString("CRIPPLE_UNCRIPPLED"))
            MeleeExposePlayer(indexPlayer, False)
        playerIndex = playerIndex + 1
        if playerIndex == bj_MAX_PLAYERS:
            break
        pass

    pass

def MeleeCheckLostUnit(lostUnit:"unit")->"nothing":
    lostUnitOwner = GetOwningPlayer(lostUnit)
    if ( GetPlayerStructureCount(lostUnitOwner, True) <= 0 ):
        MeleeCheckForLosersAndVictors()
    MeleeCheckForCrippledPlayers()
    pass

def MeleeCheckAddedUnit(addedUnit:"unit")->"nothing":
    addedUnitOwner = GetOwningPlayer(addedUnit)
    if ( bj_playerIsCrippled[GetPlayerId(addedUnitOwner)] ):
        MeleeCheckForCrippledPlayers()
    pass

def MeleeTriggerActionConstructCancel()->"nothing":
    MeleeCheckLostUnit(GetCancelledStructure())
    pass

def MeleeTriggerActionUnitDeath()->"nothing":
    if ( IsUnitType(GetDyingUnit(), UNIT_TYPE_STRUCTURE) ):
        MeleeCheckLostUnit(GetDyingUnit())
    pass

def MeleeTriggerActionUnitConstructionStart()->"nothing":
    MeleeCheckAddedUnit(GetConstructingStructure())
    pass

def MeleeTriggerActionPlayerDefeated()->"nothing":
    thePlayer = GetTriggerPlayer()
    CachePlayerHeroData(thePlayer)
    if ( MeleeGetAllyCount(thePlayer) > 0 ):
        ShareEverythingWithTeam(thePlayer)
        if ( not  bj_meleeDefeated[GetPlayerId(thePlayer)] ):
            MeleeDoDefeat(thePlayer)
    else:
        MakeUnitsPassiveForTeam(thePlayer)
        if ( not  bj_meleeDefeated[GetPlayerId(thePlayer)] ):
            MeleeDoDefeat(thePlayer)
    MeleeCheckForLosersAndVictors()
    pass

def MeleeTriggerActionPlayerLeft()->"nothing":
    thePlayer = GetTriggerPlayer()
    if ( IsPlayerObserver(thePlayer) ):
        RemovePlayerPreserveUnitsBJ(thePlayer, PLAYER_GAME_RESULT_NEUTRAL, False)
    CachePlayerHeroData(thePlayer)
    if ( MeleeGetAllyCount(thePlayer) > 0 ):
        ShareEverythingWithTeam(thePlayer)
        MeleeDoLeave(thePlayer)
    else:
        MakeUnitsPassiveForTeam(thePlayer)
        MeleeDoLeave(thePlayer)
    MeleeCheckForLosersAndVictors()
    pass

def MeleeTriggerActionAllianceChange()->"nothing":
    MeleeCheckForLosersAndVictors()
    MeleeCheckForCrippledPlayers()
    pass

def MeleeTriggerTournamentFinishSoon()->"nothing":
    global bj_finishSoonAllExposed
    playerIndex = None
    indexPlayer = None
    timeRemaining = GetTournamentFinishSoonTimeRemaining()
    if not  bj_finishSoonAllExposed:
        bj_finishSoonAllExposed = True
        playerIndex = 0
        while True:
            indexPlayer = Player(playerIndex)
            if bj_playerIsCrippled[playerIndex]:
                bj_playerIsCrippled[playerIndex] = False
                PauseTimer(bj_crippledTimer[playerIndex])
                if ( GetLocalPlayer() == indexPlayer ):
                    TimerDialogDisplay(bj_crippledTimerWindows[playerIndex], False)
            playerIndex = playerIndex + 1
            if playerIndex == bj_MAX_PLAYERS:
                break
            pass

        MeleeExposeAllPlayers()
    TimerDialogDisplay(bj_finishSoonTimerDialog, True)
    TimerDialogSetRealTimeRemaining(bj_finishSoonTimerDialog, timeRemaining)
    pass

def MeleeWasUserPlayer(whichPlayer:"player")->"boolean":
    slotState = None
    if ( GetPlayerController(whichPlayer) != MAP_CONTROL_USER ):
        return False
    slotState = GetPlayerSlotState(whichPlayer)
    return ( slotState == PLAYER_SLOT_STATE_PLAYING or slotState == PLAYER_SLOT_STATE_LEFT )
    pass

def MeleeTournamentFinishNowRuleA(multiplier:"integer")->"nothing":
    global bj_meleeGameOver
    playerScore = [None]*8192
    teamScore = [None]*8192
    teamForce = [None]*8192
    teamCount = None
    index = None
    indexPlayer = None
    index2 = None
    indexPlayer2 = None
    bestTeam = None
    bestScore = None
    draw = None
    index = 0
    while True:
        indexPlayer = Player(index)
        if MeleeWasUserPlayer(indexPlayer):
            playerScore[index] = GetTournamentScore(indexPlayer)
            if playerScore[index] <= 0:
                playerScore[index] = 1
        else:
            playerScore[index] = 0
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    teamCount = 0
    index = 0
    while True:
        if playerScore[index] != 0:
            indexPlayer = Player(index)
            teamScore[teamCount] = 0
            teamForce[teamCount] = CreateForce()
            index2 = index
            while True:
                if playerScore[index2] != 0:
                    indexPlayer2 = Player(index2)
                    if PlayersAreCoAllied(indexPlayer, indexPlayer2):
                        teamScore[teamCount] = teamScore[teamCount] + playerScore[index2]
                        ForceAddPlayer(teamForce[teamCount], indexPlayer2)
                        playerScore[index2] = 0
                index2 = index2 + 1
                if index2 == bj_MAX_PLAYERS:
                    break
                pass

            teamCount = teamCount + 1
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    bj_meleeGameOver = True
    if teamCount != 0:
        bestTeam = - 1
        bestScore = - 1
        index = 0
        while True:
            if teamScore[index] > bestScore:
                bestTeam = index
                bestScore = teamScore[index]
            index = index + 1
            if index == teamCount:
                break
            pass

        draw = False
        index = 0
        while True:
            if index != bestTeam:
                if bestScore < ( multiplier * teamScore[index] ):
                    draw = True
            index = index + 1
            if index == teamCount:
                break
            pass

        if draw:
            index = 0
            while True:
                ForForce(teamForce[index], MeleeDoDrawEnum)
                index = index + 1
                if index == teamCount:
                    break
                pass

        else:
            index = 0
            while True:
                if index != bestTeam:
                    ForForce(teamForce[index], MeleeDoDefeatEnum)
                index = index + 1
                if index == teamCount:
                    break
                pass

            ForForce(teamForce[bestTeam], MeleeDoVictoryEnum)
    pass

def MeleeTriggerTournamentFinishNow()->"nothing":
    rule = GetTournamentFinishNowRule()
    if bj_meleeGameOver:
        pass

    if ( rule == 1 ):
        MeleeTournamentFinishNowRuleA(1)
    else:
        MeleeTournamentFinishNowRuleA(3)
    MeleeRemoveObservers()
    pass

def MeleeInitVictoryDefeat()->"nothing":
    global bj_finishSoonTimerDialog
    trig = None
    index = None
    indexPlayer = None
    bj_finishSoonTimerDialog = CreateTimerDialog(None)
    trig = CreateTrigger()
    TriggerRegisterGameEvent(trig, EVENT_GAME_TOURNAMENT_FINISH_SOON)
    TriggerAddAction(trig, MeleeTriggerTournamentFinishSoon)
    trig = CreateTrigger()
    TriggerRegisterGameEvent(trig, EVENT_GAME_TOURNAMENT_FINISH_NOW)
    TriggerAddAction(trig, MeleeTriggerTournamentFinishNow)
    index = 0
    while True:
        indexPlayer = Player(index)
        if ( GetPlayerSlotState(indexPlayer) == PLAYER_SLOT_STATE_PLAYING ):
            bj_meleeDefeated[index] = False
            bj_meleeVictoried[index] = False
            bj_playerIsCrippled[index] = False
            bj_playerIsExposed[index] = False
            bj_crippledTimer[index] = CreateTimer()
            bj_crippledTimerWindows[index] = CreateTimerDialog(bj_crippledTimer[index])
            TimerDialogSetTitle(bj_crippledTimerWindows[index], MeleeGetCrippledTimerMessage(indexPlayer))
            trig = CreateTrigger()
            TriggerRegisterPlayerUnitEvent(trig, indexPlayer, EVENT_PLAYER_UNIT_CONSTRUCT_CANCEL, None)
            TriggerAddAction(trig, MeleeTriggerActionConstructCancel)
            trig = CreateTrigger()
            TriggerRegisterPlayerUnitEvent(trig, indexPlayer, EVENT_PLAYER_UNIT_DEATH, None)
            TriggerAddAction(trig, MeleeTriggerActionUnitDeath)
            trig = CreateTrigger()
            TriggerRegisterPlayerUnitEvent(trig, indexPlayer, EVENT_PLAYER_UNIT_CONSTRUCT_START, None)
            TriggerAddAction(trig, MeleeTriggerActionUnitConstructionStart)
            trig = CreateTrigger()
            TriggerRegisterPlayerEvent(trig, indexPlayer, EVENT_PLAYER_DEFEAT)
            TriggerAddAction(trig, MeleeTriggerActionPlayerDefeated)
            trig = CreateTrigger()
            TriggerRegisterPlayerEvent(trig, indexPlayer, EVENT_PLAYER_LEAVE)
            TriggerAddAction(trig, MeleeTriggerActionPlayerLeft)
            trig = CreateTrigger()
            TriggerRegisterPlayerAllianceChange(trig, indexPlayer, ALLIANCE_PASSIVE)
            TriggerRegisterPlayerStateEvent(trig, indexPlayer, PLAYER_STATE_ALLIED_VICTORY, EQUAL, 1)
            TriggerAddAction(trig, MeleeTriggerActionAllianceChange)
        else:
            bj_meleeDefeated[index] = True
            bj_meleeVictoried[index] = False
            if ( IsPlayerObserver(indexPlayer) ):
                trig = CreateTrigger()
                TriggerRegisterPlayerEvent(trig, indexPlayer, EVENT_PLAYER_LEAVE)
                TriggerAddAction(trig, MeleeTriggerActionPlayerLeft)
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    TimerStart(CreateTimer(), 2.0, False, MeleeTriggerActionAllianceChange)
    pass

def CheckInitPlayerSlotAvailability()->"nothing":
    global bj_slotControlReady
    index = None
    if ( not  bj_slotControlReady ):
        index = 0
        while True:
            bj_slotControlUsed[index] = False
            bj_slotControl[index] = MAP_CONTROL_USER
            index = index + 1
            if index == bj_MAX_PLAYERS:
                break
            pass

        bj_slotControlReady = True
    pass

def SetPlayerSlotAvailable(whichPlayer:"player", control:"mapcontrol")->"nothing":
    playerIndex = GetPlayerId(whichPlayer)
    CheckInitPlayerSlotAvailability()
    bj_slotControlUsed[playerIndex] = True
    bj_slotControl[playerIndex] = control
    pass

def TeamInitPlayerSlots(teamCount:"integer")->"nothing":
    index = None
    indexPlayer = None
    team = None
    SetTeams(teamCount)
    CheckInitPlayerSlotAvailability()
    index = 0
    team = 0
    while True:
        if ( bj_slotControlUsed[index] ):
            indexPlayer = Player(index)
            SetPlayerTeam(indexPlayer, team)
            team = team + 1
            if ( team >= teamCount ):
                team = 0
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    pass

def MeleeInitPlayerSlots()->"nothing":
    TeamInitPlayerSlots(bj_MAX_PLAYERS)
    pass

def FFAInitPlayerSlots()->"nothing":
    TeamInitPlayerSlots(bj_MAX_PLAYERS)
    pass

def OneOnOneInitPlayerSlots()->"nothing":
    SetTeams(2)
    SetPlayers(2)
    TeamInitPlayerSlots(2)
    pass

def InitGenericPlayerSlots()->"nothing":
    gType = GetGameTypeSelected()
    if ( gType == GAME_TYPE_MELEE ):
        MeleeInitPlayerSlots()
    elif ( gType == GAME_TYPE_FFA ):
        FFAInitPlayerSlots()
    elif ( gType == GAME_TYPE_ONE_ON_ONE ):
        OneOnOneInitPlayerSlots()
    elif ( gType == GAME_TYPE_TWO_TEAM_PLAY ):
        TeamInitPlayerSlots(2)
    elif ( gType == GAME_TYPE_THREE_TEAM_PLAY ):
        TeamInitPlayerSlots(3)
    elif ( gType == GAME_TYPE_FOUR_TEAM_PLAY ):
        TeamInitPlayerSlots(4)
    pass

def SetDNCSoundsDawn()->"nothing":
    if bj_useDawnDuskSounds:
        StartSound(bj_dawnSound)
    pass

def SetDNCSoundsDusk()->"nothing":
    if bj_useDawnDuskSounds:
        StartSound(bj_duskSound)
    pass

def SetDNCSoundsDay()->"nothing":
    global bj_dncIsDaytime
    ToD = GetTimeOfDay()
    if ( ToD >= bj_TOD_DAWN and ToD < bj_TOD_DUSK ) and not  bj_dncIsDaytime:
        bj_dncIsDaytime = True
        StopSound(bj_nightAmbientSound, False, True)
        StartSound(bj_dayAmbientSound)
    pass

def SetDNCSoundsNight()->"nothing":
    global bj_dncIsDaytime
    ToD = GetTimeOfDay()
    if ( ToD < bj_TOD_DAWN or ToD >= bj_TOD_DUSK ) and bj_dncIsDaytime:
        bj_dncIsDaytime = False
        StopSound(bj_dayAmbientSound, False, True)
        StartSound(bj_nightAmbientSound)
    pass

def InitDNCSounds()->"nothing":
    global bj_dncSoundsDawn
    global bj_dncSoundsDusk
    global bj_duskSound
    global bj_dncSoundsNight
    global bj_dncSoundsDay
    global bj_dawnSound
    bj_dawnSound = CreateSoundFromLabel("RoosterSound", False, False, False, 10000, 10000)
    bj_duskSound = CreateSoundFromLabel("WolfSound", False, False, False, 10000, 10000)
    bj_dncSoundsDawn = CreateTrigger()
    TriggerRegisterGameStateEvent(bj_dncSoundsDawn, GAME_STATE_TIME_OF_DAY, EQUAL, bj_TOD_DAWN)
    TriggerAddAction(bj_dncSoundsDawn, SetDNCSoundsDawn)
    bj_dncSoundsDusk = CreateTrigger()
    TriggerRegisterGameStateEvent(bj_dncSoundsDusk, GAME_STATE_TIME_OF_DAY, EQUAL, bj_TOD_DUSK)
    TriggerAddAction(bj_dncSoundsDusk, SetDNCSoundsDusk)
    bj_dncSoundsDay = CreateTrigger()
    TriggerRegisterGameStateEvent(bj_dncSoundsDay, GAME_STATE_TIME_OF_DAY, GREATER_THAN_OR_EQUAL, bj_TOD_DAWN)
    TriggerRegisterGameStateEvent(bj_dncSoundsDay, GAME_STATE_TIME_OF_DAY, LESS_THAN, bj_TOD_DUSK)
    TriggerAddAction(bj_dncSoundsDay, SetDNCSoundsDay)
    bj_dncSoundsNight = CreateTrigger()
    TriggerRegisterGameStateEvent(bj_dncSoundsNight, GAME_STATE_TIME_OF_DAY, LESS_THAN, bj_TOD_DAWN)
    TriggerRegisterGameStateEvent(bj_dncSoundsNight, GAME_STATE_TIME_OF_DAY, GREATER_THAN_OR_EQUAL, bj_TOD_DUSK)
    TriggerAddAction(bj_dncSoundsNight, SetDNCSoundsNight)
    pass

def InitBlizzardGlobals()->"nothing":
    global filterEnumDestructablesInCircleBJ
    global bj_questSecretSound
    global filterMeleeTrainedUnitIsHeroBJ
    global bj_cineModePriorMaskSetting
    global bj_cineModePriorSpeed
    global bj_cineModePriorFogSetting
    global bj_questWarningSound
    global filterGetUnitsInRectOfPlayer
    global filterGetUnitsOfTypeIdAll
    global bj_isSinglePlayer
    global bj_questItemAcquiredSound
    global bj_MELEE_MAX_TWINKED_HEROES
    global bj_defeatDialogSound
    global bj_victoryDialogSound
    global filterGetUnitsOfPlayerAndTypeId
    global filterLivingPlayerUnitsOfTypeId
    global bj_FORCE_ALL_PLAYERS
    global filterIssueHauntOrderAtLocBJ
    global bj_questHintSound
    global bj_questCompletedSound
    global bj_questUpdatedSound
    global bj_rescueSound
    global bj_questFailedSound
    global bj_questDiscoveredSound
    index = None
    userControlledPlayers = None
    v = None
    filterIssueHauntOrderAtLocBJ = Filter(IssueHauntOrderAtLocBJFilter)
    filterEnumDestructablesInCircleBJ = Filter(EnumDestructablesInCircleBJFilter)
    filterGetUnitsInRectOfPlayer = Filter(GetUnitsInRectOfPlayerFilter)
    filterGetUnitsOfTypeIdAll = Filter(GetUnitsOfTypeIdAllFilter)
    filterGetUnitsOfPlayerAndTypeId = Filter(GetUnitsOfPlayerAndTypeIdFilter)
    filterMeleeTrainedUnitIsHeroBJ = Filter(MeleeTrainedUnitIsHeroBJFilter)
    filterLivingPlayerUnitsOfTypeId = Filter(LivingPlayerUnitsOfTypeIdFilter)
    index = 0
    while True:
        if index == bj_MAX_PLAYER_SLOTS:
            break
        bj_FORCE_PLAYER[index] = CreateForce()
        ForceAddPlayer(bj_FORCE_PLAYER[index], Player(index))
        index = index + 1
        pass

    bj_FORCE_ALL_PLAYERS = CreateForce()
    ForceEnumPlayers(bj_FORCE_ALL_PLAYERS, None)
    bj_cineModePriorSpeed = GetGameSpeed()
    bj_cineModePriorFogSetting = IsFogEnabled()
    bj_cineModePriorMaskSetting = IsFogMaskEnabled()
    index = 0
    while True:
        if index >= bj_MAX_QUEUED_TRIGGERS:
            break
        bj_queuedExecTriggers[index] = None
        bj_queuedExecUseConds[index] = False
        index = index + 1
        pass

    bj_isSinglePlayer = False
    userControlledPlayers = 0
    index = 0
    while True:
        if index >= bj_MAX_PLAYERS:
            break
        if ( GetPlayerController(Player(index)) == MAP_CONTROL_USER and GetPlayerSlotState(Player(index)) == PLAYER_SLOT_STATE_PLAYING ):
            userControlledPlayers = userControlledPlayers + 1
        index = index + 1
        pass

    bj_isSinglePlayer = ( userControlledPlayers == 1 )
    bj_rescueSound = CreateSoundFromLabel("Rescue", False, False, False, 10000, 10000)
    bj_questDiscoveredSound = CreateSoundFromLabel("QuestNew", False, False, False, 10000, 10000)
    bj_questUpdatedSound = CreateSoundFromLabel("QuestUpdate", False, False, False, 10000, 10000)
    bj_questCompletedSound = CreateSoundFromLabel("QuestCompleted", False, False, False, 10000, 10000)
    bj_questFailedSound = CreateSoundFromLabel("QuestFailed", False, False, False, 10000, 10000)
    bj_questHintSound = CreateSoundFromLabel("Hint", False, False, False, 10000, 10000)
    bj_questSecretSound = CreateSoundFromLabel("SecretFound", False, False, False, 10000, 10000)
    bj_questItemAcquiredSound = CreateSoundFromLabel("ItemReward", False, False, False, 10000, 10000)
    bj_questWarningSound = CreateSoundFromLabel("Warning", False, False, False, 10000, 10000)
    bj_victoryDialogSound = CreateSoundFromLabel("QuestCompleted", False, False, False, 10000, 10000)
    bj_defeatDialogSound = CreateSoundFromLabel("QuestFailed", False, False, False, 10000, 10000)
    DelayedSuspendDecayCreate()
    v = VersionGet()
    if ( v == VERSION_REIGN_OF_CHAOS ):
        bj_MELEE_MAX_TWINKED_HEROES = bj_MELEE_MAX_TWINKED_HEROES_V0
    else:
        bj_MELEE_MAX_TWINKED_HEROES = bj_MELEE_MAX_TWINKED_HEROES_V1
    pass

def InitQueuedTriggers()->"nothing":
    global bj_queuedExecTimeout
    bj_queuedExecTimeout = CreateTrigger()
    TriggerRegisterTimerExpireEvent(bj_queuedExecTimeout, bj_queuedExecTimeoutTimer)
    TriggerAddAction(bj_queuedExecTimeout, QueuedTriggerDoneBJ)
    pass

def InitMapRects()->"nothing":
    global bj_mapInitialPlayableArea
    global bj_mapInitialCameraBounds
    bj_mapInitialPlayableArea = Rect(GetCameraBoundMinX() - GetCameraMargin(CAMERA_MARGIN_LEFT), GetCameraBoundMinY() - GetCameraMargin(CAMERA_MARGIN_BOTTOM), GetCameraBoundMaxX() + GetCameraMargin(CAMERA_MARGIN_RIGHT), GetCameraBoundMaxY() + GetCameraMargin(CAMERA_MARGIN_TOP))
    bj_mapInitialCameraBounds = GetCurrentCameraBoundsMapRectBJ()
    pass

def InitSummonableCaps()->"nothing":
    index = None
    index = 0
    while True:
        if ( not  GetPlayerTechResearched(Player(index), 1382576756, True) ):
            SetPlayerTechMaxAllowed(Player(index), 1752331380, 0)
        if ( not  GetPlayerTechResearched(Player(index), 1383031403, True) ):
            SetPlayerTechMaxAllowed(Player(index), 1869898347, 0)
        SetPlayerTechMaxAllowed(Player(index), 1970498405, bj_MAX_SKELETONS)
        index = index + 1
        if index == bj_MAX_PLAYERS:
            break
        pass

    pass

def UpdateStockAvailability(whichItem:"item")->"nothing":
    iType = GetItemType(whichItem)
    iLevel = GetItemLevel(whichItem)
    if ( iType == ITEM_TYPE_PERMANENT ):
        bj_stockAllowedPermanent[iLevel] = True
    elif ( iType == ITEM_TYPE_CHARGED ):
        bj_stockAllowedCharged[iLevel] = True
    elif ( iType == ITEM_TYPE_ARTIFACT ):
        bj_stockAllowedArtifact[iLevel] = True
    pass

def UpdateEachStockBuildingEnum()->"nothing":
    iteration = 0
    pickedItemId = None
    while True:
        pickedItemId = ChooseRandomItemEx(bj_stockPickedItemType, bj_stockPickedItemLevel)
        if IsItemIdSellable(pickedItemId):
            break
        iteration = iteration + 1
        if ( iteration > bj_STOCK_MAX_ITERATIONS ):
            pass

        pass

    AddItemToStock(GetEnumUnit(), pickedItemId, 1, 1)
    pass

def UpdateEachStockBuilding(iType:"itemtype", iLevel:"integer")->"nothing":
    global bj_stockPickedItemLevel
    global bj_stockPickedItemType
    g = None
    bj_stockPickedItemType = iType
    bj_stockPickedItemLevel = iLevel
    g = CreateGroup()
    GroupEnumUnitsOfType(g, "marketplace", None)
    ForGroup(g, UpdateEachStockBuildingEnum)
    DestroyGroup(g)
    pass

def PerformStockUpdates()->"nothing":
    pickedItemId = None
    pickedItemType = None
    pickedItemLevel = 0
    allowedCombinations = 0
    iLevel = None
    iLevel = 1
    while True:
        if ( bj_stockAllowedPermanent[iLevel] ):
            allowedCombinations = allowedCombinations + 1
            if ( GetRandomInt(1, allowedCombinations) == 1 ):
                pickedItemType = ITEM_TYPE_PERMANENT
                pickedItemLevel = iLevel
        if ( bj_stockAllowedCharged[iLevel] ):
            allowedCombinations = allowedCombinations + 1
            if ( GetRandomInt(1, allowedCombinations) == 1 ):
                pickedItemType = ITEM_TYPE_CHARGED
                pickedItemLevel = iLevel
        if ( bj_stockAllowedArtifact[iLevel] ):
            allowedCombinations = allowedCombinations + 1
            if ( GetRandomInt(1, allowedCombinations) == 1 ):
                pickedItemType = ITEM_TYPE_ARTIFACT
                pickedItemLevel = iLevel
        iLevel = iLevel + 1
        if iLevel > bj_MAX_ITEM_LEVEL:
            break
        pass

    if ( allowedCombinations == 0 ):
        pass

    UpdateEachStockBuilding(pickedItemType, pickedItemLevel)
    pass

def StartStockUpdates()->"nothing":
    PerformStockUpdates()
    TimerStart(bj_stockUpdateTimer, bj_STOCK_RESTOCK_INTERVAL, True, PerformStockUpdates)
    pass

def RemovePurchasedItem()->"nothing":
    RemoveItemFromStock(GetSellingUnit(), GetItemTypeId(GetSoldItem()))
    pass

def InitNeutralBuildings()->"nothing":
    global bj_stockUpdateTimer
    global bj_stockItemPurchased
    iLevel = None
    iLevel = 0
    while True:
        bj_stockAllowedPermanent[iLevel] = False
        bj_stockAllowedCharged[iLevel] = False
        bj_stockAllowedArtifact[iLevel] = False
        iLevel = iLevel + 1
        if iLevel > bj_MAX_ITEM_LEVEL:
            break
        pass

    SetAllItemTypeSlots(bj_MAX_STOCK_ITEM_SLOTS)
    SetAllUnitTypeSlots(bj_MAX_STOCK_UNIT_SLOTS)
    bj_stockUpdateTimer = CreateTimer()
    TimerStart(bj_stockUpdateTimer, bj_STOCK_RESTOCK_INITIAL_DELAY, False, StartStockUpdates)
    bj_stockItemPurchased = CreateTrigger()
    TriggerRegisterPlayerUnitEvent(bj_stockItemPurchased, Player(PLAYER_NEUTRAL_PASSIVE), EVENT_PLAYER_UNIT_SELL_ITEM, None)
    TriggerAddAction(bj_stockItemPurchased, RemovePurchasedItem)
    pass

def MarkGameStarted()->"nothing":
    global bj_gameStarted
    bj_gameStarted = True
    DestroyTimer(bj_gameStartedTimer)
    pass

def DetectGameStarted()->"nothing":
    global bj_gameStartedTimer
    bj_gameStartedTimer = CreateTimer()
    TimerStart(bj_gameStartedTimer, bj_GAME_STARTED_THRESHOLD, False, MarkGameStarted)
    pass

def InitBlizzard()->"nothing":
    ConfigureNeutralVictim()
    InitBlizzardGlobals()
    InitQueuedTriggers()
    InitRescuableBehaviorBJ()
    InitDNCSounds()
    InitMapRects()
    InitSummonableCaps()
    InitNeutralBuildings()
    DetectGameStarted()
    pass

def RandomDistReset()->"nothing":
    global bj_randDistCount
    bj_randDistCount = 0
    pass

def RandomDistAddItem(inID:"integer", inChance:"integer")->"nothing":
    global bj_randDistCount
    bj_randDistID[bj_randDistCount] = inID
    bj_randDistChance[bj_randDistCount] = inChance
    bj_randDistCount = bj_randDistCount + 1
    pass

def RandomDistChoose()->"integer":
    sum = 0
    chance = 0
    index = None
    foundID = - 1
    done = None
    if ( bj_randDistCount == 0 ):
        return - 1
    index = 0
    while True:
        sum = sum + bj_randDistChance[index]
        index = index + 1
        if index == bj_randDistCount:
            break
        pass

    chance = GetRandomInt(1, sum)
    index = 0
    sum = 0
    done = False
    while True:
        sum = sum + bj_randDistChance[index]
        if ( chance <= sum ):
            foundID = bj_randDistID[index]
            done = True
        index = index + 1
        if ( index == bj_randDistCount ):
            done = True
        if done == True:
            break
        pass

    return foundID
    pass

def UnitDropItem(inUnit:"unit", inItemID:"integer")->"item":
    x = None
    y = None
    radius = 32
    unitX = None
    unitY = None
    droppedItem = None
    if ( inItemID == - 1 ):
        return None
    unitX = GetUnitX(inUnit)
    unitY = GetUnitY(inUnit)
    x = GetRandomReal(unitX - radius, unitX + radius)
    y = GetRandomReal(unitY - radius, unitY + radius)
    droppedItem = CreateItem(inItemID, x, y)
    SetItemDropID(droppedItem, GetUnitTypeId(inUnit))
    UpdateStockAvailability(droppedItem)
    return droppedItem
    pass

def WidgetDropItem(inWidget:"widget", inItemID:"integer")->"item":
    x = None
    y = None
    radius = 32
    widgetX = None
    widgetY = None
    if ( inItemID == - 1 ):
        return None
    widgetX = GetWidgetX(inWidget)
    widgetY = GetWidgetY(inWidget)
    x = GetRandomReal(widgetX - radius, widgetX + radius)
    y = GetRandomReal(widgetY - radius, widgetY + radius)
    return CreateItem(inItemID, x, y)
    pass

