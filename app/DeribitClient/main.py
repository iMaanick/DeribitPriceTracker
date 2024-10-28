import asyncio

from app.DeribitClient.client import DeribitClient


async def main():
    db = None
    client = DeribitClient(db=db)
    try:
        await client.start()
        await client.start_polling(interval=5)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())