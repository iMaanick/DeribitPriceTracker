from typing import Annotated, Optional

from fastapi import APIRouter, Query, Depends

from app.application.prices import get_prices, get_latest_price, get_prices_with_date_filter
from app.application.protocols.database import DatabaseGateway

prices_router = APIRouter()


@prices_router.get("/")
async def get_prices_by_ticker(
        database: Annotated[DatabaseGateway, Depends()],
        ticker: Annotated[str, Query(..., title="Ticker", example="btc_usd")],
):
    crypto_price_list = await get_prices(database, ticker)
    return crypto_price_list


@prices_router.get("/latest")
async def get_latest_price_by_ticker(
        database: Annotated[DatabaseGateway, Depends()],
        ticker: Annotated[str, Query(..., title="Ticker", example="btc_usd")],
):
    latest_price = await get_latest_price(database, ticker)
    return latest_price


@prices_router.get("/by-date")
async def get_prices_by_date(
        database: Annotated[DatabaseGateway, Depends()],
        ticker: Annotated[str, Query(..., title="Ticker", example="btc_usd")],
        start_date: Annotated[Optional[int], Query(..., title="Start Date in UNIX timestamp")] = None,
        end_date: Annotated[Optional[int], Query(..., title="End Date in UNIX timestamp")] = None,
):
    prices = await get_prices_with_date_filter(database, ticker, start_date, end_date)
    return prices
