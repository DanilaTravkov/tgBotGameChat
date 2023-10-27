from aiogram import types, F, Router, Bot
from aiogram.types import ReplyKeyboardRemove, CallbackQuery, KeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from filters.chat_type import ChatTypeFilter
from aiogram.fsm.context import FSMContext

import kb

from states import CallBackOnStart

import json
from datetime import datetime

router = Router()

@router.message(Command("start"), ChatTypeFilter(chat_type=["private"]))
async def start_handler(message: types.Message, state: FSMContext):

    current_user_id = message.from_user.id

    with open('users_list.json', 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)
        for elem in data:
            # Проверяем проходил ли пользователь опрос раньше и принял ли его прошлый заказ кто либо из бустеров
            if elem.get('id') == current_user_id and elem.get('reviewed') == False:
                user = False
                break
            else:
                user = True
    if user:    
        # await state.update_data(user_id=current_user_id)
        await state.set_state(CallBackOnStart.name)
        await message.answer("Напишите свой @ в телеграмме, чтобы мы связались с вами\n(Пример: <code>@useruser</code>)", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(text="Вы уже проходили тест. Чтобы зарегистрировать новый заказ подождите некоторое время, пока бустеры отвят на ваш последний запрос.")

@router.message(CallBackOnStart.name, ChatTypeFilter(chat_type=["private"]))
async def choose_game(message: types.Message, state: FSMContext):

    name = message.text
    await state.update_data(name=name, user_id=message.from_user.id)
    await state.set_state(CallBackOnStart.game)
    await message.answer(text=f"Очень приятно {name}! Теперь выберите игру", reply_markup=kb.choose_game_menu)

@router.callback_query(lambda query: query.data.startswith('game'), CallBackOnStart.game)
async def choose_platform(callback_query: CallbackQuery, state: FSMContext):

    game = callback_query.data
    await state.update_data(game=game)
    await state.set_state(CallBackOnStart.poll)
    await callback_query.message.answer(text=f"Вы выбрали {game}, теперь выберите платформу", reply_markup=kb.choose_platform_menu)

@router.callback_query(lambda query: query.data.startswith('plat'), CallBackOnStart.poll)
async def handle_poll(callback: CallbackQuery, state: FSMContext):

    platform = callback.data
    await state.update_data(platform=platform)
    await state.set_state(CallBackOnStart.poll)
    data = await state.get_data()
    game = data.get("game") 

    if game == 'game_rainbow_six_siege':
        await callback.message.answer(
            text=f"Вы выбрали {platform}, остался последний штрих, ответьте на следующие вопросы через пробел\n\n\
1. Впишите ваш текущий ранг\n\
2. Впишите желаемый ранг\n\
3. Впишите количество получаемых очков за игру",
            )
    elif game == 'game_fall_guys':
        await callback.message.answer(
            text=f"Вы выбрали {platform}, остался последний штрих, ответьте на следующий вопрос\n\n\
1. Впишите количество желаемых побед"
            )
    elif game == 'game_apex_legends':
        await callback.message.answer(
            text=f"Вы выбрали {platform}, остался последний штрих, ответьте на следующие вопросы через пробел\n\n\
1. Впишите ваш текущий ранг\n\
2. Впишите желаемый ранг"   
            )

@router.message(CallBackOnStart.poll, ChatTypeFilter(chat_type=["private"]))
async def handle_finish(message: types.Message, bot: Bot, state: FSMContext):

    data = await state.get_data()
    name = data.get("name")
    game = data.get("game") 
    platform = data.get("platform")
    poll = message.text
    timestamp = datetime.today().strftime('%Y.%m.%d')

    try:
        with open('users_list.json', 'r', encoding="utf-8") as json_file:
            user_data = json.load(json_file)
    except FileNotFoundError:
        user_data = []

    new_data = {
        "id": message.from_user.id, 
        "username": name,
        "game": game,
        "platform": platform,
        "game_poll": str(poll),
        "timestamp": timestamp,
        "reviewed": False
    }

    await state.update_data(poll=poll)
    await state.set_state(CallBackOnStart.reviewed)

    accept_menu = [[KeyboardButton(text='Принять', callback_data=f"accepted:{message.from_user.id}")]]
    accept_menu = InlineKeyboardMarkup(inline_keyboard=accept_menu)   

    message_order_created = await bot.send_message(
        chat_id=-1002054102871, text=f"\
Поступил новый заказ!\n\n\
От: {name}\n\
Игра: {game}\n\
Платформа: {platform}\n\
Доп.информация: {str(poll)}\n\
Дата: {timestamp}", reply_markup=accept_menu)
    
    await message.answer(
        text='Спасибо за формирование заказа, в скором времени его рассмотрят наши геймеры-исполнители и вам придет уведомлении о подтверждении бустером',
    )
    new_data['message_order_created_id'] = message_order_created.message_id
    user_data.append(new_data)

    # TODO раскомментировать сохранение данных в файл json в продакшене + добавить обновление данных
    # в хендлере reviewed

    with open('users_list.json', 'w', encoding="utf-8") as json_file:
        json.dump(user_data, json_file, ensure_ascii=False, indent=4)

@router.callback_query(lambda query: query.data.startswith('accepted:'))
async def accept_order_callback(callback: types.CallbackQuery, bot: Bot):

    user_id = int(callback.data.split(":")[1])

    with open('users_list.json', 'r', encoding="utf-8") as json_file:
        data = json.load(json_file)
        for elem in data:
            if elem.get('id') == user_id and not elem.get('reviewed'):
                elem['reviewed'] = True

    with open('users_list.json', 'w', encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    booster_name = callback.from_user.username
    chat_id = callback.message.chat.id
    
    await bot.send_message(chat_id, f"@{booster_name} принял заказ! Заказ закрыт.", reply_to_message_id=callback.message.message_id)    
    await bot.edit_message_reply_markup(chat_id, callback.message.message_id, reply_markup=None)

@router.message(Command("help"))
async def help(message: types.Message):
    if message.chat.id > 0:
        await message.reply(
            '/start - пройти опрос сначала\n/delete - удалить текущий запрос\n/show - просмотреть статус моего запроса' 
        )

@router.message(F.text)
async def wrong_message_handler(message: types.Message):
    if message.chat.id > 0:
        await message.answer(
            'Вы ввели что-то непонятное, попробуйте снова?\n\n<b>Помощь</b>: /help'
        )




        




