from aiogram import Bot, executor, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, \
    InputTextMessageContent
from aiogram.utils.callback_data import CallbackData
import hashlib
import setings
import logging
import os

"""Inline Bot

- Inline режим телеграм бота
- Бот который помогает нам создать какое либо сообщения от нашего имени
- /setinline в BotFather что бы перевести бота в  инлайн режим
- InlineQuery -это запрос который генерируеться ,когда пользователь обращаеться к инлайн боту отправляя текст!
- InlineQuery in API telegram -это класс,результатом которого являеться его экземпляр-конкретный запрос сформированый
  при отправки пользователем текста,через обращения к инлайн Боту!
- Echo InlineBotzxq1
"""
logging.basicConfig(level=logging.INFO)
bot = Bot(os.getenv('TOKEN'))
db = Dispatcher(bot)
cb_daata = CallbackData('ikb', 'action')  # pattern


def ikb_inline() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Button_1', callback_data=cb_daata.new('push_button1'))],
        [InlineKeyboardButton('Button_2', callback_data=cb_daata.new('push_button2'))]
    ])

    return ikb


@db.message_handler(commands=["start"])
async def command_start(message: types.Message):
    await message.answer(text="Hello i am aiogram bot",
                         reply_markup=ikb_inline())


@db.callback_query_handler(cb_daata.filter(action='push_button1'))
async def callback_push1(callback: types.CallbackQuery):
    await callback.answer(text='Hello')


@db.callback_query_handler(cb_daata.filter(action='push_button2'))
async def callback_push2(callback: types.CallbackQuery):
    await callback.answer(text='World')


# Inline query_handler
@db.inline_handler()  # process InlineQuery is foomed telegram API
async def inline_echo(inline_query: types.InlineQuery):
    text = inline_query.query or 'Echo'  # text от пользователя
    input_content = InputTextMessageContent(text)  # формируем контент echo сообщения
    result_id = hashlib.md5(text.encode()).hexdigest()  # уникальный ID

    item = InlineQueryResultArticle(

        input_message_content=input_content,
        id=result_id,
        title='Echo!!!'

    )

    await bot.answer_inline_query(inline_query_id=inline_query.id,
                                  results=[item],
                                  cache_time=1)


if __name__ == "__main__":
    executor.start_polling(db, skip_updates=True)
