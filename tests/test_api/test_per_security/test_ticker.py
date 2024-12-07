import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_exchange() -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/per-security/")
        assert response.status_code == 200
        assert "nse" in response.json()


@pytest.mark.asyncio
async def test_ticker_info():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/per-security/nse/tcs")
        assert response.status_code == 200
        result = response.json()
        assert result["longName"] == "Tata Consultancy Services Limited"


@pytest.mark.asyncio
async def test_ticker_history():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(
            "/per-security/nse/tcs/history",
            params={"interval": "1m", "period": "1d"},
        )
        assert response.status_code == 200
        result = response.json()
        assert "Close" in result[0]
