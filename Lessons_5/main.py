from aiogram import Bot, executor, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup, StatesGroupMeta
import logging
import setings
import os

"""
Aiogram FSM машина состояния для бота

- Это алгоритм,который имеет некоторое состояния,которое может изменяться путем данных!
- db = Dispatcher(bot,storage= -Хранилище MemoryStorage)
- message.photo[0].file_id - индитификатор фотографии
-  async with state.proxy() as data открываем храннилище
"""

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(os.getenv('TOKEN'))
db = Dispatcher(bot, storage=storage)


class ClientStateGrope(StatesGroup):
    photo = State()
    description = State()


def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("Начать работу!")
    )
    return kb


def get_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))


@db.message_handler(commands=['start'])
async def command_start(message: types.Message) -> None:
    await message.answer(text=F"Hello {message.from_user.username}",
                         reply_markup=get_kb())


@db.message_handler(commands=['cancel'], state='*')
async def command_start(message: types.Message, state: FSMContext) -> None:
    current_state =  await state.get_state()
    if current_state is None:
        return
    await message.reply('Отменил',reply_markup=get_kb())
    await state.finish()


@db.message_handler(Text(equals="Начать работу!", ignore_case=Text), state=None)
async def go_work(message: types.Message) -> None:
    await ClientStateGrope.photo.set()
    await message.answer('Сначала отправь нам фотографию',
                         reply_markup=get_cancel())


@db.message_handler(lambda message: not message.photo, state=ClientStateGrope.photo)
async def ckeck_photo(message: types.Message):
    return await message.reply('Это не фотография')


@db.message_handler(lambda message: message.photo, state=ClientStateGrope.photo, content_types=['photo'])
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await ClientStateGrope.next()
    await message.reply('А теперь отправь нам описание!')


@db.message_handler(state=ClientStateGrope.description)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await message.reply('Ваша фотография сохранена!')

    async with state.proxy() as data:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=data['photo'],
                             caption=data['description'])
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(db, skip_updates=True)
