from fastapi import APIRouter, Query, Depends

from database.services.gambling_service import GamblingService
from postback.db_dependencies import get_gambling_service


router = APIRouter()


@router.get('/reg/')
async def reg(
    user_id: str = Query(),
    gambling_service: GamblingService = Depends(get_gambling_service)
):
    await gambling_service.create(user_id)


@router.get('/dep/')
async def reg(
    user_id: str = Query(),
    amount: float = Query(),
    gambling_service: GamblingService = Depends(get_gambling_service)
):
    try:
        await gambling_service.dep(user_id, amount)
    except AttributeError:
        pass