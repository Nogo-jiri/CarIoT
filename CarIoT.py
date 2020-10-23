import RPi.GPIO as GPIO
import picamera
import time
import json

camera=PiCamera()

with open('settings.json') as JsonFile:
    JsonData=json.load(JsonFile)
    MessageOfDoorAlarm=JsonData['MessageOfDoorAlarm']
    MessageOfDoorClosed=JsonData['MessageOfDoorClosed']
    MessageOfImpactAlarm=JsonData['MessageOfImpactAlarm']
    StandardTime=JsonData['StandardTime']

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
    if GPIO.input(32)==0:
        camera.capture('CarImage.jpg')
        TwitMessage(MessageOfImpactAlarm, True)
        time.sleep(5)
