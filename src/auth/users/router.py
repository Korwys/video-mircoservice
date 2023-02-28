from config.db import get_db
from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from users.schemas import UserLogin, UserCreate, Token

from .schemas import UserInDB
from .services import add_new_user_in_db, check_user_in_db
from .utils import get_current_user

router = APIRouter(prefix='/api/users', tags=['users'])


@router.post('/new')
async def create_new_user(new_user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await add_new_user_in_db(db, new_user)


@router.post('/login', response_model=Token, status_code=status.HTTP_200_OK)
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    return await check_user_in_db(db, user)


@router.post('/validate',status_code=status.HTTP_200_OK)
async def validate(token: str = Body(), db: AsyncSession = Depends(get_db)):
    return await get_current_user(token, db)
