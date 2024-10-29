import asyncio
from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from aioresponses import aioresponses

from app.application.models.crypto_price import CryptoPriceCreate
from app.deribit_client.client import DeribitClient


@pytest.fixture
def mock_db() -> AsyncMock:
    return AsyncMock()


@pytest_asyncio.fixture
async def deribit_client(mock_db: AsyncMock) -> AsyncGenerator[DeribitClient, None]:
    client = DeribitClient(db=mock_db)
    await client.start()
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_fetch_price_success(deribit_client: DeribitClient) -> None:
    ticker = "btc_usd"
    price = 30000.0

    with aioresponses() as mock_response:
        mock_response.get(
            f"{DeribitClient.BASE_URL}?index_name={ticker}",
            payload={"result": {"index_price": price}},
            status=200
        )

        result = await deribit_client.fetch_price(ticker)

        assert result is not None
        assert isinstance(result, CryptoPriceCreate)
        assert result.ticker == ticker
        assert result.price == price
        assert isinstance(result.timestamp, int)


@pytest.mark.asyncio
async def test_fetch_price_error_response(deribit_client: DeribitClient) -> None:
    ticker = "btc_usd"

    with aioresponses() as mock_response:
        mock_response.get(
            f"{DeribitClient.BASE_URL}?index_name={ticker}",
            status=500
        )

        result = await deribit_client.fetch_price(ticker)
        assert result is None


@pytest.mark.asyncio
async def test_fetch_price_invalid_data(deribit_client: DeribitClient) -> None:
    ticker = "btc_usd"

    with aioresponses() as mock_response:
        mock_response.get(
            f"{DeribitClient.BASE_URL}?index_name={ticker}",
            payload={"result": {"unexpected_key": 12345}},
            status=200
        )

        result = await deribit_client.fetch_price(ticker)
        assert result is None


@pytest.mark.asyncio
async def test_fetch_and_save(deribit_client: DeribitClient, mock_db: AsyncMock) -> None:
    ticker_btc = "btc_usd"
    price_btc = 30000.0
    ticker_eth = "eth_usd"
    price_eth = 2000.0

    with aioresponses() as mock_response:
        mock_response.get(
            f"{DeribitClient.BASE_URL}?index_name={ticker_btc}",
            payload={"result": {"index_price": price_btc}},
            status=200
        )
        mock_response.get(
            f"{DeribitClient.BASE_URL}?index_name={ticker_eth}",
            payload={"result": {"index_price": price_eth}},
            status=200
        )

        await deribit_client.fetch_and_save()
        assert mock_db.insert_price.call_count == 2
        mock_db.insert_price.assert_any_call(
            CryptoPriceCreate(
                ticker="btc_usd",
                price=price_btc,
                timestamp=mock_db.insert_price.call_args[0][0].timestamp
            )
        )
        mock_db.insert_price.assert_any_call(
            CryptoPriceCreate(
                ticker="eth_usd",
                price=price_eth,
                timestamp=mock_db.insert_price.call_args[0][0].timestamp
            )
        )


@pytest.mark.asyncio
async def test_start_polling(deribit_client: DeribitClient, mock_db: AsyncMock) -> None:
    with patch.object(DeribitClient, 'fetch_and_save', new_callable=AsyncMock) as mock_fetch_and_save:
        task = asyncio.create_task(deribit_client.start_polling())
        await asyncio.sleep(1)

        task.cancel()
        await asyncio.gather(task, return_exceptions=True)

        assert mock_fetch_and_save.call_count > 0
