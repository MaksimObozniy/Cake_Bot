import asyncio
import logging
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, html
from os import environ
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import F
from aiogram.filters import CommandStart
from bot_property.handler import (start_handler, user_name_handler, phone_number_handler,
                                  create_order_handler, choose_text_handler, input_address_handler,
                                  input_comment_handler)

from bot_property.callback import (user_agreement_callback, exit_callback, choose_level_callback,
                                   choose_form_callback, choose_topping_callback, choose_berries_callback,
                                   choose_decore_callback, pass_text_callback, swith_month_callback,
                                   choose_date_callback, switch_time_callback, comment_pass_calback,
                                   approve_order_callback)

from bot_property.state import Authorization, CreateOrder

load_dotenv()
TOKEN = environ['BOT_TOKEN']
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main():
    dp = Dispatcher()
    dp.callback_query.register(exit_callback, F.data == 'exit')
    dp.message.register(start_handler, CommandStart())
    dp.message.register(user_name_handler, F.text, Authorization.choose_fio)
    dp.message.register(phone_number_handler, F.text,
                        Authorization.choose_phonenumber)
    dp.message.register(create_order_handler, F.text == 'Создать заказ')
    dp.message.register(choose_text_handler, F.text, CreateOrder.choose_text)
    dp.message.register(input_address_handler, F.text,
                        CreateOrder.choose_addrese)
    dp.message.register(input_comment_handler, F.text,
                        CreateOrder.choose_comment)

    dp.callback_query.register(
        swith_month_callback, F.data.startswith('month_'))

    dp.callback_query.register(
        switch_time_callback, F.data.startswith(
            'time_'), CreateOrder.choose_time
    )

    dp.callback_query.register(
        user_agreement_callback, F.data.startswith('agreement_'), Authorization.user_agreement)
    dp.callback_query.register(
        choose_level_callback, F.data.startswith(
            'level_'), CreateOrder.choose_level
    )
    dp.callback_query.register(
        choose_form_callback, F.data.startswith(
            'form_'), CreateOrder.choose_form
    )
    dp.callback_query.register(
        choose_topping_callback,  F.data.startswith(
            'topping_'), CreateOrder.choose_topping
    )
    dp.callback_query.register(
        choose_berries_callback, F.data.startswith(
            'berries_'), CreateOrder.choose_berries
    )
    dp.callback_query.register(
        choose_decore_callback, F.data.startswith(
            'decore_'), CreateOrder.choose_decor
    )
    dp.callback_query.register(
        pass_text_callback, F.data == 'text_pass'
    )
    dp.callback_query.register(
        choose_date_callback, F.data.startswith(
            'day_'), CreateOrder.choose_date
    )
    dp.callback_query.register(
        comment_pass_calback, F.data == 'comment_pass'
    )
    dp.callback_query.register(
        approve_order_callback, F.data == 'order_approve', CreateOrder.choose_approve
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
