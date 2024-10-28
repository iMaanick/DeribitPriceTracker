from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.models import User
from app.application.models.crypto_price import CryptoPrice
from app.application.protocols.database import DatabaseGateway
from app.adapters.sqlalchemy_db import models


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self, user: User) -> None:
        # self.session.add(user)
        print(user)
        return

    async def get_prices_by_ticker(self, ticker: str) -> list[CryptoPrice]:
        query = select(models.CryptoPrice).where(models.CryptoPrice.ticker == ticker)
        result = await self.session.execute(query)
        crypto_price_list = [CryptoPrice.model_validate(crypto_price) for crypto_price in result.scalars().all()]
        return crypto_price_list
