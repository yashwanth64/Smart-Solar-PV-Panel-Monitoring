from sensorClass.client_broker_data import *
from sensorClass.TempHumidityDust import *

# Function to call publisher to send data
def publisher_data(input_topic_name,payload_data, myclient):
    publish_data = json.dumps(payload_data,indent=4)
    myclient.publish(input_topic_name,publish_data,qos=QOS)
    print("Publishing to :" + input_topic_name )
    time.sleep(0.1)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
def on_message(client, userdata, msg):
    pass   

class simRoomTemp():
    """docstring for simRoomTemp"""

    #LineNum in int
    #passed as simTime in unit minutes, stored as seconds

    # ------- Publish timeline -----------
    # room temp + humidity sensor : every 15 sec
    # solder sensor : every 5 sec
    # convyor belt - will check every 1 Sec 
    # IR sensor - every 5 min - but will sense every 5 sec, will send "false" and "true" count only in the interval of 5 min
    # esd sensor  will check every 1 sec
    # pressure sensor - every 5 sec 

    def __init__(self, lineNum, simTime = 5,rTcount = 1):
        super(simRoomTemp, self).__init__()
        self.lineNum = lineNum
        self.simTime = simTime*60 + 5 
        self.rTcount = rTcount
        self.pause = False

        self.roomTemp = {}

        #create instances of room temperature sensor
        self.roomTempSensList =[]
        for i in range (0,self.rTcount):
            identity = createInstanceID(self.lineNum, 'S', ABV_DICT["roomTemp"], i)
            self.roomTempSensList.append(TemperatureSensor(instanceID = identity,  tempSensorType = TEMP_ROOM))
            print(identity)

        self.topicFinal = ""

    def startSim(self, clientName):

        startTime = datetime.datetime.now()
        timeDiff = 0
        sec15Count = 15
        keySet= True

        while self.simTime > 0 and not(self.pause) :

            if(int(timeDiff) == 1):

                startTime = currTime
                self.simTime -= 1
                sec15Count  -= 1

            #check 15 seconds have passed or not
            if(sec15Count == 0):
                sec15Count = 15

                #sense room temperature sensor values
                for x in range(self.rTcount):
                    key = self.roomTempSensList[x].getInstanceID()
                    self.roomTemp[key] =  self.roomTempSensList[x].sense()

                    if(keySet):
                        self.topicFinal += "_"+key
                        
                keySet = False

                publisher_data(topicDict["RT"] +self.topicFinal ,self.roomTemp ,clientName)

                # print("---15 sec over Room Temp---")


            currTime = datetime.datetime.now()
            timeDiff  = (currTime - startTime).total_seconds()
        self.stopSim()

    def stopSim(self):
        self.simTime = 0 
        print("----Simulation endded----") 

    def pauseSim(self):
        self.pause = True


def main() :
    simRoomTempClient   = mqtt.Client(clientDict["simRoomTempClient"], clean_session =False)

    simRoomTempClient.on_connect = on_connect 
    simRoomTempClient.on_message = on_message

    simRoomTempClient.connect(brokerHost, brokerPort,brokerKeepAlive)
    time.sleep(0.2)

    test = simRoomTemp(1,SIMULATION_TIME)

    simRoomTempClient.loop_start()
    test.startSim(simRoomTempClient)
    simRoomTempClient.loop_stop()

    simRoomTempClient.disconnect()

if __name__ == "__main__":
    main()
