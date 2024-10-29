import datetime
from abc import ABC, abstractmethod
from typing import Optional

from app.application.models.crypto_price import CryptoPrice, CryptoPriceCreate


class UoW(ABC):
    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def flush(self) -> None:
        raise NotImplementedError


class DatabaseGateway(ABC):

    @abstractmethod
    async def get_prices_by_ticker(self, ticker: str) -> list[CryptoPrice]:
        raise NotImplementedError

    @abstractmethod
    async def get_latest_price_by_ticker(self, ticker: str) -> Optional[CryptoPrice]:
        raise NotImplementedError

    @abstractmethod
    async def get_prices_by_date(
            self, ticker: str,
            start_date: Optional[datetime.datetime],
            end_date: Optional[datetime.datetime]
    ) -> list[CryptoPrice]:
        raise NotImplementedError

    @abstractmethod
    async def insert_price(self, price_data: CryptoPriceCreate) -> None:
        raise NotImplementedError

