from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query

from investing.api.dependency.utils import yahoo_finance_aware_ticker
from investing.core.data import StockData
from investing.core.models import (
    APITags,
    ExchangeTickers,
    ExchangeTickersHistory,
    StockExchangeFullName,
    TickerHistoryQuery,
    YahooTickerIdentifier,
)

router = APIRouter(prefix="/api/per-security", tags=[APITags.per_security])


@router.get("/")
async def list_exchange() -> dict[str, str]:
    """Get list of available exchanges"""
    return {exchange.name.lower(): exchange.value for exchange in StockExchangeFullName}


@router.get("/{exchange}", response_model=ExchangeTickers)
async def list_ticker(
    exchange: Annotated[
        str,
        Path(
            description="Symbol of the exchange",
            examples=["nse", "nyse"],
        ),
    ],
) -> list[str]:
    """Get all the available `ticker` in given `exchange`"""
    return ["INFY", "AAPL"]


@router.get("/{exchange}/{ticker}")
async def ticker_information(
    # exchange: Annotated[StockExchange, Path(description="Exchange symbol to which ticker belongs")],
    ticker: Annotated[YahooTickerIdentifier, Depends(yahoo_finance_aware_ticker)],
) -> dict:
    """Get given `Ticker` information"""
    stock_data = StockData(f"{ticker.symbol}{ticker.exch_id}")
    result = stock_data.get_ticker_info()
    return getattr(result, ticker.symbol)


@router.get("/{exchange}/{ticker}/history")
async def ticker_history(
    ticker: Annotated[YahooTickerIdentifier, Depends(yahoo_finance_aware_ticker)],
    query_param: Annotated[TickerHistoryQuery, Query()],
) -> ExchangeTickersHistory:
    """Get stock history data for given `Ticker`"""
    stock_data = StockData(f"{ticker.symbol}{ticker.exch_id}")
    result = stock_data.get_ticker_history(
        period=query_param.period,
        interval=query_param.interval,
        start=query_param.start_date,
        end=query_param.end_date,
    )
    return ExchangeTickersHistory(
        ticker=ticker.symbol,
        exchange=ticker.exchange,
        history=getattr(result, ticker.symbol).to_dicts(),
    )
