from litestar import Router

from .tickers_controllers import TickerDataController

per_security_router = Router("per-security", route_handlers=[TickerDataController])
