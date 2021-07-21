from config import ADMINS
from main import dp, bot
from aiogram.types import Message
from market_api import Market

@dp.message_handler()
async def get_item_info(message: Message):
    mark = await Market.get_item(message.text)
    text = mark.items.items_str

    if message.from_user.id not in ADMINS:
        return 0

    if text == '':
        return await message.answer('Не найдено')

    return await message.answer(mark.items.items_str)
