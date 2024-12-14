import polars as pl
import yfinance as yf

from investing.core.data import Interval, Period, StockData

unit_stock_data = StockData(ticker="INFY.NS")
bulk_stock_data = StockData(ticker=["INFY", "TCS"])


def test_stock_data_ticker_handler():
    assert isinstance(unit_stock_data.ticker_handler, yf.ticker.Ticker)
    assert isinstance(bulk_stock_data.ticker_handler, yf.tickers.Tickers)


def test_stock_data_get_ticker_info():
    # Unit ticker
    unit_result = unit_stock_data.get_ticker_info()
    assert unit_result["INFY"]["longName"] == "Infosys Limited"

    # Multiple tickers
    bulk_result = bulk_stock_data.get_ticker_info()
    assert bulk_result["INFY"]["longName"] == "Infosys Limited"
    assert bulk_result["TCS"]["longName"] == "Tata Consultancy Services Limited"


def test_stock_data_get_ticker_history():
    # Unit ticker
    unit_result = unit_stock_data.get_ticker_history(
        period=Period.FIVE_DAYS, interval=Interval.ONE_DAY
    )
    assert isinstance(unit_result["INFY"], pl.DataFrame)
    assert "Close" in unit_result["INFY"].columns

    # Multiple ticker
    bulk_result = bulk_stock_data.get_ticker_history()
    assert isinstance(bulk_result["INFY"], pl.DataFrame)
    assert "Close" in bulk_result["INFY"].columns
    assert isinstance(bulk_result["TCS"], pl.DataFrame)
    assert "Close" in bulk_result["TCS"].columns
