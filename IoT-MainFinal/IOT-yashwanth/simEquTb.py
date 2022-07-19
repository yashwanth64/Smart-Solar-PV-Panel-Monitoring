from sensorClass.client_broker_data import *
from sensorClass.equipment import *


# Function to call publisher to send data
def publisher_data(input_topic_name, payload_data, myclient):
    publish_data = json.dumps(payload_data, indent=4)
    myclient.publish(input_topic_name, publish_data, QOS)
    print("Publishing to :" + input_topic_name)
    time.sleep(0.1)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    identity = userdata.tb.getInstanceID()
    client.subscribe(topicDict["PET"] + identity + "/#", qos=QOS)
    print("--Subscribed to :" + topicDict["PET"] + identity + "/#")
    time.sleep(0.1)


def on_message(client, userdata, msg):

    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    dataReceived = json.loads(m_decode)  # decode json data

    print("Server msg received :" + msg.topic)

    newTopic = topicDict["TB"] + userdata.tb.getInstanceID() + "/" + dataReceived

    if dataReceived == userdata.topicListSend[0]:
        data = {userdata.tb.getInstanceID(): userdata.tb.getToBeCalibDate()}

    elif dataReceived == userdata.topicListSend[1]:
        data = {userdata.tb.getInstanceID(): userdata.tb.doSelfCheck()}

    publisher_data(newTopic, data, client)


class simEquTb:
    """docstring for simEquTb"""

    # LineNum in int
    # passed as simTime in unit minutes, stored as seconds

    def __init__(self, lineNum, simTime=5):
        super(simEquTb, self).__init__()
        self.lineNum = lineNum
        self.simTime = simTime * 60 + 5
        self.pause = False

        self.topicListSend = ["getCalibDate", "doCheck", "value"]

        # create instances of room temperature actuator

        id = createInstanceID(self.lineNum, "E", ABV_DICT["testBentch"], 0)
        self.tb = testBench(instanceID=id)
        print(id)

    def startSim(self, clientName):

        startTime = datetime.datetime.now()
        timeDiff = 0
        sec15Count = 15
        tempID = self.tb.getInstanceID()
        topic = topicDict["TB"] + tempID + "/" + self.topicListSend[2]
        result = {}

        while self.simTime > 0 and not (self.pause):

            if int(timeDiff) == 1:

                startTime = currTime
                self.simTime -= 1
                sec15Count -= 1

            if sec15Count == 0:
                sec15Count = 15

                result["ValueVolt"] = self.tb.getVoltage()
                result["ValueCurr"] = self.tb.getCurrent()

                publisher_data(topic, {tempID: result}, clientName)

            time.sleep(0.1)
            currTime = datetime.datetime.now()
            timeDiff = (currTime - startTime).total_seconds()
        self.stopSim()

    def stopSim(self):
        self.simTime = 0
        print("----Simulation Ended---")

    def pauseSim(self):
        self.pause = True


def main():
    simEquTbClient = mqtt.Client(clientDict["simEquTbClient"], clean_session=True)

    simEquTbClient.on_connect = on_connect
    simEquTbClient.on_message = on_message

    simEquTbClient.connect(brokerHost, brokerPort, brokerKeepAlive)
    time.sleep(0.1)

    test = simEquTb(1, SIMULATION_TIME)

    userdata = test

    simEquTbClient.user_data_set(userdata)

    simEquTbClient.loop_start()
    test.startSim(simEquTbClient)
    simEquTbClient.loop_stop()

    simEquTbClient.disconnect()


if __name__ == "__main__":
    main()
