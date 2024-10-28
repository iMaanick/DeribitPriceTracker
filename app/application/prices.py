from typing import Annotated, Optional

from fastapi import Depends

from app.application.models.crypto_price import CryptoPrice
from app.application.protocols.database import DatabaseGateway


async def get_prices(
        database: DatabaseGateway,
        ticker: str,
) -> list[CryptoPrice]:
    crypto_price_list = await database.get_prices_by_ticker(ticker)
    return crypto_price_list


async def get_latest_price(
        database: DatabaseGateway,
        ticker: str,
) -> Optional[CryptoPrice]:
    latest_price = await database.get_latest_price_by_ticker(ticker)
    return latest_price


async def get_prices_with_date_filter(
        database: DatabaseGateway,
        ticker: str,
        start_date: Optional[int],
        end_date: Optional[int]
) -> Optional[CryptoPrice]:
    crypto_price_list = await database.get_prices_by_date(ticker, start_date,end_date)
    return crypto_price_list
