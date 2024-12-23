import logging
from typing import Annotated

import polars as pl
from fastapi import APIRouter, Path, Query

from investing.core.data import StockData
from investing.core.indicator.price_trend import SuperTrend
from investing.core.models import (
    APITags,
    StockExchange,
    TickerInput,
    StockExchangeYahooIdentifier,
    SuperTrendRecentNDatasetQuery,
    SuperTrendRecentNDatasetFormat,
)

logger = logging.getLogger("factor-investing")
router = APIRouter(prefix="/api/dataset/indicator", tags=[APITags.dataset])


@router.post(
    "/{exchange}/indicator/super-trend",
)
async def super_trend_recent_top_n(
    exchange: Annotated[
        StockExchange,
        Path(
            description="Exchange symbol to which `Ticker` belongs",
        ),
    ],
    ticker: TickerInput,
    query_param: Annotated[SuperTrendRecentNDatasetQuery, Query()],
) -> list[str] | list[dict]:
    """Super Trend attempts to determine the primary trend of Close prices by using
    Average True Range (ATR) band thresholds. It can indicate a buy/ sell signal or a trailing stop
    when the trend changes.

    `Super Trend Recent N`: Is based on following logic:
      - Calculate SuperTrend for each given ticker
      - Get top `n` rows based on `lower` column
      - Filter out tickers which have `null` in recent `n` rows
    """
    yahoo_tickers = ticker.get_yahoo_aware_ticker(exchange)

    stock_data = StockData(
        ticker.ticker, getattr(StockExchangeYahooIdentifier, exchange.name)
    )
    history = stock_data.get_ticker_history(
        period=query_param.period,
        interval=query_param.interval,
        start=query_param.start_date,
        end=query_param.end_date,
    )
    indicator_data = SuperTrend(history, query_param.retain_source_column)
    result = indicator_data.calculate_bulk(
        lookback_periods=query_param.lookback_periods, multiplier=query_param.multiplier
    )

    # Transformation for the dataset
    for ticker in list(result):
        # adding ticker column
        cols = result[ticker].columns
        cols[1:1] = ["ticker"]
        result[ticker] = result[ticker].with_columns(ticker=pl.lit(ticker))
        # rearranging columns
        result[ticker] = result[ticker].select(cols)
        # getting recent `n` rows
        result[ticker] = (
            result[ticker].sort(by="date", descending=True).head(query_param.recent_n)
        )
        # removing tickers which have `null` in recent n rows for lower column
        if result[ticker].select("lower").to_series().has_nulls():
            logger.debug(f"found null in {ticker}, removing it")
            result.pop(ticker)

    # sending result based on desired format
    if query_param.result_format == SuperTrendRecentNDatasetFormat.detail:
        final_result = pl.DataFrame()
        for ticker in result:
            final_result = final_result.vstack(result[ticker])
        final_result = final_result.to_dicts()
    elif query_param.result_format == SuperTrendRecentNDatasetFormat.ticker_only:
        final_result = list(result)

    return final_result
