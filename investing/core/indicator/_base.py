from abc import ABC, abstractmethod
from dataclasses import dataclass

import polars as pl

from investing.core.data import polars_to_quote


@dataclass
class IndicatorBase(ABC):
    data: pl.DataFrame | dict[str, pl.DataFrame]
    retain_source_column: list[str] | None

    @abstractmethod
    def calculate_per_security(self): ...

    @abstractmethod
    def calculate_bulk(self): ...

    @abstractmethod
    def plot_line(self, ticker: str = None): ...

    @abstractmethod
    def plot_candle_stick(self, ticker: str = None): ...

    @abstractmethod
    def plot_bar(self, ticker: str = None): ...

    @abstractmethod
    def rank(self): ...

    def _quote_data(self):
        if isinstance(self.data, dict):
            return {ticker: polars_to_quote(df) for ticker, df in self.data.items()}
        else:
            return polars_to_quote(self.data)

    @staticmethod
    def _prepare_data_for_plot(data: pl.DataFrame, on=None) -> pl.DataFrame:
        return data.unpivot(
            on=on,
            index="date",
            variable_name="indicator",
            value_name="price",
        )
