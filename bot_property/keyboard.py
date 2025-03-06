from aiogram import types
from datetime import datetime
import calendar
from .db_helper import get_all_levels, get_all_berries, get_all_decors, get_all_forms, get_all_toppings


def create_time_control_keyboard(hours=0, minutes=0):
    def wrap_time(h, m):
        return h % 24, m % 60

    hours, minutes = wrap_time(hours, minutes)

    keyboard_buttons = [
        [
            types.InlineKeyboardButton(
                text="-", callback_data='time_hour_decrease'),
            types.InlineKeyboardButton(
                text=f"{str(hours).zfill(2)} ч.", callback_data='ignore'),
            types.InlineKeyboardButton(
                text="+", callback_data='time_hour_increase')
        ],
        [
            types.InlineKeyboardButton(
                text="-", callback_data='time_minute_decrease'),
            types.InlineKeyboardButton(
                text=f"{str(minutes).zfill(2)} м.", callback_data='ignore'),
            types.InlineKeyboardButton(
                text="+", callback_data='time_minute_increase')
        ],
        [types.InlineKeyboardButton(
            text='Подтвердить', callback_data='time_choose')],
        [types.InlineKeyboardButton(text="Отмена", callback_data="exit")]
    ]

    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def create_calendar(year, month):
    keyboard_buttons = [[types.InlineKeyboardButton(
        text='<<', callback_data=f'month_prev_{year}_{month}'),
        types.InlineKeyboardButton(
            text="{} - {}".format(calendar.month_name[month], year), callback_data='ignore'),
        types.InlineKeyboardButton(
            text='>>', callback_data=f'month_next_{year}_{month}')],]

    month_days = calendar.monthcalendar(year, month)
    print("test", year, month)
    for week in month_days:
        row = []
        for day in week:
            if day == 0:
                row.append(types.InlineKeyboardButton(
                    text=' ', callback_data='ignore'))
            else:
                row.append(types.InlineKeyboardButton(text=str(day),
                           callback_data=f'day_{year}_{month}_{day}'))
        keyboard_buttons += [row]
    keyboard_buttons += [[types.InlineKeyboardButton(
        text="Отмена", callback_data="exit")]]

    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def exit_button():
    return types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(
        text="Отмена", callback_data="exit")]])


def exit_keyboard():
    keyboard_button = [[types.InlineKeyboardButton(
        text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_button)


def create_order_keyboard():
    keyboard_buttons = [[types.KeyboardButton(text="Создать заказ")], [
        types.KeyboardButton(text='Мои заказы')]]
    return types.ReplyKeyboardMarkup(keyboard=keyboard_buttons)


def user_agreement_keyboard():
    keyboard_buttons = [[types.InlineKeyboardButton(text='Я соглашаюсь', callback_data='agreement_approve')],
                        [types.InlineKeyboardButton(text='Не согласен', callback_data='agreement_refusal')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


async def choose_level_keyboard():
    keyboard_buttons = []
    cake_levels = await get_all_levels()
    for cake_level in cake_levels:
        keyboard_buttons.append([types.InlineKeyboardButton(
            text=f'{cake_level.name} - {cake_level.price} руб.',
            callback_data=f'level_{cake_level.id}'
        )])
    keyboard_buttons += [[types.InlineKeyboardButton(
        text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


async def choose_form_keyboard():
    keyboard_buttons = []
    cake_forms = await get_all_forms()
    for cake_form in cake_forms:
        keyboard_buttons.append([types.InlineKeyboardButton(
            text=f'{cake_form.name} - {cake_form.price} руб.',
            callback_data=f'form_{cake_form.id}'
        )])
    # keyboard_buttons = [[types.InlineKeyboardButton(text='Квадрат', callback_data='form_1')],
    #                     [types.InlineKeyboardButton(text='Круг', callback_data='form_2')]]
    keyboard_buttons += [[types.InlineKeyboardButton(
        text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


async def choose_topping_keyboard():
    keyboard_buttons = []
    cake_toppings = await get_all_toppings()
    for cake_topping in cake_toppings:
        keyboard_buttons.append([types.InlineKeyboardButton(
            text=f'{cake_topping.name} - {cake_topping.price} руб.',
            callback_data=f'topping_{cake_topping.id}'
        )])
    # keyboard_buttons = [[types.InlineKeyboardButton(text='Без топпнига', callback_data='topping_1')],
    #                     [types.InlineKeyboardButton(text='Белый соус', callback_data='topping_2')]]
    keyboard_buttons += [[types.InlineKeyboardButton(
        text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


async def choose_berries_keyboard():
    keyboard_buttons = []
    cake_berries = await get_all_berries()
    for cake_berry in cake_berries:
        keyboard_buttons.append([types.InlineKeyboardButton(
            text=f'{cake_berry.name} - {cake_berry.price} руб.',
            callback_data=f'berries_{cake_berry.id}'
        )])
    # keyboard_buttons = [[types.InlineKeyboardButton(text='Ежевика', callback_data='berries_1')],
    #                     [types.InlineKeyboardButton(text='Малина', callback_data='berries_2')]]
    keyboard_buttons += [[types.InlineKeyboardButton(text='Пропустить', callback_data='berries_pass')],
                         [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


async def choose_decore_keyboard():
    keyboard_buttons = []
    cake_decories = await get_all_decors()
    for cake_decor in cake_decories:
        keyboard_buttons.append([types.InlineKeyboardButton(
            text=f'{cake_decor.name} - {cake_decor.price} руб.',
            callback_data=f'decore_{cake_decor.id}'
        )])
    # keyboard_buttons = [[types.InlineKeyboardButton(text='Фисташки', callback_data='decore_1')],
    #                     [types.InlineKeyboardButton(text='Безе', callback_data='decore_2')]]
    keyboard_buttons += [[types.InlineKeyboardButton(text='Пропустить', callback_data='decore_pass')],
                         [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def text_pass_keyboard():
    keyboard_buttons = [[types.InlineKeyboardButton(text="Пропустить", callback_data='text_pass')],
                        [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def comment_pass_keyboard():
    keyboard_buttons = [[types.InlineKeyboardButton(text="Пропустить", callback_data='comment_pass')],
                        [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def approve_order_keyboard():
    keyboard_buttons = [[types.InlineKeyboardButton(text="Подтвердить заказ", callback_data='order_approve')],
                        [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def my_orders_keyboard(orders, number):
    orders_count = len(orders)
    info = orders[number]
    if len(orders) > 1:
        keyboard_buttons = [[types.InlineKeyboardButton(text='<-', callback_data='my_order_prev'), types.InlineKeyboardButton(text=f'{number}/{orders_count}', callback_data='my_order_info'),
                            types.InlineKeyboardButton(text='<-', callback_data='my_order_next')],
                            [types.InlineKeyboardButton(text=f'Адрес:{str(info.adress)} Дата: {info.date.strftime('%d-%m-%Y %H-%M')}', callback_data='my_order_info')]]
    else:
        keyboard_buttons = [[types.InlineKeyboardButton(
            text=f'Адрес:{str(info.adress)} Дата: {info.date.strftime('%d-%m-%Y %H-%M')}', callback_data='my_order_info')]]
    keyboard_buttons += [[types.InlineKeyboardButton(
        text='Отмена', callback_data='exit')]]

    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
