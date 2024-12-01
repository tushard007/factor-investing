import re
from datetime import datetime
from enum import Enum


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


class DateString:
    date_format = "%Y-%m-%d"
    regex_pattern = r"^\d{4}-\d{2}-\d{2}$"

    def __init__(self, date_str: str):
        if not self.is_valid_date(date_str):
            raise ValueError(
                f"Date string '{date_str}' is not in the yyyy-mm-dd format."
            )
        self.date_str = date_str

    @classmethod
    def is_valid_date(cls, date_str: str) -> bool:
        if not re.match(cls.regex_pattern, date_str):
            return False
        try:
            datetime.strptime(date_str, cls.date_format)
            return True
        except ValueError:
            return False

    def __str__(self):
        return self.date_str

    def to_date(self):
        return datetime.strptime(self.date_str, self.date_format).date()
