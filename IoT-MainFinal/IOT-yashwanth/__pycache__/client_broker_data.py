import paho.mqtt.client as mqtt
import time
import datetime  
import json 
from sensorClass.act_TempAndHumidity import *
from sensorClass.TempHumidityDust import *
from sensorClass.prodLine import *


# awshost = "a1etmfjjj6j48x-ats.iot.us-west-2.amazonaws.com"  
# awsport = 8883
# caPath = "/home/yashwanth/Desktop/IOT/Certificates/root-ca.pem.txt"
# certPath = "/home/yashwanth/Desktop/IOT/Certificates/certificate.pem.crt"
# keyPath = "/home/yashwanth/Desktop/IOT/Certificates/private.pem.key"

brokerHost =  "broker.emqx.io" #"localhost"
brokerPort = 1883
brokerKeepAlive = 60





clientDict = {  "simLineClient" : "ProdLine",
				"simTempActClient" : "TemperatureActuator",
				"simHumActClient" : "HumidityActuator",
				"simProdServerClient" : "ProductionServer",
				"simRoomTempClient"  : "RoomTemperatureSensor",
				"simHumiditySensorClient" : "HumiditySensor",
				}

topicDict ={    "ST" : "prodLine/solderingStation",
 			    "HS" : "prodLine/humidity" ,
 				"RT" : "prodLine/roomTemp",
 				"OS" : "equipment/oscilloscope",
 				"TB" : "equipment/testBentch",
 				"CB" : "prodLine/equipment/convyor",
 				"RA" : "actuator/roomtempActuator",
 				"HA" : "actuator/humidityActuator",
 				"IR" : "prodLine/irSensor",
 				"ES" : "prodLine/ESD",
 				"PS" : "prodLine/pressure"}

##########################
# Instance ID format -of len 7
#  instance ID =  S/A/E | Abbrevation |Line Number | instance number
#   S/A -> 'S' (sensor) or 'A' (actuator ) or 'E' (equipment)  - 1 char
#   Line number  -> 01 - 99 -> 2char
#   instance number -> 00 - 99 -> 2 char
#    Abbrevation -> 2char
#        list of abbrevation
#                HS : HUMIDITY SENSOR
#                RT : ROOM TEMPERATUR SENSOR
#                ST : SOLDERING STATION SENSOR
#                OS : OSCILLOSCOPE 
#                TB : TESTBENTCH
#                CB : CONVYOR BELT
#				 RA : ROOM ACTUATOR
#				 HA : HUMIDITY ACTUATOR
# 				 IR : IR SENSOR
#########################

ABV_DICT  = { "humidity":		    'HS',
			   "roomTemp":			'RT', 
			   "solderingStation":  'ST', 
			   "oscilloscope" :     'OS',
			   "testBentch":        'TB',
			   "convyor" :          'CB',
			   "roomtempActuator":  'RA' ,
			   "humidityActuator":  'HA',
			   "irSensor" :         "IR",
			   "ESD" :              "ES",
			   "pressure" :         "PS"}

def createInstanceID(lineNum, s_a, abv, instanceNumber):
	createdID = s_a
	createdID = createdID + abv

	if lineNum < 10 :
	    createdID += '0'

	createdID += str(lineNum)

	if instanceNumber < 10 :
	    createdID += '0'

	createdID += str(instanceNumber)

	return createdID