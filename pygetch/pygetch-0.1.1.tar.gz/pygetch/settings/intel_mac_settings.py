"""
"""

from ..utils.bidict import convert_to_bidict

# FROM:
#   - MacBook Air
#   - ascii / utf-8

####################################
# ANSI
ANSI_ARROW_KEYS = {
    (27, 91, 65): "UP",
    (27, 91, 66): "DOWN",
    (27, 91, 67): "RIGHT",
    (27, 91, 68): "LEFT",
}

ANSI_CONTROL_ARROWS = {
    (27, 91, 53, 68): "CTRL-LEFT",
    (27, 91, 53, 67): "CTRL-RIGHT",
}

ANSI_OPTION_ARROWS = {
    (27,98): "OPT-LEFT",
    (27,102): "OPT-RIGHT",
}

ANSI_FN_SHIFT_ARROWS = {
    (27, 91, 53, 126): "FN-SHIFT-UP",
    (27, 91, 54, 126): "FN-SHIFT-DOWN",
    (27, 91, 72):      "FN-SHIFT-LEFT",
    (27, 91, 70):      "FN-SHIFT-RIGHT",
}

ANSI_F1_F4 = {
    (27, 79, 80): 'F1',
    (27, 79, 81): 'F2',
    (27, 79, 82): 'F3',
    (27, 79, 83): 'F4',
}

ANSI_F5_F12 = {
    (27, 91, 49, 53, 126): 'F5',
    (27, 91, 49, 55, 126): 'F6',
    (27, 91, 49, 56, 126): 'F7',
    (27, 91, 49, 57, 126): 'F8',
    (27, 91, 50, 48, 126): 'F9',
    (27, 91, 50, 49, 126): 'F10',
    (27, 91, 50, 51, 126): 'F11',
    (27, 91, 50, 52, 126): 'F12',
}

ANSI_FN_SHIFT_F5_12 = {
    (27, 91, 50, 53, 126): "FN-SHIFT-F5",
    (27, 91, 50, 54, 126): "FN-SHIFT-F6",
    (27, 91, 50, 56, 126): "FN-SHIFT-F7",
    (27, 91, 50, 57, 126): "FN-SHIFT-F8",
    (27, 91, 51, 49, 126): "FN-SHIFT-F9",
    (27, 91, 50, 50, 126): "FN-SHIFT-F10",
    (27, 91, 51, 51, 126): "FN-SHIFT-F11",
    (27, 91, 51, 52, 126): "FN-SHIFT-F12",
}

ANSI_FN_MISC = {
    (27, 91, 51, 126): "FN-DEL / forward delete",
}

# for iteration
ALL_ANSI_GROUPS = [
    ANSI_ARROW_KEYS,
    ANSI_CONTROL_ARROWS,
    ANSI_OPTION_ARROWS,
    ANSI_FN_SHIFT_ARROWS,
    ANSI_F1_F4,
    ANSI_F5_F12,
    ANSI_FN_SHIFT_F5_12,
    ANSI_FN_MISC,
]

ALL_ANSI_GROUPS = [convert_to_bidict(d) for d in ALL_ANSI_GROUPS]

ANSI = {}
for group in ALL_ANSI_GROUPS:
    ANSI.update(group)


####################################
# singletons

# special/control
ASCII_CONTROL = {
    (0,): 'NUL',
    (1,): 'SOH',
    (2,): 'STX',
    (3,): 'ETX',
    (4,): 'EOT',
    (5,): 'ENQ',
    (6,): 'ACK',
    (7,): 'BEL',
    (8,): 'BS',
    (9,): 'TAB',
    (10,): 'LF',
    (11,): 'VT',
    (12,): 'FF',
    (13,): 'CR',
    (14,): 'SO',
    (15,): 'SI',
    (16,): 'DLE',
    (17,): 'DC1',
    (18,): 'DC2',
    (19,): 'DC3',
    (20,): 'DC4',
    (21,): 'NAK',
    (22,): 'SYN',
    (23,): 'ETB',
    (24,): 'CAN',
    (25,): 'EM',
    (26,): 'SUB',
    (27,): 'ESC',
    (28,): 'FS',
    (29,): 'GS',
    (30,): 'RS',
    (31,): 'US',

    (127,): 'DEL',
}

