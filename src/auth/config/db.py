from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.base import settings

SQLALCHEMY_URL = f"postgresql+asyncpg://{settings.db_username}:{settings.db_password}@" \
                 f"{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine = create_async_engine(SQLALCHEMY_URL, echo=True)

session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with session() as db:
        yield db


async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
