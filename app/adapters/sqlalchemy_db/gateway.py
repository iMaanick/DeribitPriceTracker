from typing import Optional

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.models.crypto_price import CryptoPrice
from app.application.protocols.database import DatabaseGateway
from app.adapters.sqlalchemy_db import models


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_prices_by_ticker(self, ticker: str) -> list[CryptoPrice]:
        query = select(models.CryptoPrice).where(models.CryptoPrice.ticker == ticker)
        result = await self.session.execute(query)
        crypto_price_list = [CryptoPrice.model_validate(crypto_price) for crypto_price in result.scalars().all()]
        return crypto_price_list

    async def get_latest_price_by_ticker(self, ticker: str) -> Optional[CryptoPrice]:
        query = select(models.CryptoPrice).where(
            models.CryptoPrice.ticker == ticker
        ).order_by(desc(models.CryptoPrice.timestamp))
        result = await self.session.execute(query)
        latest_price = result.scalars().first()
        return latest_price

    async def get_prices_by_date(
            self, ticker: str,
            start_date: Optional[int],
            end_date: Optional[int]
    ) -> list[CryptoPrice]:

        query = select(models.CryptoPrice).where(models.CryptoPrice.ticker == ticker)

        if start_date:
            query = query.where(models.CryptoPrice.timestamp >= start_date)

        if end_date:
            query = query.where(models.CryptoPrice.timestamp <= end_date)

        result = await self.session.execute(query)
        crypto_price_list = [CryptoPrice.model_validate(crypto_price) for crypto_price in result.scalars().all()]
        return crypto_price_list
