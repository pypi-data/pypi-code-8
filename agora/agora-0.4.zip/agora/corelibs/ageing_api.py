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

from onyx.core import GetVal
from agora.corelibs.trade_api import TradesBy


# -----------------------------------------------------------------------------
def age_portfolio(port):
    books = GetVal(port, "RecursiveBooks")
    kids = set.union(*[set(GetVal(book, "Children").keys()) for book in books])
    pos_dt = GetVal("Database", "PositionsDate")
    for kid in kids:
        ntd = GetVal(kid, "NextTransactionDate")
        if ntd == pos_dt:
            print(kid, "do something...")
            trade_type = GetVal(kid, "ExpectedTransaction")
            print(trade_type)
            print(GetVal(kid, "ExpectedSecurities", trade_type))

            # --- affected trades
            trades = TradesBy(security=kid)
            print(trades)

            for trade in trades:
                pass

if __name__ == "__main__":
    from onyx.core import Date, EvalBlock
    from agora.corelibs.onyx_utils import OnyxInit

    with OnyxInit():
        with EvalBlock() as eb:
            eb.set_diddle("Database", "PositionsDate", Date(2015, 4, 24))
            age_portfolio("AVC EQ LS")
