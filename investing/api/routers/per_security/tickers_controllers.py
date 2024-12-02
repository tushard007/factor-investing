from typing import Annotated

from litestar import Controller, get
from litestar.openapi.spec.example import Example
from litestar.params import Parameter

from investing.core.data import StockData
from investing.core.models import StockExchange, StockExchangeFullName


class TickerDataController(Controller):
    path = "/per-security"

    @get("/", name="List available exchange")
    async def list_exchange(self) -> dict[str, str]:
        """Get list of available exchanges"""
        return {
            exchange.name.lower(): exchange.value for exchange in StockExchangeFullName
        }

    @get("/{exchange: str}", name="List available ticker")
    async def list_ticker(
        self,
        exchange: Annotated[
            str,
            Parameter(
                description="Symbol of the exchange",
                examples=[Example("nse"), Example("nyse")],
            ),
        ],
    ) -> list[str]:
        "Get all the available `ticker` in given `exchange`"
        return ["INFY", "AAPL"]

    @get("/{exchange: str}/{ticker: str}", name="Get ticker info")
    async def get_ticker_data(self, exchange: StockExchange, ticker: str) -> dict:
        stock_data = StockData(f"{exchange.value}/{ticker}")
        result = stock_data.get_ticker_info()
        return getattr(result, ticker)
