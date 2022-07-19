from sensorClass.client_broker_data import *
from sensorClass.act_TempAndHumidity import *


# Function to call publisher to send data
def publisher_data(input_topic_name, payload_data, myclient):
    publish_data = json.dumps(payload_data, indent=4)
    myclient.publish(input_topic_name, publish_data, QOS)
    print("Publishing to :" + input_topic_name + "data:" + publish_data)
    time.sleep(0.1)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe(topicDict["DA"], QOS)
    print("--Subscribed to :"+topicDict["DA"])
    time.sleep(0.2)


def on_message(client, userdata, msg):
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    dataReceived = json.loads(m_decode)  # decode json data
    print(f"Dust: {dataReceived}, {msg.topic}")
    if 'server' in msg.topic:
        print("Change state command received from server")
        if userdata.dustAct.getState() != dataReceived:
            userdata.dustAct.changeState(dataReceived)
    else:
        userdata.dustAct.updateValue(dataReceived)
        dataSend = {userdata.dustAct.getInstanceID(): userdata.dustAct.getState()}
        publisher_data(topicDict["DA"]+"State", dataSend, client)
        publisher_data(topicDict["RPi"], {"Dust":userdata.dustAct.getState()}, client)


class simDustAct():
    """docstring for simDustAct"""

    #LineNum in int
    # passed as simTime in unit minutes, stored as seconds

    def __init__(self, lineNum, simTime=5):
        super(simDustAct, self).__init__()
        self.lineNum = lineNum
        self.simTime = simTime*60 + 5
        self.pause = False

        # create instances of room temperature actuator

        identity = createInstanceID(
            self.lineNum, 'A', ABV_DICT["dustActuator"], 0)
        self.dustAct = dustAction(instanceID=identity)
        print(identity)

    def startSim(self, clientName):

        startTime = datetime.datetime.now()
        timeDiff = 0
        sec15Count = 15

        while self.simTime > 0 and not(self.pause):

            if(int(timeDiff) == 1):

                startTime = currTime
                self.simTime -= 1
                sec15Count -= 1

            if sec15Count == 0:
                sec15Count = 15

                dataSend = {self.dustAct.getInstanceID(): self.dustAct.getState()}
                #publisher_data(topicDict["DA"]+"State", dataSend, clientName)

            time.sleep(0.1)
            currTime = datetime.datetime.now()
            timeDiff = (currTime - startTime).total_seconds()
        self.stopSim()

    def stopSim(self):
        self.simTime = 0
        print("----Simulation endded----")

    def pauseSim(self):
        self.pause = True


def main():
    simDustActClient = mqtt.Client(
        clientDict["simDustActClient"], clean_session=True)

    simDustActClient.on_connect = on_connect
    simDustActClient.on_message = on_message

    simDustActClient.connect(brokerHost, brokerPort, brokerKeepAlive)
    time.sleep(0.1)

    test = simDustAct(1, SIMULATION_TIME)

    userdata = test

    simDustActClient.user_data_set(userdata)

    simDustActClient.loop_start()
    test.startSim(simDustActClient)
    simDustActClient.loop_stop()

    simDustActClient.disconnect()


if __name__ == "__main__":
    main()