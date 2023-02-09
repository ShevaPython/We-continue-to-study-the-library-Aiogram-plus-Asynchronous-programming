"""Program mode 1
Finite-state-machine
"""
from aiogram import Bot, executor, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
import setings
import os

storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(os.getenv('TOKEN'))
db = Dispatcher(bot, storage=storage)


class ProfileStateGroup(StatesGroup):
    photo = State()
    name = State()
    age = State()
    description = State()


def get_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton("/create")
    )
    return kb


def get_kb_cancel() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("/cansel"))
    return kb


@db.message_handler(commands=['start'])
async def command_start(message: types.Message) -> None:
    await message.answer(
        text=F"Привет {message.from_user.full_name}!Что-бы создать ваш профиль введите команду /create",
        reply_markup=get_kb())


@db.message_handler(commands=['cansel'], state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.reply("Вы прервали создания анкеты", reply_markup=get_kb())


@db.message_handler(commands=['create'])
async def command_create(message: types.Message) -> None:
    await message.answer(
        text=F"Давай создадим наш профиль!Отправь мне свою фотографию -> 📷",
        reply_markup=get_kb_cancel())
    await ProfileStateGroup.photo.set()


@db.message_handler(lambda message: not message.photo, state=ProfileStateGroup.photo)
async def check_photo(message: types.Message):
    await message.reply(text=F"Это не фото,не обманывай!")


@db.message_handler(content_types=['photo'], state=ProfileStateGroup.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id

    await message.answer(text='Теперь отправь свое имя!')
    await ProfileStateGroup.next()


@db.message_handler(lambda message: not message.text.isalpha(),
                    state=ProfileStateGroup.name)
async def check_name(message: types.Message):
    await message.reply(text=F"Имя должно состоять только из букв!")


@db.message_handler(state=ProfileStateGroup.name)
async def save_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer(text='Введите свой возраст!')
    await ProfileStateGroup.next()


@db.message_handler(lambda message: not message.text.isdigit() or float(message.text) > 120 or float(message.text) < 5,
                    state=ProfileStateGroup.age)
async def check_age(message: types.Message):
    await message.reply(text=F"Возраст должен состоять только из цыфр!И быть реальным")


@db.message_handler(state=ProfileStateGroup.age)
async def save_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text

    await message.answer(text='А теперь расскажи немного о себе.')
    await ProfileStateGroup.next()


@db.message_handler(state=ProfileStateGroup.description)
async def save_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

    await message.answer(text='Ваши данные сохранены.Спасибо)')
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=data['photo'],
                         caption=F"Имя: {data['name']}\n Ваш возраст :{data['age']}\n Описанние :{data['description']}")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(db, skip_updates=True)
