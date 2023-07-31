import asyncio
from loguru import logger

from src.app import start_app


async def main():
    await start_app()


if __name__ == "__main__":
    logger.info("Start main!")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

