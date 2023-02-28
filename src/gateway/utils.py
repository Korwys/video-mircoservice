import requests
from fastapi import HTTPException, Request


def check_current_user(request: Request) -> str:
    if not request.headers['authorization']:
        raise HTTPException(status_code=401, detail='Bad credentials')

    response = requests.post(f"http://0.0.0.0:8080/api/users/validate", json=request.headers['authorization'])
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.content)
    return response.text
