from aiogram.fsm.state import StatesGroup, State


class Authorization(StatesGroup):
    user_agreement = State()
    choose_fio = State()
    choose_phonenumber = State()


class CreateOrder(StatesGroup):
    # Добавить проверку соглашения с пд
    choose_level = State()
    choose_form = State()
    choose_topping = State()
    choose_berries = State()
    choose_decor = State()
    choose_text = State()
    choose_comment = State()
    choose_addrese = State()
    choose_date = State()
    choose_time = State()
    choose_approve = State()
