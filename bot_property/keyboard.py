from aiogram import types
from datetime import datetime
import calendar


def create_calendar(year, month, type_callback):
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
                           callback_data=f'{type_callback}_day_{year}_{month}_{day}'))
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
    keyboard_buttons = [[types.KeyboardButton(text="Создать заказ")]]
    return types.ReplyKeyboardMarkup(keyboard=keyboard_buttons)


def user_agreement_keyboard():
    keyboard_buttons = [[types.InlineKeyboardButton(text='Я соглашаюсь', callback_data='agreement_approve')],
                        [types.InlineKeyboardButton(text='Не согласен', callback_data='agreement_refusal')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def choose_level_keyboard():
    # Добавить наполнение из бд Заменить на кб билдер
    keyboard_buttons = [[types.InlineKeyboardButton(text='1 уровень', callback_data='level_1')],
                        [types.InlineKeyboardButton(text='2 уровня', callback_data='level_2')]]
    keyboard_buttons += [[types.InlineKeyboardButton(
        text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def choose_form_keyboard():
    # Добавить наполнение из бд Заменить на кб билдер
    keyboard_buttons = [[types.InlineKeyboardButton(text='Квадрат', callback_data='form_1')],
                        [types.InlineKeyboardButton(text='Круг', callback_data='form_2')]]
    keyboard_buttons += [[types.InlineKeyboardButton(
        text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def choose_topping_keyboard():
    # Добавить наполнение из бд Заменить на кб билдер
    keyboard_buttons = [[types.InlineKeyboardButton(text='Без топпнига', callback_data='topping_1')],
                        [types.InlineKeyboardButton(text='Белый соус', callback_data='topping_2')]]
    keyboard_buttons += [[types.InlineKeyboardButton(
        text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def choose_berries_keyboard():
    # Добавить наполнение из бд Заменить на кб билдер
    keyboard_buttons = [[types.InlineKeyboardButton(text='Ежевика', callback_data='berries_1')],
                        [types.InlineKeyboardButton(text='Малина', callback_data='berries_2')]]
    keyboard_buttons += [[types.InlineKeyboardButton(text='Пропустить', callback_data='berries_pass')],
                         [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def choose_decore_keyboard():
    # Добавить наполнение из бд Заменить на кб билдер
    keyboard_buttons = [[types.InlineKeyboardButton(text='Фисташки', callback_data='decore_1')],
                        [types.InlineKeyboardButton(text='Безе', callback_data='decore_2')]]
    keyboard_buttons += [[types.InlineKeyboardButton(text='Пропустить', callback_data='decore_pass')],
                         [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def text_pass_keyboard():
    keyboard_buttons = [[types.InlineKeyboardButton(text="Пропустить", callback_data='text_pass')],
                        [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)


def approve_order_keyboard():
    keyboard_buttons = [[types.InlineKeyboardButton(text="Подтвердить заказ", callback_data='order_approve')],
                        [types.InlineKeyboardButton(text='Отмена', callback_data='exit')]]
    return types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
