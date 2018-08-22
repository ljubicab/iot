import paho.mqtt.client as mqtt
import serial
import time
import datetime
import pymongo
from pymongo import MongoClient

ser=serial.Serial(port='/dev/ttyACM0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,timeout=1)

mongodb_uri="mongodb://Ema:ef123456@ds231941.mlab.com:31941/mewpurr"
client = MongoClient(mongodb_uri, connectTimeoutMS=30000)
db=client.get_database("mewpurr")
times=db.timestamps

def on_connect(clinet,userdata,flags,rc):
	client.subscribe("mewpurr/food")
	print "on connect"

def on_message(client,userdata,msg):
	print(msg.topic+" "+str(msg.payload))
	if msg.payload =="release the food":
		print "tu sam"
		ser.write("0")
		vrijeme = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%s')
                a= {
                       "date":vrijeme,
                       "confirmed":"true"
                       }              
		pushRECORD(a)


def pushRECORD(record):
	times.insert_one(record)

arduino = serial.Serial('/dev/ttyACM0',9600)
  #      print arduino.name
   #     print "Connected"
#except:
 #       print "Failed to connect"


try:
	while True:
		if arduino.readline().strip() == 'move':
			print "if" 
			vrijeme = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%s')
			a= {
				"date":vrijeme,
				"confirmed":"true"
				}
			pushRECORD(a)	
			print "else"
			client=mqtt.Client()
			client.on_connect=on_connect
			client.on_message=on_message
			client.connect("broker.hivemq.com",1883,60)
			client.loop_forever()

	 
except:
	print "fail"
#client=mqtt.Client()
#client.on_connect=on_connect
#client.on_message=on_message
#client.connect("broker.hivemq.com",1883,60)
#client.loop_forever()
