import logging

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

logger = logging.getLogger('app.users.utils')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/login")


def create_hashed_password(user_password: str) -> str:
    hashed_password = pwd_context.hash(user_password)
    return hashed_password

