import json

import pika
import requests
from fastapi import HTTPException, Request, UploadFile
from starlette.responses import JSONResponse

from gateway.config.connections import manager
from email.message import EmailMessage


def check_current_user(request: Request) -> str:
    if not request.headers['authorization']:
        raise HTTPException(status_code=401, detail='Bad credentials')

    response = requests.post(f"http://0.0.0.0:8080/api/users/validate", json=request.headers['authorization'])
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.content)
    return response.text


def add_message_in_video_queue(message: dict):
    try:

        manager.channel.queue_declare(queue='video')
        manager.channel.basic_publish(exchange='',
                                      routing_key='video',
                                      body=json.dumps(message),
                                      properties=pika.BasicProperties(
                                          delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                                      ),
                                      )
        return 'ok'
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content='Some error')


def save_file_in_mongo(file: UploadFile, user: str):
    try:
        fid = manager.grid_video.put(file.file)
    except Exception as err:
        print(err)
        return JSONResponse(status_code=500, content='Some error')

    message = {
        'video_fid': str(fid),
        'audio_fid': None,
        'username': user
    }
    queue_response = add_message_in_video_queue(message=message)

    if queue_response != 'ok':
        return queue_response

    return JSONResponse(status_code=200, content='File was saved. We send you the download link in few moments')



if __name__ == '__main__':
    save_file_in_mongo()
