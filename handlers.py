from aiogram import types, F, Router, Bot
from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, CommandObject
from aiogram import flags, html
from aiogram.fsm.context import FSMContext
from datetime import datetime

import logging

import kb
import text
import utils

from states import CallBackOnStart

import json

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):

    if message.chat.id > 0:

        current_user_id = message.from_user.id

        with open('users_list.json', 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)
            for elem in data:
                if elem.get('id') == current_user_id: # Проверяем проходил ли пользователь опрос раньше
                    user = False
                    break
                else:
                    user = True
            # except FileNotFoundError or json.decoder.JSONDecodeError:
            #     mock_data = [{"id": 1}]
            #     json.dump(mock_data, json_file, indent=4)
        if user:
            await state.set_state(CallBackOnStart.name)
            await message.answer("Как я могу к вам обращаться?", reply_markup=ReplyKeyboardRemove())
        else:
            await message.answer(text="Вы уже проходили тест. Чтобы зарегистрировать новый заказ подождите некоторое время, пока бустеры отвят на ваш последний запрос.")
            await state.clear()

@router.message(CallBackOnStart.name)
async def choose_game(message: types.Message, state: FSMContext):

    if message.chat.id > 0:

        name = message.text
        await state.update_data(name=name)
        await state.set_state(CallBackOnStart.game)
        await message.answer(text=f"Очень приятно {name}! Теперь выберите игру", reply_markup=kb.choose_game_menu)

@router.callback_query(CallBackOnStart.game)
async def choose_platform(callback_query: CallbackQuery, state: FSMContext):

    game = callback_query.data

    await state.update_data(game=game)
    await state.set_state(CallBackOnStart.poll)
    await callback_query.message.answer(text=f"Вы выбрали {game}, теперь выберите платформу", reply_markup=kb.choose_platform_menu)

@router.callback_query(CallBackOnStart.poll)
async def handle_poll(callback: CallbackQuery, state: FSMContext):
    platform = callback.data

    data = await state.get_data()
    game = data.get("game") 
    
    await state.update_data(platform=platform)
    if game == 'rainbow_six_siege':
        await callback.message.answer(
            text=f"Вы выбрали {platform}, остался последний штрих, ответьте на следующие вопросы через пробел\n\n\
1. Впишите ваш текущий ранг\n\
2. Впишите желаемый ранг\n\
3. Впишите количество получаемых очков за игру",
            )
    elif game == 'fall_guys':
        await callback.message.answer(
            text=f"Вы выбрали {platform}, остался последний штрих, ответьте на следующий вопрос\n\n\
1. Впишите количество желаемых побед"
            )
    elif game == 'apex_legends':
        await callback.message.answer(
            text=f"Вы выбрали {platform}, остался последний штрих, ответьте на следующий вопрос\n\n\
1. Впишите ваш текущий ранг\n\
2. Впишите желаемый ранг"   
            )

@router.message(CallBackOnStart.poll)
async def handle_finish(message: types.Message, bot: Bot, state: FSMContext):

    if message.chat.id > 0:
        data = await state.get_data()
        name = data.get("name")
        game = data.get("game") 
        platform = data.get("platform")
        poll = message.text
        timestamp = datetime.today().strftime('%Y:%m:%d')

        try:
            with open('users_list.json', 'r', encoding="utf-8") as json_file:
                user_data = json.load(json_file)
        except FileNotFoundError:
            user_data = []

    # Добавьте новые данные в список
        new_data = {
            "id": message.from_user.id, 
            "username": name,
            "game": game,
            "platform": platform,
            "game_poll": str(poll),
            "timestamp": timestamp
        }
        user_data.append(new_data)

    # Сохраните обновленные данные в файл
        with open('users_list.json', 'w', encoding="utf-8") as json_file:
            json.dump(user_data, json_file, ensure_ascii=False, indent=4)

        await state.update_data(poll=poll)
        await bot.send_message(
            chat_id=-1002054102871, text=f"\
Поступил новый заказ!\n\n\
От: {name}\n\
Игра: {game}\n\
Платформа: {platform}\n\
Доп.информация: {str(poll)}\n\
Дата: {timestamp}\
    "
        )
        await message.answer(
            text='Спасибо за формирование заказа, наш геймер-исполнитель свяжется с вами в ближайшее время для подтверждения заказа и проведения оплаты',
        )
        await state.clear()

@router.message(Command("help"))
async def help(message: types.Message):
    if message.chat.id > 0:
        await message.reply('Меню help', reply_markup=kb.help)

@router.message(F.text)
async def wrong_message_handler(message: types.Message):
    if message.chat.id > 0:
        await message.answer(
            'Вы ввели что-то непонятное, попробуйте снова?\n\n<b>Помощь</b>: /help'
        )




        




