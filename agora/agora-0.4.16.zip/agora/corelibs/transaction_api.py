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

from onyx.core import (Date, ObjDbTransaction, AddObj, GetObj, UpdateObj,
                       PurgeObj, ObjDbQuery, ObjNotFound, GetVal,
                       TableSchema, ObjDbTable)

from agora.corelibs.base36 import unique_id
from agora.corelibs.tradable_api import AddByInference
from agora.system.ufo_transaction import (Transaction,
                                          TransactionError, TransactionWarning)

import logging

__all__ = [
    "CommitTransaction",
    "RollbackTransaction",
    "DeleteTransaction",
    "TransactionsBy"
]

LOG_FMT = "%(asctime)-15s %(levelname)-8s %(name)-38s %(message)s"

logging.basicConfig(level=logging.INFO, format=LOG_FMT)
logger = logging.getLogger(__name__)

QUERY_INSERT_POSEFF = """
INSERT INTO PosEffects VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);
NOTIFY PosEffects, %s;"""

QUERY_DELETE_POSEFF = """
DELETE FROM PosEffects WHERE Transaction=%s;
NOTIFY PosEffects, %s; NOTIFY PosEffects, %s;"""


# -----------------------------------------------------------------------------
def create_poseffects_table():
    schema = TableSchema([
        ["TradeDate", "date", "NOT NULL"],
        ["TimeCreated", "timestamptz", "NOT NULL"],
        ["Book", "varchar(64)", "NOT NULL"],
        ["Qty", "double precision", "NOT NULL"],
        ["Unit", "varchar(64)", "NOT NULL"],
        ["UnitType", "varchar(64)", "NOT NULL"],
        ["Transaction", "varchar(64)", "NOT NULL"],
        ["Event", "varchar(64)", "NOT NULL"],
        ["Trade", "varchar(64)", "NOT NULL"],
    ])

    indexes = {
        "pos_by_trade_date": ["TradeDate"],
        "pos_by_time_created": ["TimeCreated"],
        "pos_by_book": ["Book"],
        "pos_by_trade": ["Trade"],
    }

    table_obj = ObjDbTable(Name="PosEffects",
                           Schema=schema, Indexes=indexes)

    with ObjDbTransaction("Table Object Insert"):
        AddObj(table_obj)
        table_obj.create()


# -------------------------------------------------------------------------
def CommitTransaction(transaction):
    """
    Description:
        Insert/amend a transaction, taking care of all position effects.
    Inputs:
        transaction - the instance of Transaction to commit
    Returns:
        The Transaction instance.
    """
    # --- clone security traded: AddByInference is needed to generate the
    #     proper ImpliedName.
    sec = AddByInference(GetObj(transaction.SecurityTraded).clone())

    try:
        # --- reload security: this is needed to avoid basing decisions on
        #     attribute values that might have been set in memory
        transaction = GetObj(transaction.Name, refresh=True)

    except ObjNotFound:
        # --- transaction not found, it must be added to the backend along with
        #     its position effects
        transaction.SecurityTraded = sec.Name
        transaction.Marker = "HEAD"
        return insert_transaction(transaction)

    else:
        info = GetVal(transaction, "TransactionInfo")
        info["SecurityTraded"] = sec.Name
        return amend_transaction(transaction, info)


# -----------------------------------------------------------------------------
def insert_transaction(transaction):
    """
    This function should never be called directly. Use TransactionCommit
    instead.
    """
    if transaction.Marker != "HEAD":
        raise TransactionError("Only head transaction can be "
                               "created. Marker for {0:s} is "
                               "{1:s}.".format(transaction.Name,
                                               transaction.Marker))

    # --- create a new transaction to make sure that Version, ChangedBy, and
    #     timestamps are fresh
    name = transaction.format_name(Date.today(), unique_id(8))
    transaction = transaction.clone(name=name)
    time_created = transaction.TimeCreated

    logger.info("creating transaction {0:s}".format(name))

    with ObjDbTransaction("Insert", "SERIALIZABLE"):
        AddObj(transaction)

        for pos in GetVal(transaction, "PositionEffects"):
            ObjDbQuery(QUERY_INSERT_POSEFF,
                       parms=(pos.TradeDate, time_created, pos.Book,
                              pos.Qty, pos.Unit, pos.UnitType, pos.Name,
                              pos.Event, pos.Trade, pos.Book))

    return transaction


