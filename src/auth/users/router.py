from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.db import get_db
from src.auth.users.schemas import UserCreate

router = APIRouter(prefix='users', tags=['users'])


@router.post('/new')
async def create_new_user(new_user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await add_new_user_in_db(db, new_user)
