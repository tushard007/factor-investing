import logging

import polars as pl
from stock_indicators import indicators

from investing.core.exception import InvestingIndicaError
from ._base import IndicatorBase

logger = logging.getLogger("factor-investing")


class SuperTrend(IndicatorBase):
    def __init__(
        self,
        data: pl.DataFrame | dict[str, pl.DataFrame],
        retain_source_column: list[str] | None = None,
    ):
        if retain_source_column is None:
            retain_source_column = ["close"]
        self._result_data = None
        super().__init__(data, retain_source_column)

    def calculate_per_security(
        self, lookback_periods: int = 10, multiplier: float = 3
    ) -> pl.DataFrame:
        if not isinstance(self.data, pl.DataFrame):
            raise InvestingIndicaError(
                "found multiple securities, use calculate_bulk instead"
            )
        if not self._result_data:
            self._result_data = self._unit_result(
                self._quote_data(), lookback_periods, multiplier
            )
        return self._result_data

    def calculate_bulk(
        self, lookback_periods: int = 10, multiplier: float = 3
    ) -> dict[str, pl.DataFrame]:
        if isinstance(self.data, pl.DataFrame):
            raise InvestingIndicaError(
                "found single security, use calculate_security instead"
            )
        if not self._result_data:
            quote_data = self._quote_data()
            self._result_data = {
                ticker: self._unit_result(quote, lookback_periods, multiplier, ticker)
                for ticker, quote in quote_data.items()
            }
        return self._result_data

    def plot_line(self, ticker: str = None, columns_to_plot: list[str] = None):
        if isinstance(self.data, dict):
            if not ticker:
                raise InvestingIndicaError(
                    "found multiple securities, provide ticker name to plot"
                )
            if self._result_data is None:
                logger.debug("no result data found, calculating first")
                self._result_data = self.calculate_bulk()
            plot_df = self._prepare_data_for_plot(
                data=self._result_data[ticker],
                on=columns_to_plot,
            )
        else:
            if self._result_data is None:
                logger.debug("no result data found, calculating first")
                self._result_data = self.calculate_per_security()
            plot_df = self._prepare_data_for_plot(
                data=self._result_data,
            )
        return plot_df.plot.line(x="date", y="price", color="indicator")

    def plot_bar(self, ticker: str = None):
        pass

    def plot_candle_stick(self, ticker: str = None):
        pass

    def rank(self):
        pass

    def _unit_result(self, quote_data, lookback_periods, multiplier, ticker=None):
        # calculating indicator specific results
        result = indicators.get_super_trend(
            quote_data, lookback_periods, multiplier
        ).condense()
        result_df = pl.DataFrame(
            [
                {
                    "date": i.date,
                    "super_trend": i.super_trend,
                    "upper": i.upper_band,
                    "lower": i.lower_band,
                }
                for i in result
            ],
            infer_schema_length=None,  # use of every row to determine colum  type
        )
        result_df = result_df.with_columns(
            pl.col("date").cast(pl.Date),
            pl.col("super_trend").cast(pl.Float64).round(2),
            pl.col("upper").cast(pl.Float64).round(2),
            pl.col("lower").cast(pl.Float64).round(2),
        )
        cols = result_df.columns

        # getting source data
        source_data = self.data[ticker] if ticker else self.data

        # performing join ops to retain source column
        if self.retain_source_column:
            # Date column is reserved for join ops
            if "date" not in self.retain_source_column:
                self.retain_source_column.append("date")
            # adding all the required column from parent source
            source_select = source_data.select(self.retain_source_column)
            # inner join
            result_df = result_df.join(source_select, on="date", how="inner")
            # re-arranging columns
            self.retain_source_column.remove("date")
            cols[1:1] = self.retain_source_column  # inserting after index 1

        return result_df.select(cols)
