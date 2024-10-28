from abc import ABC, abstractmethod
from typing import Optional

from app.application.models import User
from app.application.models.crypto_price import CryptoPrice


class UoW(ABC):
    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def flush(self):
        raise NotImplementedError


class DatabaseGateway(ABC):
    @abstractmethod
    async def add_user(self, user: User) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_prices_by_ticker(self, ticker: str) -> list[CryptoPrice]:
        raise NotImplementedError

    @abstractmethod
    async def get_latest_price_by_ticker(self, ticker: str) -> Optional[CryptoPrice]:
        raise NotImplementedError
