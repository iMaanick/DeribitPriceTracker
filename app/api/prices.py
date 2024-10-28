from typing import Annotated

from fastapi import APIRouter, Query, Depends, HTTPException

from app.application.protocols.database import DatabaseGateway

prices_router = APIRouter()


@prices_router.get("/")
async def get_prices_by_ticker(
        database: Annotated[DatabaseGateway, Depends()],
        ticker: str = Query(...),
):
    crypto_price_list = await database.get_prices_by_ticker(ticker)
    if not crypto_price_list:
        raise HTTPException(status_code=404, detail="Data not found for specified ticker.")
    return crypto_price_list
