import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import JSONResponse

from users.helpers import error_info
from .schemas import UserCreate, UserLogin
from users.models import User
from .utils import create_hashed_password, verify_user_password, create_token

logger = logging.getLogger('app.users.services')


async def add_new_user_in_db(db: AsyncSession, obj_in: UserCreate) -> JSONResponse:
    response = await db.execute(select(User.username).where(User.username == obj_in.username))
    if response.first():
        return JSONResponse(status_code=404, content={'Message': 'This username already in user'})

    obj_in = obj_in.dict()
    obj_in['password'] = create_hashed_password(obj_in['password'])
    db_obj = User(**obj_in)

    try:
        db.add(db_obj)
        await db.commit()
        return JSONResponse(status_code=201, content={'Message': 'New user is create'})
    except SQLAlchemyError as err:
        logger.error(err)
        return error_info()


async def check_user_in_db(db: AsyncSession, user: UserLogin):
    user_response = await fetch_user_from_db(db, user)
    if not user_response or not verify_user_password(user.password, user_response.password):
        return JSONResponse(status_code=401, content={'Message': 'Bad credentials'})

    return {
        "access_token": create_token(sub=user_response.username),
        "token_type": "bearer"
    }


async def fetch_user_from_db(db: AsyncSession, data):
    try:
        response = await db.execute(select(User).filter(User.username == data.username))
        return response.scalars().first()
    except SQLAlchemyError as err:
        logger.exception(err)
