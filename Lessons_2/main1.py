from aiogram import Bot, executor, Dispatcher, types
from keyboart import ikb
import os
from pprint import pprint

"""
Структура callback запросов

{"id": "2574338545590195009",
                      "from": {"id": 599384900, "is_bot": false, "first_name": "Сергій", "last_name": "Шевцов",
                               "username": "Sergey_ShevaA", "language_code": "ru"}, "message": {"message_id": 43,
                                                                                                "from": {
                                                                                                    "id": 5999708408,
                                                                                                    "is_bot": true,
                                                                                                    "first_name": "AsincoTeleBot",
                                                                                                    "username": "AsincoTeleBot"},
                                                                                                "chat": {
                                                                                                    "id": 599384900,
                                                                                                    "first_name": "Сергій",
                                                                                                    "last_name": "Шевцов",
                                                                                                    "username": "Sergey_ShevaA",
                                                                                                    "type": "private"},
                                                                                                "date": 1675683305,
                                                                                                "photo": [{
                                                                                                    "file_id": "AgACAgQAAxkDAAMrY-Dl6RVPgljtK-nJzFLeroLc_pAAAi-wMRugoNRSk24VsivkZcUBAAMCAANzAAMuBA",
                                                                                                    "file_unique_id": "AQADL7AxG6Cg1FJ4",
                                                                                                    "file_size": 1000,
                                                                                                    "width": 90,
                                                                                                    "height": 60},
                                                                                                    {
                                                                                                        "file_id": "AgACAgQAAxkDAAMrY-Dl6RVPgljtK-nJzFLeroLc_pAAAi-wMRugoNRSk24VsivkZcUBAAMCAANtAAMuBA",
                                                                                                        "file_unique_id": "AQADL7AxG6Cg1FJy",
                                                                                                        "file_size": 11384,
                                                                                                        "width": 320,
                                                                                                        "height": 214},
                                                                                                    {
                                                                                                        "file_id": "AgACAgQAAxkDAAMrY-Dl6RVPgljtK-nJzFLeroLc_pAAAi-wMRugoNRSk24VsivkZcUBAAMCAAN4AAMuBA",
                                                                                                        "file_unique_id": "AQADL7AxG6Cg1FJ9",
                                                                                                        "file_size": 33156,
                                                                                                        "width": 626,
                                                                                                        "height": 418}],
                                                                                                "caption": "Нравиться ли тебе фото?",
                                                                                                "reply_markup": {
                                                                                                    "inline_keyboard": [
                                                                                                        [{"text": "❤️",
                                                                                                          "callback_data": "like"},
                                                                                                         {"text": "👎",
                                                                                                          "callback_data": "dislike"}]]}},
                      "chat_instance": "8204641450092674517", "data": "like"}
 

"""
bot = Bot(os.getenv('TOKEN'))
db = Dispatcher(bot)
is_voted = False


@db.message_handler(commands=['start'])
async def send_start(message: types.Message) -> None:
    await bot.send_photo(chat_id=message.chat.id,
                         photo='https://ru.freepik.com/free-photo/rear-view-of-programmer-working-all-night-long_5698334.htm#query=programmer&position=1&from_view=keyword',
                         caption="Нравиться ли тебе фото?",
                         reply_markup=ikb)
    await message.delete()




@db.callback_query_handler(text='close')
async def ikb_handler_close(callback: types.CallbackQuery)->None:
    await callback.message.delete()

@db.callback_query_handler()
async def ikb_handler(callback: types.CallbackQuery):
    global is_voted
    if not is_voted:
        if callback.data == 'like':
            await callback.answer(text='Тебе понравилась фотография',
                                  show_alert=True)
            is_voted = not is_voted #client is voted
        else:
            await callback.answer(text='Тебе не понравилась фотография',
                                  show_alert=True)
            is_voted = not is_voted
    await callback.answer(F"Ты уже проголосовал",
                          show_alert=True)

if __name__ == "__main__":
    executor.start_polling(db, skip_updates=True)
