from pydantic import BaseModel


class UserBase(BaseModel):
    ...


class UserCreate(UserBase):
    username: str
    password: str


class UserLogin(UserCreate):
    ...


class UserInDB(UserBase):
    id: int
    username: str
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None
