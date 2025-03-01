from aiogram import types
from datetime import datetime
import calendar


def create_order_keyboard():
    keyboard_buttons = [[types.KeyboardButton(text="Создать заказ")]]
    return types.ReplyKeyboardMarkup(keyboard=keyboard_buttons)