ASCII_MISC = {
    (32,): ' ',
    (33,): '!',
    (34,): '"',
    (35,): '#',
    (36,): '$',
    (37,): '%',
    (38,): '&',
    (39,): '\'',
    (40,): '(',
    (41,): ')',
    (42,): '*',
    (43,): '+',
    (44,): ',',
    (45,): '-',
    (46,): '.',
    (47,): '/',
    (48,): '0',
    (49,): '1',
    (50,): '2',
    (51,): '3',
    (52,): '4',
    (53,): '5',
    (54,): '6',
    (55,): '7',
    (56,): '8',
    (57,): '9',
    (58,): ':',
    (59,): ';',
    (60,): '<',
    (61,): '=',
    (62,): '>',
    (63,): '?',
    (64,): '@',

    (91,): '[',
    (92,): '\\',
    (93,): ']',
    (94,): '^',    
    (95,): '_',
    (96,): '`',

    (123,): '{',
    (124,): '|',
    (125,): '}',
    (126,): '~',
}

ASCII_UPPERCASE = {
    (65,): 'A',
    (66,): 'B',
    (67,): 'C',
    (68,): 'D',
    (69,): 'E',
    (70,): 'F',
    (71,): 'G',
    (72,): 'H',
    (73,): 'I',
    (74,): 'J',
    (75,): 'K',
    (76,): 'L',
    (77,): 'M',
    (78,): 'N',
    (79,): 'O',
    (80,): 'P',
    (81,): 'Q',
    (82,): 'R',
    (83,): 'S',
    (84,): 'T',
    (85,): 'U',
    (86,): 'V',
    (87,): 'W',
    (88,): 'X',
    (89,): 'Y',
    (90,): 'Z',
}

ASCII_LOWERCASE = {
    (97,): 'a',
    (98,): 'b',
    (99,): 'c',
    (100,): 'd',
    (101,): 'e',
    (102,): 'f',
    (103,): 'g',
    (104,): 'h',
    (105,): 'i',
    (106,): 'j',
    (107,): 'k',
    (108,): 'l',
    (109,): 'm',
    (110,): 'n',
    (111,): 'o',
    (112,): 'p',
    (113,): 'q',
    (114,): 'r',
    (115,): 's',
    (116,): 't',
    (117,): 'u',
    (118,): 'v',
    (119,): 'w',
    (120,): 'x',
    (121,): 'y',
    (122,): 'z',
}

ALL_ASCII_GROUPS = [
    ASCII_CONTROL,
    ASCII_MISC,
    ASCII_UPPERCASE,
    ASCII_LOWERCASE,
]

ALL_ASCII_GROUPS = [convert_to_bidict(d) for d in ALL_ASCII_GROUPS]

ASCII = {}
for group in ALL_ASCII_GROUPS:
    ASCII.update(group)

####################################
# key mappings and ANSI

CONTROL_DICT = {
    'NUL': 'null',
    'SOH': 'start of heading',
    'STX': 'start of text',
    'ETX': 'end of text',
    'EOT': 'end of transmission',
    'ENQ': 'enquiry',
    'ACK': 'acknowledge',
    'BEL': 'bell',
    'BS' : 'backspace',
    'TAB': 'horizontal tab',
    'LF' : 'NL line feed, new line',
    'VT' : 'vertical tab',
    'FF' : 'form feed',
    'CR' : 'carriage return',
    'SO' : 'shift out',
    'SI' : 'shift in',
    'DLE': 'data link escape',
    'DC1': 'device control 1',
    'DC2': 'device control 2',
    'DC3': 'device control 3',
    'DC4': 'device control 4',
    'NAK': 'negative acknowledge',
    'SYN': 'synchronous idle',
    'ETB': 'end of transmission block',
    'CAN': 'cancel',
    'EM' : 'end of medium',
    'SUB': 'substitute',
    'ESC': 'escape',
    'FS' : 'file separator',
    'GS' : 'group separator',
    'RS' : 'record separator',
    'US' : 'unit separator',

    # 'HT' : 'horizontal tab (or TAB)',
    # 'NL' : 'new line (or LF, line feed)',
    # 'NP' : 'new page (or FF, form feed)',

    'DEL': 'delete ???',
}

####################################
# all keys

# (tuples of ints)
KEYS = {}
KEYS.update(ANSI)
KEYS.update(ASCII)

####################################
# common control characters
CONTROL_C       = chr(3)
BACKSPACE       = chr(8)
TAB             = chr(9)
NEWLINE         = chr(10)
CARRIAGE_RETURN = chr(13) # '\r'
ESC             = chr(27)
DEL             = chr(127)

####################################
# useful sets
WHITESPACE  = {TAB, NEWLINE, CARRIAGE_RETURN}  # not including <space>
ENTER_KEYS  = {CARRIAGE_RETURN, NEWLINE}
DELETE_KEYS = {DEL, BACKSPACE}
