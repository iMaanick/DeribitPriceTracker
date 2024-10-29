import asyncio
import logging
from datetime import datetime
from typing import Optional

import aiohttp

from app.application.models.crypto_price import CryptoPriceCreate
from app.application.protocols.database import DatabaseGateway


class DeribitClient:
    BASE_URL = "https://www.deribit.com/api/v2/public/get_index_price"
    TICKERS = ["btc_usd", "eth_usd"]

    def __init__(self, db: DatabaseGateway, interval: int = 60):
        self.db = db
        self.interval = interval
        self.session: Optional[aiohttp.ClientSession] = None

    async def start(self):
        self.session = aiohttp.ClientSession()

    async def close(self):
        if self.session:
            await self.session.close()

    async def fetch_price(self, ticker: str) -> Optional[CryptoPriceCreate]:
        params = {"index_name": ticker}
        try:
            async with self.session.get(self.BASE_URL, params=params) as response:
                if response.status != 200:
                    logging.error(f"Error getting price {ticker}: status {response.status}")
                    return None

                data = await response.json()
                price = data.get("result", {}).get("index_price")
                if price is None:
                    logging.error(f"Incorrect data for {ticker}")
                    return None

                return CryptoPriceCreate(
                    ticker=ticker,
                    price=price,
                    timestamp=int(datetime.now().timestamp())
                )
        except aiohttp.ClientError as e:
            logging.error(f"Network error while getting price {ticker}: {e}")
        except Exception as e:
            logging.error(f"Error getting price {ticker}: {e}")
        return None

    async def fetch_and_save(self):
        tasks = [self.fetch_price(ticker) for ticker in self.TICKERS]
        results = await asyncio.gather(*tasks)

        for result in results:
            if isinstance(result, CryptoPriceCreate):
                await self.db.insert_price(result)
            elif isinstance(result, BaseException):
                logging.error(f"Error occurred: {result}")

    async def start_polling(self):
        while True:
            await self.fetch_and_save()
            await asyncio.sleep(self.interval)
