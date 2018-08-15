"""
This module processes mqtt data into graphical images
"""

import random
import io
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
import ptydash.interface


class ImageCard(ptydash.interface.Card):
    """
    A Card representing a graph which auto-refreshes.
    """

    def __init__(self, text=None, update_delay=1000, hostname=None, topic_id=None):
        super(ImageCard, self).__init__(text, update_delay)
        self.data = None
        self.x_data_storage = []
        self.y_data_storage = []
        self.client_list = []
        # mqtt data stream connection info
        self.host = hostname
        self.topic_name = topic_id

        identity = random.randint(0, 100)
        self.client_name = "PTYDASHCLIENT" + str(identity)
        self.client_list.append(self.client_name)
        self.client_create(self.client_name)

    def client_create(self, clientname):
        """
        creates separate mqtt subscription instances for each client
        :param clientname: client identifier
        :return:
        """
        for xyz in self.client_list:
            if xyz == clientname:
                self.mqtt_subscribe(self.client_name, self.host, self.topic_name)

    def mqtt_subscribe(self, client_name, hostname, topic):
        """
        mqtt broker subscription
        :param client_name: client identifier
        :param hostname: mqtt broker
        :param topic: mqtt subscription topic
        :return:
        """
        client = mqtt.Client(client_name)
        client.on_message = self.on_message
        client.connect(hostname, port=1883, keepalive=60, bind_address="")
        client.loop_start()
        client.subscribe(topic)

    # message receiver
    def on_message(self, client, userdata, message):
        """
        mqtt callback process to retrieve broker data
        :param client: unused client data
        :param userdata: unused user data
        :param message: message stream containing data
        :return: message payload string
        """
        # print("message topic=", message.topic)
        # print("message received ", str(message.payload.decode("utf-8")))
        # print("message qos=", message.qos)
        # print("message retain flag=", message.retain)
        out_msg = str(message.payload.decode("utf-8"))
        self.data = out_msg
        return

    # graph generation
    def get_graph(self):
        """
        process mqtt data stream output into graphical points
        :return: graphic image of mqtt data
        """
        if self.data is None:
            return None

        # split mqtt message stream into manageable chunks
        # header:, value, header:, value
        # we want value 1 and value 2, discard the headers for now.
        data_list = str.split(self.data)

        # add the data values to a list to populate the graph
        self.x_data_storage.append(data_list[1])
        self.y_data_storage.append(data_list[3])

        # create the graph
        # set graph info before plotting/scattering
        plt.axis([0, 100, 0, 100])  # fix axis scale 0-100
        plt.xlabel(data_list[0])  # set xlabel to header 1
        plt.ylabel(data_list[2])  # set ylabel to header 2
        plt.scatter([self.x_data_storage], [self.y_data_storage], marker='s')

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)

        graph_encoded = ptydash.interface.bytes_to_base64(buffer.read())
        return graph_encoded

    # A Card representing a graph which auto-refreshes.
    template = 'modules/imagecard.html'

    def get_message(self):
        # type: () -> dict
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
