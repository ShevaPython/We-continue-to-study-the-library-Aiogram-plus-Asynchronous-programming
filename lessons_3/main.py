from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
import os
import setings
import logging

"""CallbackData

- Шаблон для создания шаблона в котором мы будем генерировать callback.data
- cd.filter() Для фильтрования callback запросов которые сгенерированы по нашему шаблону
- cd.new("push") для создания какого либо действия

"""

logging.basicConfig(level=logging.INFO)

bot = Bot(os.getenv("TOKEN"))
db = Dispatcher(bot)

cd = CallbackData('ikb', 'action')
ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Button', callback_data=cd.new("push"))]
])


@db.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Hello", reply_markup=ikb)


@db.callback_query_handler(cd.filter())
async def ikb_callback(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['action'] == 'push':
        await callback.answer("OOOppps")


if __name__ == "__main__":
    executor.start_polling(db, skip_updates=True)
