import logging
from datetime import timedelta, datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from jose import JWTError, jwt

from config.base import settings
from config.db import get_db
from users.models import User
from users.schemas import TokenData

logger = logging.getLogger('app.users.utils')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")


def create_hashed_password(user_password: str) -> str:
    hashed_password = pwd_context.hash(user_password)
    return hashed_password


def verify_user_password(user_credentials, hashed_pass):
    if not pwd_context.verify(user_credentials, hashed_pass):
        return False
    return user_credentials


async def get_user_hashed_password_from_db(username: int, db: AsyncSession = Depends(get_db)) -> str:
    try:
        response = db.execute(select(User.password).filter(User.username == username))
        return response.first()
    except SQLAlchemyError as err:
        logger.exception(err)


def create_token(sub: str):
    token_type = "access_token"
    lifetime = timedelta(minutes=int(settings.ttl))
    payload = {'token': token_type, 'exp': datetime.now() + lifetime, 'sub': sub}

    try:
        return jwt.encode(payload, settings.secret, settings.algorithm)
    except JWTError as err:
        logger.exception(err)


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret, algorithms=[settings.algorithm])
        username = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    response = await db.execute(select(User).filter(User.username == token_data.username))
    if response.first() is None:
        raise credentials_exception
    return response.first()
