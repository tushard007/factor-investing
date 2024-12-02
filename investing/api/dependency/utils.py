from collections import namedtuple
from typing import Annotated

from fastapi import Path

from investing.core.models import StockExchange, StockExchangeYahooIdentifier

TickerIdentifier = namedtuple("TickerIdentifier", ["symbol", "exch_id"])


async def yahoo_finance_aware_ticker(
    exchange: Annotated[
        StockExchange,
        Path(
            description="Exchange symbol to which `Ticker` belongs",
        ),
    ],
    ticker: Annotated[str, Path(description="Desired company's `Ticker` symbol")],
) -> TickerIdentifier:
    ticker = ticker.upper()  # making sure that ticker symbol are always Upper case
    yahoo_exch_id = getattr(StockExchangeYahooIdentifier, exchange.name)
    return TickerIdentifier(ticker, yahoo_exch_id.value)
