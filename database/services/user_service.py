from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.repositories.user_repo import UserRepo
from database.repositories.gambling_repo import GamblingRepo


class UserService:
    def __init__(self, session: AsyncSession, user_repo: UserRepo, gambling_repo: GamblingRepo):
        self.session = session
        self.user_repo = user_repo
        self.gambling_repo = gambling_repo
    
    async def create_if_not_exists(self, tg_id: int):
        user = await self.get(tg_id)
        if not user:
            self.user_repo.add(tg_id)
            await self.session.commit()
    
    async def get(self, tg_id: int) -> User | None:
        return await self.user_repo.get(tg_id)

    async def get_all_users(self):
        return await self.user_repo.get_all_users()

    async def set_next_k(self, tg_id: int, k: int):
        user = await self.get(tg_id)
        user.next_k = k
        await self.session.commit()
    
    async def link_gambling_user_id(self, tg_id: int, gambling_user_id: str):
        await self.user_repo.link_gambling_user_id(tg_id, gambling_user_id)
        await self.gambling_repo.link_tg_id(tg_id, gambling_user_id)
        await self.session.commit()
    
    async def reset_next_k(self, tg_id: int):
        user = await self.get(tg_id=tg_id)
        user.next_k = None
        await self.session.commit()