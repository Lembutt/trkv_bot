import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import BOT_TOKEN


# Луп из asyncio
loop = asyncio.get_event_loop()

# Всякая магия из aiogram
bot = Bot(BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(
        dp,
        skip_updates=True
    )
