import matplotlib.pyplot as plt
import numpy as np
import io
import paho.mqtt.client as mqtt
import random

import ptydash.interface

class ImageCard(ptydash.interface.Card):#

    def __init__(self, id, text=None, update_delay=1000, hostname=None, topic_id=None, **kwargs):
        super(ImageCard, self).__init__(id, text, update_delay)
        self.data = None
        self.Xdatastorage = []
        self.Ydatastorage = []
        self.clientlist = []
        # mqtt data stream connection info
        self.host = hostname
        self.topicID = topic_id

        identity = random.randint(0, 100)
        self.client_name = "PTYDASHCLIENT" + str(identity)
        self.clientlist.append(self.client_name)
        self.client_create(self.client_name)

    def client_create(self, clientname):
        for x in self.clientlist:
            if x == clientname:
                print("this is my clientname " + clientname)
                self.mqtt_subscribe(self.client_name, self.host, self.topicID)

    def mqtt_subscribe(self, client_name, hostname, topic):
        client = mqtt.Client(client_name)
        client.on_message = self.on_message
        client.connect(hostname, port=1883, keepalive=60, bind_address="")
        client.loop_start()
        client.subscribe(topic)

    # message receiver
    def on_message(self, client, userdata, message):
        #print("message topic=", message.topic)
        #print("message received ", str(message.payload.decode("utf-8")))
        #print("message qos=", message.qos)
        #print("message retain flag=", message.retain)
        outMsg = str(message.payload.decode("utf-8"))
        self.data = outMsg
        return

    # graph generation
    def get_graph(self):
        # data management
        if self.data == None:
            return
        print("data recieved: " + self.data)

        # split mqtt message stream into manageable chunks
        # header:, value, header:, value
        # we want value 1 and value 2, discard the headers for now.
        datalist = str.split(self.data)
        print datalist[0] + datalist[1]
        print datalist[2] + datalist[3]

        # add the data values to a list to populate a graph once the length of the list is equal to 10 data points
        self.Xdatastorage.append(datalist[1])
        self.Ydatastorage.append(datalist[3])

        # create the graph: using matplotlib.pyplot
        # set graph info before plotting/scattering
        plt.axis([0, 100, 0, 100])  # fix axis scale 0-100
        plt.xlabel(datalist[0])  # set xlabel to header 1
        plt.ylabel(datalist[2])  # set ylabel to header 2
        plt.scatter([self.Xdatastorage], [self.Ydatastorage], marker='s')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)

        graph_encoded = ptydash.interface.bytes_to_base64(buffer.read())
        return graph_encoded

    """
    A Card representing a graph which auto-refreshes.
    """
    template = 'modules/imagecard.html'

    def get_message(self):
        """
        Create the message that must be sent via WebSocket to update this Card.

        :return: WebSocket message dictionary
        """
        graph_encoded = self.get_graph()

        return {
            'topic': 'update',
            'id': self.id,
            'data': {
                'image': graph_encoded,
            }
        }

