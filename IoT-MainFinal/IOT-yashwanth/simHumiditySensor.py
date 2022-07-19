from sensorClass.client_broker_data import *
from sensorClass.TempHumidityDust import *


# Function to call publisher to send data
def publisher_data(input_topic_name, payload_data, myclient):
    publish_data = json.dumps(payload_data, indent=4)
    myclient.publish(input_topic_name, publish_data, QOS)
    print("Publishing to :" + input_topic_name)
    time.sleep(0.1)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


def on_message(client, userdata, msg):
    pass


class simHumiditySensor():
    """docstring for simHumiditySensor"""

    def __init__(self, lineNum, simTime=5, hCount=1):
        self.lineNum = lineNum
        self.simTime = simTime*60 + 5
        self.hCount = hCount
        self.pause = False

        self.humidity = {}
        self.topicFinal = ""

        # create instances of humidity sensor
        self.humiditySensList = []

        for i in range(0, self.hCount):
            id = createInstanceID(self.lineNum, 'S', ABV_DICT["humidity"], i)
            self.humiditySensList.append(HumiditySensor(id))
            print(id)

    def startSim(self, clientName):

        startTime = datetime.datetime.now()
        timeDiff = 0
        sec15Count = 15
        keySet = True

        while self.simTime > 0 and not(self.pause):

            if(int(timeDiff) == 1):

                startTime = currTime
                self.simTime -= 1
                sec15Count -= 1

            # check 15 seconds have passed or not
            if(sec15Count == 0):
                sec15Count = 15
                # sense room humidity sensor values
                for x in range(self.hCount):
                    key = self.humiditySensList[x].getInstanceID()
                    self.humidity[key] = self.humiditySensList[x].sense()
                    if(keySet):
                        self.topicFinal += "_"+key

                keySet = False

                publisher_data(
                    topicDict["HA"], self.humidity, clientName)
                print(f"Humidity: {self.humidity}")
                #print("-----------15 sec over HumiditySensor---------")

            currTime = datetime.datetime.now()
            timeDiff = (currTime - startTime).total_seconds()
        self.stopSim()

    def stopSim(self):
        self.simTime = 0
        print("----Simulation endded----")

    def pauseSim(self):
        self.pause = True


def main():
    simHumiditySensorClient = mqtt.Client(
        clientDict["simHumiditySensorClient"], clean_session=True)

    simHumiditySensorClient.on_connect = on_connect
    simHumiditySensorClient.on_message = on_message

    simHumiditySensorClient.connect(brokerHost, brokerPort, brokerKeepAlive)
    time.sleep(0.2)

    test = simHumiditySensor(1, simTime=SIMULATION_TIME)

    simHumiditySensorClient.loop_start()
    test.startSim(simHumiditySensorClient)
    simHumiditySensorClient.loop_stop()

    simHumiditySensorClient.disconnect()


if __name__ == "__main__":
    main()
