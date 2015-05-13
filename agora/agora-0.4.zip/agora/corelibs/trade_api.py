###############################################################################
#
#   Agora Portfolio & Risk Management System
#
#   Copyright 2015 Carlo Sbraccia
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
###############################################################################

from onyx.core import (Date, Structure, AddObj, GetObj, UpdateObj,
                       ObjDbTransaction, CreateInMemory, ObjDbQuery, ObjExists,
                       ObjNotFound, GetVal, SetVal)

from agora.corelibs.base36 import unique_id
from agora.corelibs.tradable_api import AddByInference
from agora.corelibs.transaction_api import CommitTransaction
from agora.system.ufo_trade import TradeError

import logging

__all__ = [
    "TradeError",
    "CommitTrade",
    "ChildrenByBook",
    "TradesBy",
]

LOG_FMT = "%(asctime)-15s %(levelname)-8s %(name)-38s %(message)s"

logging.basicConfig(level=logging.INFO, format=LOG_FMT)
logger = logging.getLogger(__name__)

# --- templates for common queries
QUERY_KIDSBYBOOK = """
SELECT Unit, SUM(Qty) AS tot_qty
FROM PosEffects WHERE Book=%s AND {0:s}<=%s
GROUP BY Unit;"""


# -----------------------------------------------------------------------------
def PreTradeCompliance(trade):
    """
    Description:
        This function is ment to raise an exception for any violation
        of pre-trade compliance checks.
    Inpots:
        trade - the trade to be checked
    Returns:
        None.
    """
    # --- price validation
    GetVal(trade, "MktValUSD")

    # --- basic risk validation
    GetVal(trade, "Deltas")


# -------------------------------------------------------------------------
def CommitTrade(trade):
    """
    Description:
        Create/amend a trade, taking care of updating all position effects.
    Inputs:
        trade - the instance of Trade to commit
    Returns:
        A Trade instance.
    """
    # --- clone security traded: AddByInference is needed to generate the
    #     proper ImpliedName.
    sec = AddByInference(GetObj(trade.SecurityTraded).clone())

    try:
        # --- reload security: this is needed to avoid basing decisions on
        #     attribute values that might have been set in memory
        trade = GetObj(trade.Name, refresh=True)

    except ObjNotFound:
        # --- trade not found, proceed as new trade
        trade.SecurityTraded = sec.Name

        # --- create trade and overwrite a few stored attributes
        trade_name = trade.format_name(Date.today(), unique_id(8))
        trade = CreateInMemory(trade.clone(name=trade_name))

        PreTradeCompliance(trade)

        logger.info("creating new trade {0:s}".format(trade.Name))

        calculated = GetVal(trade, "TransactionsCalc")
        with ObjDbTransaction("Trade Insert", level="SERIALIZABLE"):
            for transaction in calculated.values():
                CommitTransaction(transaction)
            AddObj(trade)

    else:
        info = GetVal(trade, "TradeInfo")
        info["SecurityTraded"] = sec.Name

        # --- need to amend?
        same = True
        for attr, value in info.items():
            same = (value == getattr(trade, attr))
            if not same:
                break
        if same:
            raise ValueError("TradeCommit, found "
                             "nothing to amend on existing trade.")

        logger.info("amending trade {0:s}".format(trade.Name))

        # --- overwrite trade stored attributes with new ones
        for attr, value in info.items():
            SetVal(trade, attr, value)

        PreTradeCompliance(trade)

        stored = GetVal(trade, "TransactionsStored")
        calculated = GetVal(trade, "TransactionsCalc")
        with ObjDbTransaction("Trade Amend", level="SERIALIZABLE"):
            for event, transaction in calculated.items():
                # --- overwrite the name of the calculated transaction with
                #     that of the stored one
                try:
                    transaction.Name = stored[event]
                except KeyError:
                    raise TradeError("Trying to amend a "
                                     "trade with an aged transaction")
                CommitTransaction(transaction)

    return trade


# -----------------------------------------------------------------------------
def ChildrenByBook(book, pos_date, by_time_created=False):
    """
    Description:
        Return all children of a given book as of a given date.
    Inputs:
        book            - the book
        pos_date        - the positions date
        by_time_created - if True, amendments are reflected on the date they
                          were booked, not on the date of the original trade.
    Returns:
        A Structure.
    """
    if by_time_created:
        query = QUERY_KIDSBYBOOK.format("TimeCreated")
    else:
        query = QUERY_KIDSBYBOOK.format("TradeDate")

    rows = ObjDbQuery(query, parms=(book, pos_date.eod()), attr="fetchall")
    children = Structure()
    for row in rows:
        # --- exclude children with zero quantity
        if row.tot_qty != 0.0:
            children[row.unit] = int(row.tot_qty)

    return children


# -----------------------------------------------------------------------------
def TradesBy(book=None, trader=None, security=None, date_range=None):
    """
    Description:
        Return all trades matching the given criteria.
    Inputs:
        book       - a given book
        trader     - a given trader
        security   - a given security
        date_range - a tuple of start and end date
    Returns:
        A list of trade names.
    """
    pass
