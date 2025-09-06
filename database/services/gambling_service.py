from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.gambling_repo import GamblingRepo


class GamblingService:
    def __init__(self, session: AsyncSession, gambling_repo: GamblingRepo):
        self.session = session
        self.gambling_repo = gambling_repo
    
    async def create(self, user_id: str):
        self.gambling_repo.add(user_id)
        await self.session.commit()
    
    async def get(self, user_id: str):
        return await self.gambling_repo.get(user_id)
    
    async def dep(self, user_id: str, amount: int):
        await self.gambling_repo.dep(user_id, amount)
        await self.session.commit()
    
    async def get_by_tg_id(self, tg_id: int):
        return await self.gambling_repo.get_by_tg_id(tg_id)
    
    async def is_free(self, user_id: str):
        gambling_data = await self.get(user_id)
        if gambling_data and not gambling_data.tg_id:
            return True