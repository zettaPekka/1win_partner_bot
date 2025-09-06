from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import GamblingData


class GamblingRepo:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    def add(self, user_id: str):
        gambling_data = GamblingData(user_id=user_id)
        self.session.add(gambling_data)
    
    async def get(self, user_id: str):
        return await self.session.get(GamblingData, user_id)
    
    async def dep(self, user_id: str, amount: int):
        user = await self.get(user_id)
        user.balance += amount
    
    async def link_tg_id(self, tg_id: int, gambling_user_id: str):
        gambling_data = await self.get(gambling_user_id)
        gambling_data.tg_id = tg_id
    
    async def get_by_tg_id(self, tg_id: int):
        gambling_data = await self.session.execute(select(GamblingData).where(GamblingData.tg_id == tg_id))
        gambling_data = gambling_data.scalar()
        return gambling_data