# -----------------------------------------------------------------------------
def amend_transaction(head, info):
    """
    This function should never be called directly. Use TransactionCommit
    instead.
    """
    if head.Marker != "HEAD":
        raise TransactionError("Only head transaction can be "
                               "amended. Marker for {0:s} is "
                               "{1:s}.".format(head.Name, head.Marker))

    # --- need to amend?
    same = True
    for attr, value in info.items():
        same = (value == getattr(head, attr))
        if not same:
            break
    if same:
        raise TransactionWarning("amend_transaction, found nothing to amend.")

    if head.TimeCreated >= Date.today():
        # --- same day amendment: execute in-place update
        for attr, value in info.items():
            setattr(head, attr, value)

        logger.info("same day amedment "
                    "for transaction {0:s}".format(head.Name))

        time_created = head.TimeCreated
        with ObjDbTransaction("Amend", "SERIALIZABLE"):
            UpdateObj(head)

            # --- delete existing position effects for head transaction
            ObjDbQuery(QUERY_DELETE_POSEFF, (head.Name, ))

            # --- insert new position effects
            for pos in GetVal(head, "PositionEffects"):
                ObjDbQuery(QUERY_INSERT_POSEFF,
                           parms=(pos.TradeDate, time_created,
                                  pos.Book, pos.Qty, pos.Unit, pos.UnitType,
                                  pos.Name, pos.Event, pos.Trade, pos.Book))

    else:
        # --- previous day amendment: book a backout and then a new transaction
        logger.info("previous day amedment "
                    "for transaction {0:s}".format(head.Name))

        head.Marker = "AMENDED"
        backout = head.clone()
        backout.Name = head.format_name(Date.today(), unique_id(8))
        backout.Marker = "BACKOUT"
        backout.PrevTransaction = head.Name
        new = head.clone()
        new.Name = head.format_name(Date.today(), unique_id(8))
        new.Marker = "HEAD"
        new.PrevTransaction = backout.Name

        for attr, value in info.items():
            setattr(new, attr, value)

        with ObjDbTransaction("Amend", "SERIALIZABLE"):
            UpdateObj(head)
            AddObj(backout)
            AddObj(new)

            # --- update position effects table:
            # ---  1) first the back-out transaction: quantities are flipped to
            #         offset original transaction
            for pos in GetVal(backout, "PositionEffects"):
                ObjDbQuery(QUERY_INSERT_POSEFF,
                           parms=(pos.TradeDate, backout.TimeCreated,
                                  pos.Book, -pos.Qty, pos.Unit, pos.UnitType,
                                  pos.Name, pos.Event, pos.Trade, pos.Book))

            # ---  2) then the new transaction with the amendments
            for pos in GetVal(new, "PositionEffects"):
                ObjDbQuery(QUERY_INSERT_POSEFF,
                           parms=(pos.TradeDate, new.TimeCreated,
                                  pos.Book, pos.Qty, pos.Unit, pos.UnitType,
                                  pos.Name, pos.Event, pos.Trade, pos.Book))

        transaction = new

    return transaction


