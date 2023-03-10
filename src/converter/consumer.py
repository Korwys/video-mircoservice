import json

import gridfs
import pika
from pymongo import MongoClient

from utils import get_audio_from_video

client = MongoClient(
    "mongodb+srv://admin:admin@cluster0.nscqdu6.mongodb.net")

grid_video = gridfs.GridFS(client.db, collection='video')
grid_mp3 = gridfs.GridFS(client.db, collection='mp3')


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='video')

    def callback(chanel, method, properties, body):
        message = json.loads(body)
        get_audio_from_video(message, chanel, grid_video, grid_mp3)

    channel.basic_consume(on_message_callback=callback, queue='video')

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()


if __name__ == '__main__':
    main()
