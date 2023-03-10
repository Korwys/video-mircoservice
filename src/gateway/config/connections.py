import pika
from pymongo import MongoClient
import gridfs

class Connections:
    client = MongoClient(
        "mongodb+srv://admin:admin@cluster0.nscqdu6.mongodb.net")

    grid_video = gridfs.GridFS(client.db, collection='video')
    grid_mp3 = gridfs.GridFS(client.db, collection='mp3')

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()


manager = Connections()
