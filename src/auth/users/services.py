import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import JSONResponse

from config.utils import error_info
from .schemas import UserCreate, UserLogin
from users.models import User
from .utils import create_hashed_password

logger = logging.getLogger('app.users.services')


async def add_new_user_in_db(db: AsyncSession, obj_in: UserCreate) -> JSONResponse:
    stmt = select(User.username).where(User.username == obj_in.username)
    response = await db.execute(stmt)
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
    result = await db.execute(select(User).where(User.username == user.username))
    if not result:
        return JSONResponse(status_code=403, content={'Message': 'Invalid credentials'})
