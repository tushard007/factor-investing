import logging
from contextlib import asynccontextmanager
from pathlib import Path

from adbc_driver_postgresql import dbapi
from dotenv import dotenv_values
from fastapi import FastAPI

from investing.api.routers import bulk, per_security
from investing.core.models import APITags

logger = logging.getLogger("factor-investing")


@asynccontextmanager
async def db_connect(app: FastAPI):
    """Connect to database FastAPI Lifecycle"""
    config = dotenv_values(Path(__file__).resolve().parent / ".env")
    app.state.connect = dbapi.connect(
        f"postgresql://{config['USER']}:{config['PASSWORD']}@localhost:5432/playground"
    )
    logger.info("connected to database")
    yield
    app.state.connect.close()
    logger.info("closed connection")


app = FastAPI(
    title="Factor Investing API", version="0.4.0", lifespan=db_connect, debug=True
)


# Health Check
@app.get("/", tags=[APITags.root])
async def root():
    return {"message": "Factor Investing API is running"}


app.include_router(per_security.tickers_router)
app.include_router(bulk.tickers_router)
