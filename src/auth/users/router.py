from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from users.schemas import UserLogin, UserCreate
from config.db import get_db
from .services import add_new_user_in_db, check_user_in_db

router = APIRouter(prefix='/api/users', tags=['users'])


@router.post('/new')
async def create_new_user(new_user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await add_new_user_in_db(db, new_user)


@router.post('/login')
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    return check_user_in_db(db, user)
