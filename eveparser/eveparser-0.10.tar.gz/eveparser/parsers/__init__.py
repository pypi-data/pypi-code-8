"""
eveparser.parsers
~~~~~~~~~~~~~~~~
Contains all parser functions for various types of input from Eve Online.

"""

from eveparser.parsers.assets import parse_assets
from eveparser.parsers.cargo_scan import parse_cargo_scan
from eveparser.parsers.chat import parse_chat
from eveparser.parsers.contract import parse_contract
from eveparser.parsers.dscan import parse_dscan
from eveparser.parsers.eft import parse_eft
from eveparser.parsers.fitting import parse_fitting
from eveparser.parsers.industry import parse_industry
from eveparser.parsers.killmail import parse_killmail
from eveparser.parsers.listing import parse_listing
from eveparser.parsers.loot_history import parse_loot_history
from eveparser.parsers.pi import parse_pi
from eveparser.parsers.survey_scanner import parse_survey_scanner
from eveparser.parsers.view_contents import parse_view_contents
from eveparser.parsers.wallet import parse_wallet

__all__ = [
    'parse_assets',
    'parse_cargo_scan',
    'parse_chat',
    'parse_contract',
    'parse_dscan',
    'parse_eft',
    'parse_fitting',
    'parse_industry',
    'parse_killmail',
    'parse_listing',
    'parse_loot_history',
    'parse_pi',
    'parse_survey_scanner',
    'parse_view_contents',
    'parse_wallet',
]
