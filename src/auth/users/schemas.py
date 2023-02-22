from pydantic import BaseModel


class UserBase(BaseModel):
    ...


class UserCreate(UserBase):
    username: str
    password: str


class UserInDB(UserBase):
    id: int
    username: str

    class Config:
        orm_mode = True
