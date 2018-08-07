import threading
import time
import random
import paho.mqtt.client as mqtt
import ptydash.graphing as graph

# mqtt broker
host = "wonderbox.ecs.soton.ac.uk"

# mqtt client id. Change this to something unique.
client_name = "IAMACLIENT"

logFile = "log.txt"

def on_message(client,userdata,message):
    #print("message topic=", message.topic)
    #print("message received ", str(message.payload.decode("utf-8")))
    # print("message qos=", message.qos)
    # print("message retain flag=", message.retain)
    outMsg = str(message.payload.decode("utf-8"))
    graph.data = outMsg
    return

client = mqtt.Client(client_name)
client.on_message = on_message
client.connect(host, port=1883, keepalive=60, bind_address="")

def send_mqtt():
    while True:
        lf = open(logFile,"a")
        lf.write("Posting data to "+host+" at "+str(time.time()) + "\n")
        lf.close()

        #make up some data, this should be sensors or whatever
        temperatureReading = random.randint(0,100)
        humidityReading = random.randint(0,100)
        tempAndHumid = "Temperature: " + str(temperatureReading) + " Humidity: " + str(humidityReading)

        #example publish setting
        client.publish("datadump/tempAndHumid",tempAndHumid)

        time.sleep(2)
    return

def write_data():

    while True:
        client.loop_start()
        #example subscribe setting
        client.subscribe("datadump/tempAndHumid")
        client.loop_stop()

    return

threads = []

tMqtt = threading.Thread(target=send_mqtt)
tWrite = threading.Thread(target=write_data)

threads.append(tMqtt)
threads.append(tWrite)

tMqtt.start()
tWrite.start()
