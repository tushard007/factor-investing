class YahooAPIError(Exception):
    """Raised when error occurs in Yahoo Finance API"""

    def __init__(self, ticker: str | list[str], message: str):
        self.ticker = ticker
        self.message = message
        super().__init__(f"ticker(s): {ticker}, have {self.message} issue")


class InvestingIndicaError(Exception):
    """Raised when error occurs in Investing Indicators"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
