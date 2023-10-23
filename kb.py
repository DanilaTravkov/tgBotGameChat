from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

choose_game_menu = [
    [KeyboardButton(text='Rainbow Six Siege', callback_data='rainbow_six_siege')],
    [KeyboardButton(text='Fall guys', callback_data='fall_guys')],
    [KeyboardButton(text='Apex Legends', callback_data='apex_legends')]
]

choose_platform_menu = [
    [KeyboardButton(text='Playstation', callback_data='playstation')],
    [KeyboardButton(text='XBOX', callback_data='xbox')],
    [KeyboardButton(text='PC', callback_data='pc')]
]

help_menu = [
    [KeyboardButton(text='/start', callback_data='start')]
]

choose_game_menu = InlineKeyboardMarkup(inline_keyboard=choose_game_menu)
choose_platform_menu = InlineKeyboardMarkup(inline_keyboard=choose_platform_menu)
help = InlineKeyboardMarkup(inline_keyboard=help_menu)

exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
