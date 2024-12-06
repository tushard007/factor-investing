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
    nse = "nse"
    bse = "bse"
    tse = "tse"
    lse = "lse"
    hkex = "hkex"
    xetra = "xetra"
    sse = "sse"
    asx = "asx"
    nasdaq = "nasdaq"
    nyse = "nyse"
    bmv = "bmv"
    tsx = "tsx"
    euronext = "euronext"


class StockExchangeYahooIdentifier(Enum):
    nse = ".NS"
    bse = ".BO"
    tse = ".T"
    lse = ".L"
    hkex = ".H"
    xetra = ".X"
    sse = ".S"
    asx = ".A"
    nasdaq = ".N"
    nyse = ".Y"
    bmv = ".M"
    tsx = ".C"
    euronext = ".F"


class StockExchangeFullName(Enum):
    nse = "National Stock Exchange of India"
    bse = "Bombay Stock Exchange"
    tse = "Tokyo Stock Exchange"
    lse = "London Stock Exchange"
    hkex = "Hong Kong Stock Exchange"
    xetra = "Frankfurt Stock Exchange"
    sse = "Shanghai Stock Exchange"
    asx = "Australian Securities Exchange"
    nasdaq = "nasdaq Stock Exchange"
    nyse = "New York Stock Exchange"
    bmv = "Mexico Stock Exchange"
    tsx = "Toronto Stock Exchange"
    euronext = "euronext"


class YahooTickerIdentifier(BaseModel):
    symbol: str
    exchange: str
    exch_id: str


class ExchangeTickers(BaseModel):
    exchange: str
    tickers: list[str]


class ExchangeTickersInfo(BaseModel):
    exchange: str
    ticker: str
    info: dict


class TickerHistoryOutput(BaseModel):
    Open: float
    High: float
    Low: float
    Close: float
    Volume: float
    Dividends: float
    Stock_Splits: float = Field(alias="Stock Splits")


class ExchangeTickersHistory(BaseModel):
    exchange: str
    ticker: str
    history: list[TickerHistoryOutput] | None = None


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


class TickerInput(BaseModel):
    ticker: list[str] = Field(
        description="Desired company's `Ticker` symbol",
        examples=[
            ["infy", "tcs", "AKASH"],
            ["AAPL", "msft"],
        ],
    )

    def get_yahoo_aware_ticker(
        self, exchange: StockExchange
    ) -> list[YahooTickerIdentifier]:
        """Get Ticker wrt to yahoo aware exchange."""
        self.ticker = [
            t.upper() for t in self.ticker
        ]  # making sure that ticker symbol are always Upper case
        return [
            YahooTickerIdentifier(
                symbol=t,
                exchange=exchange.name,
                exch_id=getattr(StockExchangeYahooIdentifier, exchange.name),
            )
            for t in self.ticker
        ]
