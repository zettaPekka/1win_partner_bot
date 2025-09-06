from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import User


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def add(self, tg_id: int):
        user = User(tg_id=tg_id)
        self.session.add(user)
    
    async def get(self, tg_id: int):
        return await self.session.get(User, tg_id)
    
    async def get_all_users(self):
        users = await self.session.execute(select(User))
        users = users.scalars().all()
        return users
    async def link_gambling_user_id(self, tg_id: int, gambling_user_id: str):
        user = await self.get(tg_id)
        user.gambling_id = gambling_user_id