from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class APITags(Enum):
    root = "Root"
    per_security = "Per Security"
    bulk = "Bulk"


class Period(Enum):
    ONE_DAY = "1d"
    FIVE_DAYS = "5d"
    ONE_MONTH = "1mo"
    THREE_MONTHS = "3mo"
    SIX_MONTHS = "6mo"
    ONE_YEAR = "1y"
    TWO_YEARS = "2y"
    FIVE_YEARS = "5y"
    TEN_YEARS = "10y"
    YEAR_TO_DATE = "ytd"
    MAX = "max"


class Interval(Enum):
    ONE_MINUTE = "1m"
    TWO_MINUTES = "2m"
    FIVE_MINUTES = "5m"
    FIFTEEN_MINUTES = "15m"
    THIRTY_MINUTES = "30m"
    SIXTY_MINUTES = "60m"
    NINETY_MINUTES = "90m"
    ONE_HOUR = "1h"
    ONE_DAY = "1d"
    FIVE_DAYS = "5d"
    ONE_WEEK = "1wk"
    ONE_MONTH = "1mo"
    THREE_MONTHS = "3mo"


class StockExchange(Enum):
    NSE = "NSE"
    BSE = "BSE"
    TSE = "TSE"
    LSE = "LSE"
    HKEX = "HKEX"
    XETRA = "XETRA"
    SSE = "SSE"
    ASX = "ASX"
    NASDAQ = "NASDAQ"
    NYSE = "NYSE"
    BMV = "BMV"
    TSX = "TSX"
    EURONEXT = "EURONEXT"


class StockExchangeYahooIdentifier(Enum):
    NSE = ".NS"
    BSE = ".BO"
    TSE = ".T"
    LSE = ".L"
    HKEX = ".H"
    XETRA = ".X"
    SSE = ".S"
    ASX = ".A"
    NASDAQ = ".N"
    NYSE = ".Y"
    BMV = ".M"
    TSX = ".C"
    EURONEXT = ".F"


class StockExchangeFullName(Enum):
    NSE = "National Stock Exchange of India"
    BSE = "Bombay Stock Exchange"
    TSE = "Tokyo Stock Exchange"
    LSE = "London Stock Exchange"
    HKEX = "Hong Kong Stock Exchange"
    XETRA = "Frankfurt Stock Exchange"
    SSE = "Shanghai Stock Exchange"
    ASX = "Australian Securities Exchange"
    NASDAQ = "NASDAQ Stock Exchange"
    NYSE = "New York Stock Exchange"
    BMV = "Mexico Stock Exchange"
    TSX = "Toronto Stock Exchange"
    EURONEXT = "Euronext"


class TickerHistoryQuery(BaseModel):
    model_config = {"extra": "forbid"}

    interval: Interval = Field(
        Interval.ONE_DAY, description="Day interval between historical data points"
    )
    period: Period = Field(
        Period.ONE_DAY,
        description="Day period between historical data points. This is mutually exclusive with `start_date` and `end_date`",
    )
    start_date: date = Field(
        None,
        description="Start date for historical data points. This is mutually exclusive with `period`",
        examples=["2024-01-01", "2020-12-31"],
    )
    end_date: date = Field(
        None,
        description="End date for historical data points. This is mutually exclusive with `period`",
        examples=["2024-02-01", "2021-01-31"],
    )
