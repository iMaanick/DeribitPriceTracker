from typing import Annotated

from fastapi import APIRouter, Query, Depends, HTTPException

from app.application.prices import get_prices, get_latest_price
from app.application.protocols.database import DatabaseGateway

prices_router = APIRouter()


@prices_router.get("/")
async def get_prices_by_ticker(
        database: Annotated[DatabaseGateway, Depends()],
        ticker: str = Query(...),
):
    crypto_price_list = await get_prices(database, ticker)
    if not crypto_price_list:
        raise HTTPException(status_code=404, detail="Data not found for specified ticker.")
    return crypto_price_list


@prices_router.get("/latest")
async def get_latest_price_by_ticker(
        database: Annotated[DatabaseGateway, Depends()],
        ticker: str = Query(...),
):
    latest_price = await get_latest_price(database, ticker)
    if not latest_price:
        raise HTTPException(status_code=404, detail="Data not found for specified ticker.")
    return latest_price
