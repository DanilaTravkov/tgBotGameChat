from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

choose_game_menu = [
    [KeyboardButton(text='Rainbow Six Siege', callback_data='game_rainbow_six_siege')],
    [KeyboardButton(text='Fall guys', callback_data='game_fall_guys')],
    [KeyboardButton(text='Apex Legends', callback_data='game_apex_legends')]
]

choose_platform_menu = [
    [KeyboardButton(text='Playstation', callback_data='plat_playstation')],
    [KeyboardButton(text='XBOX', callback_data='plat_xbox')],
    [KeyboardButton(text='PC', callback_data='plat_pc')]
]

help_menu = [
    [KeyboardButton(text='/start', callback_data='start')]
]

accept_button = [
    [KeyboardButton(text='Принять заказ', callback_data='accepted')]
]

choose_game_menu = InlineKeyboardMarkup(inline_keyboard=choose_game_menu)
choose_platform_menu = InlineKeyboardMarkup(inline_keyboard=choose_platform_menu)
help = InlineKeyboardMarkup(inline_keyboard=help_menu)
accept_button = InlineKeyboardMarkup(inline_keyboard=accept_button)

exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
