from database.database import get_session
from database.services.gambling_service import GamblingService
from database.repositories.gambling_repo import GamblingRepo


async def get_gambling_service():
    async with get_session() as session:
        gambling_repo = GamblingRepo(session)
        gambling_service = GamblingService(session, gambling_repo)
        return gambling_service