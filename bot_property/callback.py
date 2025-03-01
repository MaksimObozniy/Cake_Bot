from aiogram import types
from aiogram.fsm.context import FSMContext
from .state import Authorization, CreateOrder
from .keyboard import (exit_keyboard, choose_form_keyboard, choose_topping_keyboard,
                       choose_berries_keyboard, choose_decore_keyboard, text_pass_keyboard)


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
    data = await state.get_data()
    await callback.message.answer(text=" ".join(map(str, data.values())))
