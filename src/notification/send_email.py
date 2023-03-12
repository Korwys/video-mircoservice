import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from bson.objectid import ObjectId



def send_notification_email(channel, data, fsaudio):
    message = json.dumps(data)
    receiver_email = message['username']
    audio_file = fsaudio.get(ObjectId(message['audio_fid']))

    sender = os.environ.get('SENDER_EMAIL')
    password = os.environ.get('SENDER_PASSWORD')

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(user=sender, password=password)

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver_email
    msg['Subject'] = 'You mp3 file is ready!'

    file = MIMEAudio(audio_file.read())

    file.add_header('content-disposition','attachment')
    msg.attach(file)

    server.sendmail(sender,receiver_email,msg.as_string())

