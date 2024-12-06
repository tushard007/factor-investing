from fastapi import FastAPI

from investing.api.routers import bulk, per_security
from investing.core.models import APITags

app = FastAPI(title="Factor Investing API", version="0.1")


# Health Check
@app.get("/", tags=[APITags.root])
async def root():
    return {"message": "Factor Investing API is running"}


app.include_router(per_security.tickers_router)
app.include_router(bulk.tickers_router)
