from aiogram import Bot, executor, types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from random import randint
import setings
import logging
import os

logging.basicConfig(level=logging.INFO)

bot = Bot(os.getenv("TOKEN"))
db = Dispatcher(bot)


def get_inline_keyboard() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Increase", callback_data="btn_increase"),
         InlineKeyboardButton(text="Decrease", callback_data="btn_decrease")],
        [InlineKeyboardButton(text="Randon_number", callback_data='btn_random_number')]

    ])
    return ikb


number = 0


@db.message_handler(commands='start')
async def command_start(message: types.Message):
    await message.answer(text=F"The current number is : {number}",
                         reply_markup=get_inline_keyboard())


@db.callback_query_handler(lambda callback_query: str(callback_query.data.startswith('btn_')))
async def ikb_callback_count(callback: types.CallbackQuery):
    global number
    if callback.data == "btn_increase":
        number += 1
        await callback.message.edit_text(text=F"The current number is  : {number}", reply_markup=get_inline_keyboard())
    elif callback.data == "btn_decrease":
        number -= 1
        await callback.message.edit_text(text=F"The current number is  : {number}", reply_markup=get_inline_keyboard())
    elif callback.data == "btn_random_number":
        number = randint(1, 10000)
        await callback.message.edit_text(text=F"The current random_number is  : {number}",
                                         reply_markup=get_inline_keyboard())
    else:
        1 / 0


if __name__ == "__main__":
    executor.start_polling(db,
                           skip_updates=True)
