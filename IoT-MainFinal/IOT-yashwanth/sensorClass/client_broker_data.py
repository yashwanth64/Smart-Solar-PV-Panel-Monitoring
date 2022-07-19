import paho.mqtt.client as mqtt
import time
import datetime
import json


brokerHost = "broker.emqx.io"  # "broker.hivemq.io" #"localhost"
brokerPort = 1883
brokerKeepAlive = 60

SIMULATION_TIME = 5

QOS = 1  # 0


clientDict = {
    "simLineClient": "ProdLine",
    "simTempActClient": "TemperatureActuator",
    "simHumActClient": "HumidityActuator1",
    "simDustActClient": "DustActuator",
    "simProdServerClient": "ProductionServer1",
    "simTemperatureSensorClient": "TemperatureSensor",
    "simHumiditySensorClient": "HumiditySensor",
    "simEquTbClient": "tbEquipment",
    "simDustSensorClient": "DustSensor",
}

topicDict = {
    "ST": "room/room1/prodLine1/sensor/solderingStation/",
    "HS": "room/room1/sensor/humidity1/",
    "RT": "room/room1/sensor/Temp/",
    "DS": "room/room1/sensor/dust/",
    "OS": "room/room1/equipment/oscilloscope/",
    "TB": "room/room1/equipment/testBentch/",
    "CB": "room/room1/prodLine1/equipment/convyor/",
    "RA": "room/room1/actuator/tempActuator1/",
    "HA": "room/room1/actuator/humidityActuator1/",
    "DA": "room/room1/actuator/dustActuator/",
    "IR": "room/room1/prodLine1/sensor/irSensor/",
    "ES": "room/room1/prodLine1/sensor/ESD/",
    "PS": "room/room1/prodLine1/sensor/pressure/",
    "PEO": "server/equipment/osc/",
    "PET": "server/equipment/tb/",
    "PHA": "server/actuator/humidityActuator1/",
    "PDA": "server/actuator/dustActuator/",
    "PRA": "server/actuator/tempActuator1/",
    "PRL": "server/room1/prodLine1/sensor/pressure/",
    "RPi": "room/rasberryPi/actuators/"
}


ABV_DICT = {
    "humidity": "HS",
    "dust": "DS",
    "temperature": "RT",
    "solderingStation": "ST",
    "oscilloscope": "OS",
    "testBentch": "TB",
    "convyor": "CB",
    "temperatureActuator": "RA",
    "humidityActuator": "HA",
    "dustActuator": "DA",
    "irSensor": "IR",
    "ESD": "ES",
    "pressure": "PS",
    "dust": "DS",
}

def createInstanceID(lineNum, s_a, abv, instanceNumber):
    createdID = s_a
    createdID = createdID + abv

    if lineNum < 10:
        createdID += "0"

    createdID += str(lineNum)

    if instanceNumber < 10:
        createdID += "0"

    createdID += str(instanceNumber)

    return createdID
