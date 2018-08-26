import paho.mqtt.client as mqtt
import serial
import time
import datetime
import pymongo
from pymongo import MongoClient
from threading import Thread

ser=serial.Serial(port='/dev/ttyACM1', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,timeout=1)
print ser.name
mongodb_uri="mongodb://Ema:ef123456@ds231941.mlab.com:31941/mewpurr"
client = MongoClient(mongodb_uri, connectTimeoutMS=30000)
db=client.get_database("mewpurr")
times=db.timestamps
alarms=db.alarms
distance=db.sensor
def on_connect(clinet,userdata,flags,rc):
        client.subscribe("mewpurr/food")
        print "on connect"

def on_message(client,userdata,msg):
        print(msg.topic+" "+str(msg.payload))
        if msg.payload =="release the food":
                ser.write("0")

def arduinoFunction():
	while True:
		if ser.readline().strip()=="m":
               		vrijeme = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%s')
               		record = {
       	               		"date":vrijeme,
             	        	"confirmed":"true"
               	       		}
			times.insert_one(record)
			print "aaaa"
			num = times.count()
			print num
		
def alarmFunction():
	while True:
		for document in alarms.find():
			timeNow=datetime.datetime.today().strftime('%H:%M')
			print timeNow
			if alarms.find_one({"time":timeNow}) != None:
				ser.write("0")
			time.sleep(60)
def sensorFunction():
	while True:
		if ser.readline().strip()=="e":
			distance.delete_many({"food":"empty"})
			record = {
				"food":"empty"
				}
			distance.insert_one(record)
			time.sleep(10)

arduino_thread=Thread(target=arduinoFunction)
arduino_thread.start()
alarm_thread=Thread(target=alarmFunction)
alarm_thread.start()
sensor_thread=Thread(target=sensorFunction)
sensor_thread.start()
client=mqtt.Client()
client.on_connect=on_connect
client.on_message=on_message
client.connect("broker.hivemq.com",1883,60)
client.loop_forever()	

