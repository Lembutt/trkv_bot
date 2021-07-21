from config import ADMINS
from main import dp, bot
from aiogram.types import Message
from utils.market_api import Market

@dp.message_handler(commands=['start'])
async def hello_message(message: Message):
    if message.from_user.id not in ADMINS:
        return 0
    await message.answer(f'Ну че, здорова, {message.from_user.first_name} {message.from_user.last_name}\n\nЩа к барыгам, короче, а потом по бабам:)')

@dp.message_handler()
async def get_item_info(message: Message):
    mark = await Market.get_item(message.text)
    text = mark.items.items_str

    if message.from_user.id not in ADMINS:
        return 0

    if text == '':
        return await message.answer('Не найдено')

    return await message.answer(mark.items.items_str)
