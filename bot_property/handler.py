from aiogram import types
from aiogram.fsm.context import FSMContext
import datetime
from .state import CreateOrder, Authorization
from .keyboard import (user_agreement_keyboard, exit_keyboard, create_order_keyboard,
                       choose_level_keyboard, create_calendar, approve_order_keyboard)


async def start_handler(message: types.Message, state: FSMContext):
    # Добавить проверку из бд
    # Добавить сперва проверку пользовательского соглашения
    await state.clear()
    await message.delete()
    tg_user_id = message.from_user.id
    send_with_registration = False  # Затычка убрать после проверки из бд
    if send_with_registration:
        await state.set_state(Authorization.user_agreement)
        await state.update_data({'id_user': message.from_user.id})
        # Добавить вывод в pdf
        await message.answer('Пользовательское сошлашение',
                             reply_markup=user_agreement_keyboard())
    else:
        # Добавить наполнение
        await message.answer('Вы можете создать заказ', reply_markup=create_order_keyboard())


async def user_name_handler(message: types.Message, state: FSMContext):
    await state.update_data({'fio': message.text})
    await message.delete()
    await state.set_state(Authorization.choose_phonenumber)
    await message.answer('Ввдеит номер телефона', reply_markup=exit_keyboard())


async def phone_number_handler(message: types.Message, state: FSMContext):
    # Тут добавить сохранение в бд
    data = await state.get_data()
    tg_user_id = data['id_user']
    fio = data['fio']
    await message.delete()
    await message.answer(f'Ваши данные {tg_user_id} {fio} {message.text}')
    await state.clear()
    # Добавить наполнение + Просмотр своих заказов
    await message.answer('Вы можете создать заказ', reply_markup=create_order_keyboard())


async def create_order_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.delete()
    await state.set_state(CreateOrder.choose_level)
    await message.answer('Выбрите уровни торта', reply_markup=choose_level_keyboard())


async def choose_text_handler(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data({'text': message.text})
    # data = await state.get_data()
    # await message.answer(text=" ".join(map(str, data.values())))
    await state.set_state(CreateOrder.choose_addrese)
    await message.answer('Введите адресс доставки', reply_markup=exit_keyboard())


async def input_address_handler(message: types.Message, state: FSMContext):
    # Добавить вывод предварительной стоимости с учетом подсчета
    await message.delete()
    await state.update_data({'address': message.text})
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    await state.update_data({"year_first": current_year, "month_first": current_month})
    await state.set_state(CreateOrder.choose_date)
    await message.answer('Выберите дату доставки', reply_markup=create_calendar(current_year, current_month))


async def input_comment_handler(message: types.Message, state: FSMContext):
    await message.delete()
    await state.update_data({'comment': message.text})
    await state.set_state(CreateOrder.choose_approve)
    await message.answer("Подтвердите заказ", reply_markup=approve_order_keyboard())
