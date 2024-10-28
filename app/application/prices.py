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
