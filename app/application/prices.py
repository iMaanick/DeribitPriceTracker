from typing import Annotated

from fastapi import Depends

from app.application.models.crypto_price import CryptoPrice
from app.application.protocols.database import DatabaseGateway


async def get_prices_by_ticker(
        database: Annotated[DatabaseGateway, Depends()],
        ticker: str,
) -> list[CryptoPrice]:
    crypto_price_list = await database.get_prices_by_ticker(ticker)
    return crypto_price_list
