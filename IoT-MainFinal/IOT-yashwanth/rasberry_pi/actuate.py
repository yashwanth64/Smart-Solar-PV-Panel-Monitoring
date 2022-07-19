import paho.mqtt.client as mqtt
import json, time

brokerHost = "broker.emqx.io"  # "broker.hivemq.io" #"localhost"
brokerPort = 1883
brokerKeepAlive = 60

QOS = 1

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("room/room1/rapsberry_pi/actuators/",  QOS)
    print("--Subscribed to :"+"room/room1/rapsberry_pi/actuators/")
    time.sleep(0.2)


def on_message(client, userdata, msg):
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    dataReceived = json.loads(m_decode)  # decode json data
    print(f"Temperature: {dataReceived}, {msg.topic}")
    if 'ON' in dataReceived:
        pass
    elif 'OFF' in dataReceived:
        pass

def main():
    simDustSensorClient = mqtt.Client(
        "raspberry_pi", clean_session=True)

    simDustSensorClient.on_connect = on_connect
    simDustSensorClient.on_message = on_message

    simDustSensorClient.connect(brokerHost, brokerPort, brokerKeepAlive)