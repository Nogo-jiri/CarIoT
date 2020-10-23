import RPi.GPIO as GPIO
from picamera import PiCamera
from twython import Twython
import time
import json

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(32,GPIO.IN,pull_up_down=GPIO.PUD_UP)

camera=PiCamera()

with open('settings.json') as JsonFile:
    JsonData=json.load(JsonFile)
    consumer_key=JsonData['consumer_key']
    consumer_secret=JsonData['consumer_secret']
    access_token=JsonData['access_token']
    access_token_secret=JsonData['access_token_secret']
    MessageOfDoorAlarm=JsonData['MessageOfDoorAlarm']
    MessageOfDoorClosed=JsonData['MessageOfDoorClosed']
    MessageOfImpactAlarm=JsonData['MessageOfImpactAlarm']
    StandardTime=JsonData['StandardTime']

twitter=Twython(consumer_key,consumer_secret,access_token,access_token_secret)

def TwitMessage(message,image):
    if image==False:
        twitter.update_status(status=message)
    else:
        response=twitter.upload_media(media=open('CarImage.jpg','rb'))
        media_id=[response['media_id']]
        twitter.update_status(status=message, media_ids=media_id)

while True:
    if GPIO.input(8)==1:
        print("Door is opened!")
        t=0
        while True:
            if GPIO.input(8)==0:
                print("Door is closed!")
                TwitMessage(MessageOfDoorClosed, False)
                break
            else:
                t+=1;
                time.sleep(1)
            if t==StandardTime:
                print("Door has been opened so long!")
                TwitMessage(MessageOfDoorAlarm, False)
    if GPIO.input(32)==1:
        camera.capture('CarImage.jpg')
        TwitMessage(MessageOfImpactAlarm, True)
        time.sleep(5)
