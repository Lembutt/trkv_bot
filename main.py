import asyncio
import pathlib
import os

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import BOT_TOKEN
from loader import db


# Луп из asyncio
loop = asyncio.get_event_loop()

# Всякая магия из aiogram
bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(
    bot,
    loop=loop,
    storage=JSONStorage(
        path=os.path.join(
            pathlib.Path(__file__).parent,
            'temp/storage.json'
        )
    )
)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dispatcher: Dispatcher):
    await db.setup()


async def on_shutdown(dispatcher: Dispatcher):
    await db.pool.close()


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
