import asyncio
import logging
from datetime import datetime
from typing import Optional

import aiohttp

from app.application.models.crypto_price import CryptoPriceCreate
from app.application.protocols.database import DatabaseGateway


class DeribitClient:
    BASE_URL = "https://www.deribit.com/api/v2/public/get_index_price"

    def __init__(self, db: DatabaseGateway):
        self.db = db
        self.session: Optional[aiohttp.ClientSession] = None

    async def start(self):
        self.session = aiohttp.ClientSession()

    async def close(self):
        if self.session:
            await self.session.close()

    async def fetch_price(self, currency: str) -> Optional[CryptoPriceCreate]:
        url = f"{self.BASE_URL}?index_name={currency}"
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return CryptoPriceCreate(
                        ticker=currency,
                        price=data['result']['index_price'],
                        timestamp=int(datetime.utcnow().timestamp())
                    )
                else:
                    logging.error(f"Error fetching {currency} price: {response.status}")
                    return None
        except Exception as e:
            logging.error(f"Exception while fetching {currency} price: {e}")
            return None

    async def fetch_and_save(self):
        currencies = ["btc_usd", "eth_usd"]
        tasks = [self.fetch_price(currency) for currency in currencies]
        results = await asyncio.gather(*tasks)

        for result in results:
            if isinstance(result, CryptoPriceCreate):
                await self.db.insert_price(result)
            elif isinstance(result, BaseException):
                logging.error(f"Error occurred: {result}")

    async def start_polling(self, interval: int = 60):
        while True:
            await self.fetch_and_save()
            await asyncio.sleep(interval)
