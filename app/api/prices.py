import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Query, Depends, HTTPException

from app.application.models.crypto_price import CryptoPrice
from app.application.prices import get_prices, get_latest_price, get_prices_with_date_filter
from app.application.protocols.database import DatabaseGateway

prices_router = APIRouter()


@prices_router.get("/", response_model=list[CryptoPrice])
async def get_prices_by_ticker(
        database: Annotated[DatabaseGateway, Depends()],
        ticker: Annotated[str, Query(..., title="Ticker", example="btc_usd")],
) -> list[CryptoPrice]:
    """
    Retrieve all price records for a specified cryptocurrency ticker.
    """
    crypto_price_list = await get_prices(database, ticker)
    return crypto_price_list


@prices_router.get("/latest", response_model=CryptoPrice)
async def get_latest_price_by_ticker(
        database: Annotated[DatabaseGateway, Depends()],
        ticker: Annotated[str, Query(..., title="Ticker", example="btc_usd")],
) -> CryptoPrice:
    """
    Retrieve the latest price record for a specified cryptocurrency ticker.

    Raises:
        HTTPException: If no data is found for the specified ticker.
    """
    latest_price = await get_latest_price(database, ticker)
    if not latest_price:
        raise HTTPException(status_code=404, detail="Data not found for specified ticker.")
    return latest_price


@prices_router.get("/history", response_model=list[CryptoPrice])
async def get_prices_by_date(
        database: Annotated[DatabaseGateway, Depends()],
        ticker: Annotated[str, Query(..., title="Ticker", example="btc_usd")],
        start_date: Annotated[
            Optional[datetime.datetime],
            Query(..., title="Start Date in ISO 8601 format", example="2024-10-29T09:05:00+03:00")
        ] = None,
        end_date: Annotated[
            Optional[datetime.datetime],
            Query(..., title="End Date in ISO 8601 format", example="2024-10-29T09:05:00+03:00")
        ] = None,
) -> list[CryptoPrice]:
    """
    Retrieve price records for a specified cryptocurrency ticker within a date range.
    """
    prices = await get_prices_with_date_filter(database, ticker, start_date, end_date)
    return prices
