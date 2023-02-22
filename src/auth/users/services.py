import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import JSONResponse

from src.auth.users.models import User
from src.auth.users.schemas import UserCreate
from src.auth.users.utils import error_info

logger = logging.getLogger('app.users.services')


async def add_new_user_in_db(db: AsyncSession, obj_in: UserCreate):
    stmt = db.execute(select(User).where(User.id == obj_in.username))
    if not stmt:
        return JSONResponse(status_code=404, content={'Message': 'This username already in user'})
    obj_in= obj_in.dict()
    db_obj = User(*obj_in)

    try:
        db.add(db_obj)
        await db.commit()
        return JSONResponse(status_code=201, content={'New user is create'})
    except SQLAlchemyError as err:
        logger.error(err)
        return error_info()

