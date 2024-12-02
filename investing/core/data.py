from collections import namedtuple
from dataclasses import dataclass
from datetime import date
from typing import Type

import polars as pl
import yfinance as yf

from investing.core.models import Interval, Period


@dataclass
class StockData:
    """
    A class to interact with stock data provided by yfinanc api.

    Attributes
    ----------
        ticker : str | list[str]
            Ticker or list of ticker symbol the stock data.
    """

    ticker: str | list[str]

    TickerData = namedtuple("TickerData", [])

    def __post_init__(self):
        if isinstance(self.ticker, str):
            self._ticker_data = namedtuple(
                "TickerData", self._remove_exchange_symbol([self.ticker])
            )
        if isinstance(self.ticker, list):
            self._ticker_data = namedtuple(
                "TickerData", self._remove_exchange_symbol(self.ticker)
            )

    @property
    def ticker_handler(self) -> yf.Ticker | yf.Tickers:
        return (
            yf.Ticker(self.ticker)
            if isinstance(self.ticker, str)
            else yf.Tickers(" ".join(self.ticker))
        )

    def get_ticker_info(self) -> Type[TickerData]:
        if isinstance(self.ticker_handler, yf.Ticker):
            setattr(
                self._ticker_data,
                self._remove_exchange_symbol(self.ticker),
                self.ticker_handler.get_info(),
            )
        else:
            for tick in self.ticker:
                setattr(
                    self._ticker_data,
                    self._remove_exchange_symbol(tick),
                    self.ticker_handler.tickers[tick].get_info(),
                )
        return self._ticker_data

    def get_ticker_history(
        self,
        period: Period = Period.MAX,
        interval: Interval = Interval.ONE_DAY,
        start: str | date | None = None,
        end: str | date | None = None,
    ) -> Type[TickerData]:
        if isinstance(self.ticker, str):
            result = self.ticker_handler.history(
                period=period.value,
                interval=interval.value,
                start=start,
                end=end,
                # group_by="ticker", # NOTE - not present in single `Ticker` object
            )
            setattr(
                self._ticker_data,
                self._remove_exchange_symbol(self.ticker),
                pl.from_pandas(result),
            )
        else:
            result = self.ticker_handler.history(
                period=period.value,
                interval=interval.value,
                start=start,
                end=end,
                group_by="ticker",
            )
            for t in self.ticker:
                setattr(
                    self._ticker_data,
                    self._remove_exchange_symbol(t),
                    pl.from_pandas(result[t]),
                )
        return self._ticker_data

    # TODO - add methods supporting all other api functionality provided by YFinance

    @staticmethod
    def _remove_exchange_symbol(symbol: str | list[str]) -> str | list[str]:
        if isinstance(symbol, str):
            return symbol.split(".")[0]
        else:
            return [i.split(".")[0] for i in symbol]
