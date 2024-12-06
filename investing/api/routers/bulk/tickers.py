from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from investing.api.dependency.utils import (
    yahoo_finance_aware_exchange_check,
)
from investing.core.data import StockData
from investing.core.models import (
    APITags,
    ExchangeTickers,
    ExchangeTickersHistory,
    ExchangeTickersInfo,
    StockExchange,
    TickerHistoryQuery,
    TickerInput,
)

router = APIRouter(prefix="/api/bulk", tags=[APITags.bulk])


@router.post("/", response_model=list[ExchangeTickers])
async def tickers_wrt_exchange(
    exchange: Annotated[list[str], Depends(yahoo_finance_aware_exchange_check)],
) -> dict[str, str]:
    """Get list of available `Tickers` w.r.t. given `Exchange(s)`."""
    # TODO - add logic to get list of tickers
    return {e: None for e in exchange}


@router.post("/{exchange}", response_model=list[ExchangeTickersInfo])
async def ticker_info_wrt_exchange(
    exchange: Annotated[
        StockExchange,
        Path(
            description="Exchange symbol to which `Ticker` belongs",
        ),
    ],
    ticker: TickerInput,
):
    """Get information of all`Tickers` w.r.t. given `Exchange(s)`."""
    yahoo_tickers = ticker.get_yahoo_aware_ticker(exchange)
    tickers = [f"{t.symbol}{t.exch_id}" for t in yahoo_tickers]

    stock_data = StockData(tickers)
    result = stock_data.get_ticker_info()
    return [
        ExchangeTickersInfo(
            exchange=t.exchange.upper(),
            ticker=t.symbol.upper(),
            info=getattr(result, t.symbol.upper()),
        )
        for t in yahoo_tickers
    ]


@router.post("/{exchange}/history")
async def ticker_history(
    exchange: Annotated[
        StockExchange,
        Path(
            description="Exchange symbol to which `Ticker` belongs",
        ),
    ],
    ticker: TickerInput,
    query_param: Annotated[TickerHistoryQuery, Query()],
) -> list[ExchangeTickersHistory]:
    """Get stock history data for given `Ticker`"""
    yahoo_tickers = ticker.get_yahoo_aware_ticker(exchange)
    tickers = [f"{t.symbol}{t.exch_id}" for t in yahoo_tickers]

    stock_data = StockData(tickers)
    result = stock_data.get_ticker_history(
        period=query_param.period,
        interval=query_param.interval,
        start=query_param.start_date,
        end=query_param.end_date,
    )
    return [
        ExchangeTickersHistory(
            exchange=t.exchange.upper(),
            ticker=t.symbol.upper(),
            history=getattr(result, t.symbol.upper()).to_dicts(),
        )
        for t in yahoo_tickers
    ]
