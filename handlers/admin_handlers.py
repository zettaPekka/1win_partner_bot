from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from middleware.db_di import DatabaseDI
from database.services.user_service import UserService


router = Router()
router.message.middleware(DatabaseDI())


@router.message(Command('next'))
async def set_next_k(message: Message, user_service: UserService):
    k = float(message.text.split()[-1])
    
    await user_service.set_next_k(message.from_user.id, k)
    await message.answer(f'Успешно, следующий коэф. выбран: {k}')