# -----------------------------------------------------------------------------
def RollbackTransaction(head):
    """
    Description:
        Rolls back a transaction and all its position effects.
    Inputs:
        head - the transaction to roll-back
    Returns:
        None.
    """
    # --- reload security: this is needed to avoid basing decisions on
    #     attribute values that might have been set in memory
    head = GetObj(head.Name, refresh=True)

    if head.Marker != "HEAD":
        raise TransactionError("Only head transaction can be "
                               "rolled back. Marker for {0:s} is "
                               "{1:s}.".format(head.Name,
                                               head.Marker))

    if head.TimeCreated >= Date.today():
        # --- same day roll-back: there are two sub-cases
        if head.PrevTransaction is None:
            # --- case 1: delete transaction (all postion effectes are taken
            #             care of automatically)
            with ObjDbTransaction("Rollback", "SERIALIZABLE"):
                PurgeObj(head.Name)

        else:
            # --- case 2: delete last two transactions and re-mark the amended
            #             one as "HEAD"
            backout = GetObj(head.PrevTransaction, refresh=True)
            amended = GetObj(backout.PrevTransaction, refresh=True)

            # --- check that markers conform to expectation
            if head.Marker != "HEAD":
                raise TransactionError("Wrong Marker for transaction "
                                       "{0:s}: {1:s} instead of "
                                       "HEAD".format(head.Name,
                                                     head.Marker))
            if backout.Marker != "BACKOUT":
                raise TransactionError("Wrong Marker for transaction "
                                       "{0:s}: {1:s} instead of "
                                       "BACKOUT".format(backout.Name,
                                                        backout.Marker))
            if amended.Marker != "AMENDED":
                raise TransactionError("Wrong Marker for transaction "
                                       "{0:s}: {1:s} instead of "
                                       "AMENDED".format(amended.Name,
                                                        amended.Marker))
            amended.Marker = "HEAD"

            with ObjDbTransaction("Rollback", "SERIALIZABLE"):
                PurgeObj(head.Name)
                PurgeObj(backout.Name)
                UpdateObj(amended)

    else:
        # --- previous day roll-back: book backout transactions for both the
        #     current head and backout transactions

        # --- we start with a backout of the head transaction
        head.Marker = "ROLLEDBACK"
        head_backout = head.clone()
        head_backout.Name = head.format_name(Date.today(), unique_id(8))
        head_backout.Marker = "BACKOUT"
        head_backout.PrevTransaction = head.Name

        # --- if head was the result of an amendment, look up the backout
        #     transaction and make it the new head
        if head.PrevTransaction is not None:
            backout = GetObj(head.PrevTransaction, refresh=True)
            reverse = backout.clone()
            reverse.Name = backout.format_name(Date.today(), unique_id(8))
            reverse.Marker = "HEAD"
            reverse.PrevTransaction = head_backout.Name
        else:
            reverse = None

        with ObjDbTransaction("Rollback", "SERIALIZABLE"):
            UpdateObj(head)
            AddObj(head_backout)

            # --- now update position effects: quantities are flipped to
            #     offset original transactions
            for pos in GetVal(head_backout, "PositionEffects"):
                ObjDbQuery(QUERY_INSERT_POSEFF,
                           parms=(pos.TradeDate, head_backout.TimeCreated,
                                  pos.Book, -pos.Qty, pos.Unit, pos.UnitType,
                                  pos.Name, pos.Event, pos.Trade, pos.Book))

            if reverse is not None:
                AddObj(reverse)
                for pos in GetVal(reverse, "PositionEffects"):
                    ObjDbQuery(QUERY_INSERT_POSEFF,
                               parms=(pos.TradeDate, reverse.TimeCreated,
                                      pos.Book, -pos.Qty,  pos.Unit,
                                      pos.UnitType, pos.Name, pos.Event,
                                      pos.Trade, pos.Book))


# -----------------------------------------------------------------------------
def DeleteTransaction(transaction):
    """
    Description:
        Delete a transaction and all its position effects.
    Inputs:
        transaction - the transaction to delete
    Returns:
        None.
    """
    # --- reload security: this is needed to avoid basing decisions on
    #     attribute values that might have been set in memory
    transaction = GetObj(transaction.Name, refresh=True)

    if transaction.Marker != "HEAD":
        raise TransactionError("Only head transaction can be "
                               "rolled back. Marker for {0:s} is "
                               "{1:s}.".format(transaction.Name,
                                               transaction.Marker))

    if transaction.TimeCreated >= Date.today():
        # --- same day delete: recursively delete transaction-chain
        prev = transaction.PrevTransaction
        with ObjDbTransaction("Delete", "SERIALIZABLE"):
            while prev is not None:
                PurgeObj(transaction)
                transaction = prev
                prev = transaction.PrevTransaction

    else:
        # --- previous day delete: book backout transaction
        transaction.Marker = "DELETED"
        backout = transaction.clone()
        backout.Name = transaction.format_name(Date.today(), unique_id(8))
        backout.Marker = "BACKOUT"
        backout.PrevTransaction = transaction.Name

        with ObjDbTransaction("Delete", "SERIALIZABLE"):
            UpdateObj(transaction)
            AddObj(backout)

            # --- now update position effects: quantities are flipped to
            #     offset original transactions
            for pos in GetVal(backout, "PositionEffects"):
                ObjDbQuery(QUERY_INSERT_POSEFF,
                           parms=(pos.TradeDate, backout.TimeCreated,
                                  pos.Book, -pos.Qty, pos.Unit, pos.UnitType,
                                  pos.Name, pos.Event, pos.Trade, pos.Book))


