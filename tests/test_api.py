from datetime import datetime
from typing import Optional

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest import fixture

from app.application.models.crypto_price import CryptoPrice, CryptoPriceCreate
from app.application.protocols.database import DatabaseGateway
from app.main.web import init_routers


class MockDatabase(DatabaseGateway):
    async def get_prices_by_ticker(self, ticker: str) -> list[CryptoPrice]:
        return [CryptoPrice(id=1, ticker=ticker, price=30000, timestamp=int(datetime.now().timestamp()))]

    async def get_latest_price_by_ticker(self, ticker: str) -> Optional[CryptoPrice]:
        if ticker == "nonexistent_ticker":
            return None
        return CryptoPrice(id=1, ticker=ticker, price=30000, timestamp=int(datetime.now().timestamp()))

    async def get_prices_by_date(self, ticker: str, start_date: Optional[datetime], end_date: Optional[datetime]) -> list[CryptoPrice]:
        return [CryptoPrice(id=1, ticker=ticker, price=30000, timestamp=int(datetime.now().timestamp()))]

    async def insert_price(self, price_data: CryptoPriceCreate) -> None:
        pass


@fixture
async def mock_db() -> MockDatabase:
    return MockDatabase()


@fixture
def client(mock_db: MockDatabase) -> TestClient:
    app = FastAPI()
    init_routers(app)
    app.dependency_overrides[DatabaseGateway] = lambda: mock_db
    return TestClient(app)


@pytest.mark.asyncio
async def test_get_prices_by_ticker(client: TestClient) -> None:
    params = {
        "ticker": "btc_usd",
    }
    response = client.get("/prices", params=params)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['ticker'] == 'btc_usd'


@pytest.mark.asyncio
async def test_get_prices_by_ticker_missing_param(client: TestClient) -> None:
    params = {}
    response = client.get("/prices", params=params)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_latest_price_by_ticker(client: TestClient) -> None:
    params = {
        "ticker": "btc_usd",
    }
    response = client.get("/prices/latest", params=params)
    assert response.status_code == 200
    assert response.json()['ticker'] == 'btc_usd'
    assert response.json()['price'] == 30000


@pytest.mark.asyncio
async def test_get_latest_price_not_found(client: TestClient) -> None:
    params = {
        "ticker": "nonexistent_ticker",
    }
    response = client.get("/prices/latest", params=params)
    assert response.status_code == 404
    assert response.json() == {"detail": "Data not found for specified ticker."}


@pytest.mark.asyncio
async def test_get_prices_by_date(client: TestClient) -> None:
    start_date = "2024-10-29T09:05:00+03:00"
    end_date = "2024-10-29T09:05:00+03:00"
    params = {
        "ticker": "btc_usd",
        "start_date": start_date,
        "end_date": end_date
    }
    response = client.get("/prices/history", params=params)
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]['ticker'] == 'btc_usd'


@pytest.mark.asyncio
async def test_get_prices_by_date_invalid(client: TestClient) -> None:
    start_date = "invalid-date"
    end_date = "invalid-date"
    params = {
        "ticker": "btc_usd",
        "start_date": start_date,
        "end_date": end_date
    }
    response = client.get("/prices/history", params=params)
    assert response.status_code == 422
    assert "detail" in response.json()
