class YahooAPIError(Exception):
    def __init__(self, ticker: str | list[str], message: str):
        self.ticker = ticker
        self.message = message
        super().__init__(f"ticker(s): {ticker}, have {self.message} issue")
