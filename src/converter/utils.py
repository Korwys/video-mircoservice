import json
import os
import tempfile

import moviepy
import pika
from bson.objectid import ObjectId


def add_message_in_audio_queue(channel, message, ):
    try:
        channel.queue_declare(queue='audio')
        channel.basic_publish(exchange='',
                              routing_key='audio',
                              body=json.dumps(message),
                              properties=pika.BasicProperties(
                                  delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                              ),
                              )
        return 'ok'
    except Exception as err:
        print(err)
        return 'some error'


def get_audio_from_video(message: dict, ch, gridfs_video, gridfs_audio):
    # create new named temp file
    tf = tempfile.NamedTemporaryFile()

    # fetch video from db
    video_out = gridfs_video.get(ObjectId(message['video_fid']))

    # save video in temp file
    tf.write(video_out.read())

    # save in audio_file
    audio_file = moviepy.editor.VideoClip(tf.name).audio

    # close  and delete temp file
    tf.close()

    tf_path = tempfile.gettempdir() + f'/{message["video_fid"]}.mp3'
    audio_file.write_audiofile(tf_path)

    with open(f'{tf_path}', 'rb') as file:
        data = file.read()

    fid = gridfs_audio.put(data)

    message['audio_fid'] = fid
    os.remove(tf_path)

    response = add_message_in_audio_queue(ch, message)

    if response != 'ok':
        return 'Sorry, some error. Please, try again later'

    return 'ok'
