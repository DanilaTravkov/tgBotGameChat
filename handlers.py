from aiogram import types, F, Router, Bot
from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, CommandObject
from aiogram import flags, html
from aiogram.fsm.context import FSMContext

import logging

import kb
import text
import utils

from states import CallBackOnStart

import json

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):

    current_user_id = message.from_user.id

    with open('users_list.json', 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)
        for elem in data:
            if elem.get('id') == current_user_id: # Проверяем проходил ли пользователь опрос раньше
                user = False
                break
            else:
                user = True
    if user:
        await state.set_state(CallBackOnStart.name)
        await message.answer("Как я могу к вам обращаться?", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(text="Вы уже проходили тест. Чтобы зарегистрировать новый заказ подождите некоторое время, пока бустеры отвят на ваш последний запрос.")

@router.message(CallBackOnStart.name)
async def choose_game(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CallBackOnStart.game)
    await message.answer(text=f"Очень приятно {message.text}! Теперь выберите игру", reply_markup=kb.choose_game_menu)

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
    name = data.get("name")
    
    await state.update_data(platform=platform)
    # await callback.message.answer(text=f"Давайте прорезумируем\n\n\")
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
async def handle_finish(message: types.Message, state: FSMContext):
    poll = message.text
    # data = await state.get_data()
    await state.update_data(poll=poll)
    await message.answer(
        text='Спасибо за формирование заказа, наш геймер-исполнитель свяжется с вами в ближайшее время для подтверждения заказа и проведения оплаты',
    )



@router.message(Command("help"))
async def help(message: types.Message):
    await message.reply('Меню help', reply_markup=kb.help)

@router.message(F.text)
async def wrong_message_handler(message: types.Message):
    await message.answer(
        'Вы ввели что-то непонятное, попробуйте снова?\n\n<b>Помощь</b>: /help'
        )
        




