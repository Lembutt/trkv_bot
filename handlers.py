from config import ADMINS
from main import dp, bot
from aiogram.types import Message, CallbackQuery
from utils.market_api import Market
from utils.processes.checklist import process_checklist, make_checklist_keyboard
from utils.callbacks import checklist_cb


@dp.message_handler(commands=['start'])
async def hello_message(message: Message):
    if message.from_user.id not in ADMINS:
        return 0
    await message.answer(f'Ну че, здорова, {message.from_user.first_name} {message.from_user.last_name}\n\nЩа к барыгам, короче, а потом по бабам:)')
    items = await Market.get_all_items()

@dp.message_handler(commands=['check'])
async def start_check_list(message: Message):
    if message.from_user.id not in ADMINS:
        return 0
    return await message.answer(
        text='Ну че, пора в рейд собираться!',
        reply_markup=await make_checklist_keyboard()
    )


@dp.callback_query_handler(checklist_cb.filter())
async def handle_checklist_cb(query: CallbackQuery, callback_data: dict):
    to_raid, markup, text = await process_checklist(cb_data=callback_data)
    try:
        await query.message.edit_text(text=text, reply_markup=markup)
    except Exception as e:
        pass


@dp.message_handler()
async def get_item_info(message: Message):
    mark = await Market.get_item(message.text)
    text = mark.items.items_str

    if message.from_user.id not in ADMINS:
        return 0

    if text == '':
        return await message.answer('Не найдено')

    return await message.answer(mark.items.items_str)
