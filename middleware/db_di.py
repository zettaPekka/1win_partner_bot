from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from typing import Callable, Dict, Awaitable, Any

from database.services.user_service import UserService
from database.repositories.user_repo import UserRepo
from database.services.gambling_service import GamblingService
from database.repositories.gambling_repo import GamblingRepo
from database.database import get_session


class DatabaseDI(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ):
        async with get_session() as session:
            user_service = UserService(session, UserRepo(session), GamblingRepo(session))
            data['user_service'] = user_service
            
            gambling_service = GamblingService(session, GamblingRepo(session))
            data['gambling_service'] = gambling_service
    
            return await handler(event, data)