from aiogram import types
from aiogram.fsm.context import FSMContext
from .state import Authorization, CreateOrder
from .keyboard import (exit_keyboard, choose_form_keyboard, choose_topping_keyboard,
                       choose_berries_keyboard, choose_decore_keyboard, text_pass_keyboard,
                       create_calendar, create_time_control_keyboard, comment_pass_keyboard,
                       approve_order_keyboard)

import datetime


async def exit_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()
    await callback.message.answer('Вы отменили свои действия')


async def user_agreement_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    if data == 'approve':
        await state.set_state(Authorization.choose_fio)
        await callback.message.answer('Введите ФИО', reply_markup=exit_keyboard())
    if data == 'refusal':
        await callback.message.answer('Вы не дали согласие')


async def choose_level_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    await state.update_data({'level': int(data)})
    await state.set_state(CreateOrder.choose_form)
    await callback.message.answer(text='Выберите форму торта', reply_markup=choose_form_keyboard())


async def choose_form_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    await state.update_data({'form': int(data)})
    await state.set_state(CreateOrder.choose_topping)
    await callback.message.answer(text='Выберите топинг', reply_markup=choose_topping_keyboard())


async def choose_topping_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    await state.update_data({'topping': int(data)})
    await state.set_state(CreateOrder.choose_berries)
    await callback.message.answer(text='Выберите ягоды', reply_markup=choose_berries_keyboard())


async def choose_berries_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    if data != 'pass':
        await state.update_data({'berries': int(data)})
    await state.set_state(CreateOrder.choose_decor)
    await callback.message.answer(text='Выберите декор', reply_markup=choose_decore_keyboard())


async def choose_decore_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    if data != 'pass':
        await state.update_data({'decore': int(data)})
    await state.set_state(CreateOrder.choose_text)
    await callback.message.answer(text='Выберите надпись', reply_markup=text_pass_keyboard())


async def pass_text_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    # data = await state.get_data()
    # await callback.message.answer(text=" ".join(map(str, data.values())))
    await state.set_state(CreateOrder.choose_addrese)
    await callback.message.answer('Введите адресс доставки', reply_markup=exit_keyboard())


async def swith_month_callback(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split("_")[1]
    state_data = await state.get_data()
    if 'year_last' not in state_data:
        current_year = state_data['year_first']
        current_month = state_data['month_first']
    else:
        current_year = state_data['year_last']
        current_month = state_data['month_last']

    if data == 'prev':
        if current_month - 1 <= 0:
            current_year -= 1
            current_month = 12
        else:
            current_month -= 1
    if data == 'next':
        if current_month + 1 > 12:
            current_year += 1
            current_month = 1
        else:
            current_month += 1
    if 'year_last' not in state_data:
        await state.update_data({'year_first': current_year, 'month_first': current_month})
        await callback.message.edit_text(text='Выберите к какого числа приготовить торт', reply_markup=create_calendar(current_year, current_month))
    else:
        await state.update_data({'year_last': current_year, 'month_last': current_month})
        await callback.message.edit_text(text='Выберите к какого числа приготовить торт', reply_markup=create_calendar(current_year, current_month))


async def choose_date_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = int(callback.data.split("_")[3])
    await state.update_data({'day': data})
    await state.set_state(CreateOrder.choose_time)
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    await state.update_data({'current_hours': hour, "current_minutes": minute})
    await callback.message.answer(text='Выберите время когда хотите забрать заказ', reply_markup=create_time_control_keyboard(hour, minute))


async def switch_time_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.data.split('_')[1] != 'choose':
        data = callback.data.removeprefix("time_")
        time_data = await state.get_data()
        current_hours = time_data['current_hours']
        current_minutes = time_data['current_minutes']
        if data == 'hour_decrease':
            if current_hours - 1 < 1:
                current_hours = 23
            else:
                current_hours -= 1
        elif data == 'hour_increase':
            if current_hours + 1 > 23:
                current_hours = 0
            else:
                current_hours += 1
        elif data == 'minute_decrease':
            if current_minutes - 1 < 1:
                current_minutes = 59
            else:
                current_minutes -= 1
        elif data == 'minute_increase':
            if current_minutes + 1 > 59:
                if current_hours + 1 > 23:
                    current_hours = 0
                    current_minutes = 0
                else:
                    current_hours += 1
                    current_minutes = 0
            else:
                current_minutes += 1
        await state.update_data({'current_hours': current_hours, "current_minutes": current_minutes})
        await callback.message.edit_text(text='Выберите время когда хотите забрать заказ', reply_markup=create_time_control_keyboard(current_hours, current_minutes))
    else:
        # Тут добавить условия с заказом про 24 часа
        await callback.message.delete()
        await state.set_state(CreateOrder.choose_comment)
        await callback.message.answer('Вы можете оставить коментарий к заказу', reply_markup=comment_pass_keyboard())


async def comment_pass_calback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(CreateOrder.choose_approve)
    await callback.message.answer("Подтвердите заказ", reply_markup=approve_order_keyboard())


async def approve_order_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    state_data = await state.get_data()
    order_str = "\n".join(map(str, state_data.values()))
    await state.clear()
    await callback.message.answer(f'Ваш заказ\n {order_str}')
