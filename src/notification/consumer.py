import sys

import gridfs
import pika
from pymongo import MongoClient

from send_email import send_notification_email

client = MongoClient(
    "mongodb+srv://admin:admin@cluster0.nscqdu6.mongodb.net")

grid_mp3 = gridfs.GridFS(client.db, collection='mp3')


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()
    channel.queue_declare('mp3')

    def callback(ch, method, properties, body):
        send_notification_email(ch, body, grid_mp3)

    channel.basic_consume(on_message_callback=callback, queue='mp3')

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        sys.exit()
