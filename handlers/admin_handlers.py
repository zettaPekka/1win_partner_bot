from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

from middleware.db_di import DatabaseDI
from database.services.user_service import UserService

import os


load_dotenv()

router = Router()
router.message.middleware(DatabaseDI())


@router.message(Command('next'))
async def set_next_k(message: Message, user_service: UserService):
    if message.from_user.id == int(os.getenv('ADMIN_ID')):
        k = float(message.text.split()[-1])
        user_id = int(message.text.split()[1])
        
        await user_service.set_next_k(user_id, k)
        await message.answer(f'Успешно, следующий коэф. выбран: {k}')