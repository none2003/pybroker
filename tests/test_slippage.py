"""Unit tests for slippage.py module."""

"""Copyright (C) 2023 Edward West

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pytest
import random
from .fixtures import *
from pybroker.context import ExecContext
from pybroker.slippage import RandomSlippageModel, SlippageData
from unittest.mock import patch


@pytest.fixture()
def ctx(
    col_scope,
    ind_scope,
    input_scope,
    pred_scope,
    pending_order_scope,
):
    return ExecContext(
        symbol="SPY",
        config=None,
        portfolio=None,
        col_scope=col_scope,
        ind_scope=ind_scope,
        input_scope=input_scope,
        pred_scope=pred_scope,
        pending_order_scope=pending_order_scope,
        models={},
        sym_end_index={},
        session={},
    )


class TestRandomSlippageModel:
    def test_slip_when_buy_shares(self, ctx):
        model = RandomSlippageModel(min_pct=1, max_pct=2)
        data = SlippageData(buy_shares=100, sell_shares=None)
        with patch.object(random, "uniform", return_value="0.01"):
            model.apply_slippage(data, ctx)
            assert ctx.buy_shares == Decimal(99)
            assert ctx.sell_shares is None

    def test_slip_when_sell_shares(self, ctx):
        model = RandomSlippageModel(min_pct=1, max_pct=2)
        data = SlippageData(buy_shares=None, sell_shares=100)
        with patch.object(random, "uniform", return_value="0.01"):
            model.apply_slippage(data, ctx)
            assert ctx.sell_shares == Decimal(99)
            assert ctx.buy_shares is None