import asyncio
import logging

from app.deribit_client.client import DeribitClient
from app.adapters.sqlalchemy_db.gateway import SqlaGateway
from app.main.di import create_session_maker, new_session


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    session_maker = create_session_maker()
    async with session_maker() as async_session:

        db_gateway = SqlaGateway(async_session)
        client = DeribitClient(db=db_gateway)
        try:
            await client.start()
            await client.start_polling()
        finally:
            await client.close()

if __name__ == "__main__":
    asyncio.run(main())