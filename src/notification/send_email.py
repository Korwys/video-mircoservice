import json
import os
import smtplib
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart

from bson.objectid import ObjectId


def send_notification_email(data, fsaudio):
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

    with open(audio_file, 'rb') as f:
        src = MIMEAudio(f.read(), _subtype='mp3')

    src.add_header('content-disposition', 'attachment', filename=f'{message["audio_fid"]}.mp3')
    msg.attach(src)

    server.sendmail(sender, receiver_email, msg.as_string())
