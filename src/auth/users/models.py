from sqlalchemy import Column, String

from src.auth.db import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True),
    username = Column(String(100),nullable=False)
    password = Column(String(50))