import logging

import requests
from fastapi import Depends, Request, APIRouter
from starlette.responses import JSONResponse

from auth.users.schemas import UserInDB
from gateway.schemas import UserBase
from gateway.utils import check_current_user

router = APIRouter()


@router.post('/singup')
def signup(user: UserBase):
    res = requests.post('http://0.0.0.0:8080/api/users/new', json=user.dict())
    return JSONResponse(status_code=201, content=res.text)


@router.post('/login')
def login(user: UserBase):
    username, password = user.username, user.password
    if not username or not password:
        JSONResponse(status_code=401, content='Bad credentials')

    response = requests.post('http://0.0.0.0:8080/api/users/login', json=user.dict())

    if response.status_code == 200:
        return response.text
    else:
        return JSONResponse(status_code=401, content={"Message": "Bad credentials"})


@router.post('/upload', )
def video_upload(request: Request, user: UserInDB = Depends(check_current_user)):
    a = user
    print('ok')


@router.get('/download')
def video_download():
    pass
