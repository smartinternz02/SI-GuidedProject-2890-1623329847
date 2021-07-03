import wiotp.sdk.device
import time
import random
import cv2
import numpy as np
from pyzbar.pyzbar import decode

myConfig = { 
    "identity": {
        "orgId": "jokjkc",#place you're crednetials 
        "typeId": "iotdevice",
        "deviceId":"10001"
    },
    "auth": {
        "token": "12345678"
    }
}

def myCommandCallback(cmd):
    print("Message received from IBM IoT Platform: %s" % cmd.data['command'])
    m=cmd.data['command']

client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()
cap = cv2.VideoCapture(0)
cap.set(3,640) #width of the frames in the video feed
cap.set(4,480) #height of the frames in the video feed
global hdairy,hegoods,hgoods,adairy,aegoods,agoods
hdairy=0
hegoods=0
hgoods=0
adairy=0
aegoods=0
agoods=0
while True:
    ret,img = cap.read()
    for barcode in decode(img):
        mydata = barcode.data.decode('utf-8')
        print(mydata)
        if(mydata.count("Hyderabad")>=1):
            hgoods=hgoods+1
            print("the no.of goods for Hyderabad are ",hgoods)
            if(mydata.count("dairy-products")>=1):
                hdairy=hdairy+1
                print("the no.of Dairy products for Hyderabad are ",hdairy)
            elif(mydata.count("electronic goods")>=1):
                hegoods=hegoods+1
                print("the no.of Electronic goods for Hyderabad are ",hegoods)
        if(mydata.count("Adilabad")>=1):
            agoods=agoods+1
            print("the no.of goods for Adilabad are ",agoods)
            if(mydata.count("dairy-products")>=1):
                adairy=adairy+1
                print("the no.of Dairy products for Adilabad are ",adairy)
            elif(mydata.count("electronic-goods")>=1):
                aegoods=aegoods+1
                print("the no.of Electronic goods for Adilabad are ",aegoods)
        pts = np.array([barcode.polygon],np.int32)
        pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(0,0,255),5)
        pts2 = barcode.rect
        cv2.putText(img,mydata,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,1.2,(0,255,255),3)
        cv2.imshow('rfid-scanner',img)
        cv2.waitKey(1)
        myData={'hgoods':hgoods,'hdairy':hdairy,'hegoods':hegoods,'agoods':agoods,'adairy':adairy,'aegoods':aegoods }
        client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
        print("Published data Successfully: %s", mydata)
        client.commandCallback = myCommandCallback
    time.sleep(5)
cv2.destroyAllWindows()

    
client.disconnect()