# -----------------------------------------------------------------------------
def AgeTransaction(head, date):
    """
    Description:
        Age a transaction and all its position effects.
    Inputs:
        head - the transaction to roll-back
        date - the date of the ageing event
    Returns:
        None.
    """
    # --- reload security: this is needed to avoid basing decisions on
    #     attribute values that might have been set in memory
    head = GetObj(head.Name, refresh=True)

    if head.Marker != "HEAD":
        raise TransactionError("Only head transaction can be aged. Marker "
                               "for {0:s} is {1:s}.".format(head.Name,
                                                            head.Marker))

    sec = GetVal(head, "SecurityTraded")
    event = GetVal(sec, "ExpectedTransaction")
    securities = GetVal(sec, "ExpectedSecurities", event)

    head.Marker = "AGED"
    backout = head.clone()
    backout.Name = head.format_name(Date.today(), unique_id(8))
    backout.Marker = "BACKOUT"
    backout.TransactionDate = date
    backout.PrevTransaction = head.Name

    with ObjDbTransaction("Ageing Event", "SERIALIZABLE"):
        # --- add backout transaction and its positions effects
        AddObj(backout)
        UpdateObj(head)

        for pos in GetVal(backout, "PositionEffects"):
            ObjDbQuery(QUERY_INSERT_POSEFF,
                       parms=(pos.TradeDate, backout.TimeCreated,
                              pos.Book, -pos.Qty, pos.Unit, pos.UnitType,
                              pos.Name, pos.Event, pos.Trade, pos.Book))

        # --- insert new transactions
        prev_trans = backout.Name

        for sec_info in securities:
            # --- add security
            sec = AddByInference(sec_info["Security"])
            # --- append new transaction
            insert_transaction(Transaction(
                TransactionDate=date,
                SecurityTraded=sec.Name,
                Quantity=head.Quantity*sec_info["Quantity"],
                Party=GetVal(head, "Party"),
                Counterparty=GetVal(head, "Counterparty"),
                Trade=head.Trade,
                PrevTransaction=prev_trans,
                Event=event,
                Marker="HEAD",
            ))

            # --- only the first of the new transactions points to the previous
            #     trnsaction in the chain (which one exactly of the new
            #     transactionsdoesn't matter as they would have to be all
            #     rolled back together)
            prev_trans = None


# -----------------------------------------------------------------------------
def TransactionsBy(book=None, trade=None,
                   security=None, date_range=None, head_only=True):
    """
    Description:
        Return all transactions matching the given criteria.
    Inputs:
        book       - a given book
        trade      - a given trade
        security   - a given security
        date_range - a tuple of start and end date
        head_only  - if True, only returns the Head trade
    Returns:
        A list of trade names.
    """
    extquery = []
    criteria = []

    if book is not None:
        extquery.append("Book=%s")
        criteria.append(book)

    if trade is not None:
        extquery.append("Trade=%s")
        criteria.append(trade)

    if security is not None:
        extquery.append("Unit=%s")
        criteria.append(security)

    if date_range is not None:
        extquery.append("TradeDate BETWEEN %s AND %s")
        criteria.append(date_range[0])
        criteria.append(date_range[1])

    if len(criteria):
        query = ("SELECT DISTINCT(Transaction) "
                 "FROM PosEffects WHERE {0:s};").format(" AND ".join(extquery))
        rows = ObjDbQuery(query, parms=criteria, attr="fetchall")

    else:
        query = "SELECT DISTINCT(Transaction) FROM PosEffects;"
        rows = ObjDbQuery(query, attr="fetchall")

    if head_only:
        return [row.transaction for row in rows
                if GetVal(row.transaction, "Marker") == "HEAD"]
    else:
        return [row.transaction for row in rows]
