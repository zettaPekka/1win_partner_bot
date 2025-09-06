from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import username, education_link


start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Получить доступ 🚀', callback_data='get_access')],
    [InlineKeyboardButton(text='Обучение 📚', url=education_link),
        InlineKeyboardButton(text='Связь 💬', url=f'https://t.me/{username}')],
])

check_dep = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Проверить депозит 🔍', callback_data='check_dep')]
])

reg_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Регистрация 🌐', url='https://tdf.er')],
])

get_signal = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Получить сигнал 🚀', callback_data='get_signal')],
    [InlineKeyboardButton(text='Обучение 📚', url=education_link)],
    [InlineKeyboardButton(text='Профиль 🏡', callback_data='profile')]
])