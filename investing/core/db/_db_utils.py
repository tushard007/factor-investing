import logging

import polars as pl

from investing.core.exception import YahooAPIError

logger = logging.getLogger("factor-investing")


def prepare_ticker_history_table(df: pl.DataFrame, ticker: str) -> pl.DataFrame:
    if df.is_empty():
        raise YahooAPIError(
            ticker, "got empty dataframe, may not able to download data from yahoo"
        )
    ticker = ticker.upper()
    # Note - Creating the query for transformation lazily
    df = df.lazy()

    # creating primary key & other column
    df = df.with_columns(
        (pl.col("Date").cast(pl.Date)),
        (pl.lit(ticker).alias("ticker")),
        (
            pl.lit(ticker.lower())
            + pl.col("Date").cast(pl.Date).cast(pl.String).str.replace_all("-", "")
        ).alias("key"),
    )

    # dropping all null values
    df = df.drop_nulls()

    # rearranging appropriately
    df = df.select(
        pl.col("Date").cast(pl.Date).alias("date"),
        pl.col("ticker").cast(pl.String),
        pl.col("key").cast(pl.String),
        pl.col("Open").cast(pl.Float64).alias("open"),
        pl.col("High").cast(pl.Float64).alias("high"),
        pl.col("Low").cast(pl.Float64).alias("low"),
        pl.col("Close").cast(pl.Float64).alias("close"),
    )
    return df.collect()
