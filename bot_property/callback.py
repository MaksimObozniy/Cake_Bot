from aiogram import types
from aiogram.fsm.context import FSMContext
from .state import Authorization, CreateOrder
from .keyboard import (exit_keyboard, choose_form_keyboard, choose_topping_keyboard,
                       choose_berries_keyboard, choose_decore_keyboard, text_pass_keyboard,
                       create_calendar, create_time_control_keyboard, comment_pass_keyboard,
                       approve_order_keyboard, my_orders_keyboard)
from .db_helper import create_order, get_my_orders, get_admins,get_dict_order
import asyncio
import datetime


def format_order(order):
   
    tg_id = order.get("tg_id", "Не указано")
    year = order.get("year", "")
    month = order.get("month", "")
    day = order.get("day", "")
    hours = order.get("hours", "")
    minutes = order.get("minutes", "")

    if year and month and day and hours is not None and minutes is not None:
        delivery_date = f"{day:02d}-{month:02d}-{str(year)[-2:]} {hours:02d}:{minutes:02d}"
    else:
        delivery_date = "Не указана"

    text = order.get("text", "Не указано")
    comments = order.get("comments", "Не указано")
    level = order.get("level", "Не указано")
    form = order.get("form", "Не указано")
    berries = order.get("berries", "Не указано")
    decor = order.get("decor", "Не указано")
    topping = order.get("topping", "Не указано")

    
    result = (
        f"Заказ от пользователя: {tg_id}\n"
        f"Дата доставки: {delivery_date}\n"
        f"Надпись на торте: {text}\n"
        f"Комментарий: {comments}\n"
        f"Уровни торта: {level}\n"
        f"Форма: {form}\n"
        f"Ягоды: {berries}\n"
        f"Декор: {decor}\n"
        f"Топпинг: {topping}"
    )

    return result


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
    await callback.message.answer(text='Выберите форму торта', reply_markup=await choose_form_keyboard())


async def choose_form_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    await state.update_data({'form': int(data)})
    await state.set_state(CreateOrder.choose_topping)
    await callback.message.answer(text='Выберите топинг', reply_markup=await choose_topping_keyboard())


async def choose_topping_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    await state.update_data({'topping': int(data)})
    await state.set_state(CreateOrder.choose_berries)
    await callback.message.answer(text='Выберите ягоды', reply_markup=await choose_berries_keyboard())


async def choose_berries_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = callback.data.split("_")[1]
    if data != 'pass':
        await state.update_data({'berries': int(data)})
    await state.set_state(CreateOrder.choose_decor)
    await callback.message.answer(text='Выберите декор', reply_markup=await choose_decore_keyboard())


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
    current_year = state_data['year']
    current_month = state_data['month']
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
    await state.update_data({'year': current_year, 'month': current_month})
    await callback.message.edit_text(text='Выберите к какого числа приготовить торт', reply_markup=create_calendar(current_year, current_month))


async def choose_date_callback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = int(callback.data.split("_")[3])
    await state.update_data({'day': data})
    await state.set_state(CreateOrder.choose_time)
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    await state.update_data({'hours': hour, "minutes": minute})
    await callback.message.answer(text='Выберите время когда хотите забрать заказ', reply_markup=create_time_control_keyboard(hour, minute))


async def switch_time_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.data.split('_')[1] != 'choose':
        data = callback.data.removeprefix("time_")
        time_data = await state.get_data()
        current_hours = time_data['hours']
        current_minutes = time_data['minutes']
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
        await state.update_data({'hours': current_hours, "minutes": current_minutes})
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
    await create_order(state_data)
    await state.clear()
    admins = await get_admins()
    print(admins)
    await callback.message.answer(format_order(state_data))
    for admin in admins:
        await callback.bot.send_message(admin.tg_id, format_order(state_data))
        asyncio.sleep(3)


async def swith_orders_callback(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('_')[2]
    order_data = await state.get_data()
    number = order_data['order_number']
    tg_id = order_data['tg_id']
    orders = await get_my_orders(tg_id)
    if data == 'next':
        if number + 1 > len(orders) - 1:
            number = 1
        else:
            number += 1
        await state.update_data({'order_number':number})
        await callback.message.edit_text(text='Ваши заказы', reply_markup=my_orders_keyboard(orders, number))
    if data == 'prev':
        if number - 1 < 0:
            number = len(orders) - 1
        else:
            number -= 1
        await state.update_data({'order_number':number})
        await callback.message.edit_text(text='Ваши заказы', reply_markup=my_orders_keyboard(orders, number))
    if data == 'info':
        print(data)
        order = await get_dict_order(orders[number].id)
        info = format_order(order)
        await callback.message.answer(info)
