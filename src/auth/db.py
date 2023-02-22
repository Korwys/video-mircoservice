from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_URL = f'postgresql+asyncpg://postgres:postgres@localhost/postgres'

engine = create_async_engine(SQLALCHEMY_URL, echo=True)

session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with session() as db:
        yield db
        yield db.commit()
