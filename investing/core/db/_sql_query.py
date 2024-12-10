import datetime

from sqlglot import Dialects, exp, select

TABLE_FULL_NAME = "factor_investing.ticker_history"


def latest_data_query() -> str:
    _sub_query = select(exp.Max(this="date")).from_(TABLE_FULL_NAME)
    return (
        select("*")
        .from_(TABLE_FULL_NAME)
        .where(f"date = ({_sub_query})")
        .sql(Dialects.POSTGRES)
    )


def specific_date_query(date: datetime.date) -> str:
    return (
        select("*").from_(TABLE_FULL_NAME).where("date").eq(date).sql(Dialects.POSTGRES)
    )


def get_ticker_history_query(ticker: str) -> str:
    return (
        select("*")
        .from_(TABLE_FULL_NAME)
        .where("ticker")
        .eq(ticker)
        .sql(Dialects.POSTGRES)
    )
