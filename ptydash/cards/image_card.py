import matplotlib.pyplot as plt
import numpy as np
import io
import paho.mqtt.client as mqtt

import ptydash.interface

class ImageCard(ptydash.interface.Card):#

    def __init__(self, id, text=None, update_delay=1000, **kwargs):
        super(ImageCard, self).__init__(id, text, update_delay)
        self.data = None
        # mqtt data stream connection
        # mqtt broker hostname
        host = "wonderbox.ecs.soton.ac.uk"
        # TODO add host config entry to config file

        # mqtt client id. Change this to something unique.
        self.client_name = "IAMACLIENT"
        self.client = mqtt.Client(self.client_name)
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.connect(host, port=1883, keepalive=60, bind_address="")
        self.client.subscribe("datadump/tempAndHumid")
        self.client.loop_start()
        # TODO add MQTT topic subscription field to config file

    def on_connect(self, client, userdata, flags, rc):
        print(flags, rc)

    def on_message(self, client, userdata, message):
        print("message topic=", message.topic)
        # print("message received ", str(message.payload.decode("utf-8")))
        # print("message qos=", message.qos)
        # print("message retain flag=", message.retain)
        outMsg = str(message.payload.decode("utf-8"))
        self.data = outMsg
        return

    # graph generation

    def get_graph(self):
        Xdatastorage = []
        Ydatastorage = []
        # data management
        #data = self.on_message().outMsg#
        if self.data == None:
            return
        print("this is the data: " + self.data)

        # split mqtt message stream into manageable chunks
        # header:, value, header:, value
        # we want value 1 and value 2, discard the headers for now.
        datalist = str.split(self.data)
        print datalist[0] + datalist[1]
        print datalist[2] + datalist[3]

        # add the data values to a list to populate a graph once the length of the list is equal to 10 data points
        Xdatastorage.append(datalist[1])
        Ydatastorage.append(datalist[3])

        # create the graph: using matplotlib.pyplot
        # set graph info before plotting/scattering
        plt.axis([0, 100, 0, 100])  # fix axis scale 0-100
        plt.xlabel(datalist[0])  # set xlabel to header 1
        plt.ylabel(datalist[2])  # set ylabel to header 2
        plt.scatter([Xdatastorage], [Ydatastorage], marker='s')

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

