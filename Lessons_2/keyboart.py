from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ikb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton('❤️', callback_data='like'), InlineKeyboardButton("👎", callback_data='dislike')],
    [InlineKeyboardButton('Close keyboard',callback_data='close')]

     ])
