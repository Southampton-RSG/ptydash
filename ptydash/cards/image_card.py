"""
This module processes MQTT data into graphical images
"""

import datetime
import io
import uuid

import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt

import ptydash.interface


class ImageCard(ptydash.interface.Card):
    """
    A Card representing a graph which auto-refreshes.
    """
    template = 'modules/imagecard.html'

    def __init__(self, text=None, update_delay=1000, hostname=None, topic_id=None):
        super(ImageCard, self).__init__(text, update_delay)
        self.data = None
        self.x_data_storage = []
        self.y_data_storage = []

        # MQTT data stream connection info
        self.host = hostname
        self.topic_name = topic_id
        self.data_list = []

        self.client_name = "PtyDashClient-" + str(uuid.uuid4())
        self._client = self.mqtt_subscribe()

    def mqtt_subscribe(self):
        """
        MQTT broker subscription.
        """
        client = mqtt.Client(self.client_name)
        client.on_message = self.on_message
        client.connect(self.host, port=1883, keepalive=60, bind_address="")
        client.loop_start()
        client.subscribe(self.topic_name)

        return client

    # message receiver
    def on_message(self, client, userdata, message):
        """
        MQTT callback process to retrieve broker data.

        :param client: unused client data
        :param userdata: unused user data
        :param message: message stream containing data
        """
        self.data = str(message.payload.decode("utf-8"))

    # graph generation
    def get_graph(self, data):
        """
        Process MQTT data stream output into graphical points.

        :return: graph image of MQTT data
        """
        if data is None:
            return None

        # TODO inject function to process expected fomat into k-v mapping
        # split mqtt message stream into manageable chunks
        # header:, value, header:, value
        # we want value 1 and value 2, we'll use the headers in a mo.
        self.data_list = str.split(data)

        if len(self.data_list) >= 5:
            # grab the time data
            date = self.data_list[3]
            time = self.data_list[4]
            dateandtime = date + " " + time

            timestamp = datetime.datetime.strptime(dateandtime, '%Y-%m-%d %H:%M:%S.%f')

            ## this bit might not work
            ## but it might
            ## not tested it.
            """
            days = dates.DayLocator()
            hours = dates.HourLocator(interval=3)
            dfmt = dates.DateFormatter('              %b %d')

            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.xaxis.set_major_locator(days)
            ax.xaxis.set_major_formatter(dfmt)
            ax.xaxis.set_minor_locator(hours)
            ax.grid(True)
            """
            ## end of bit that may not work
            ## or might work
            ## it wasn't tested so dont know...

            plt.xlabel(self.data_list[2])  # set xlabel to timestamp
            plt.ylabel(self.data_list[0])  # set ylabel to Y value header

            self.x_data_storage.append(timestamp)
            self.y_data_storage.append(int(self.data_list[1]))

            plt.plot(self.x_data_storage, self.y_data_storage)

        else:
            self.x_data_storage.append(int(self.data_list[1]))
            self.y_data_storage.append(int(self.data_list[3]))

            plt.axis([0, 100, 0, 100])  # fix axis scale 0-100
            plt.xlabel(self.data_list[0])  # set xlabel to header 1
            plt.ylabel(self.data_list[2])  # set ylabel to header 2

            plt.scatter([self.x_data_storage], [self.y_data_storage], marker='s')

        # Encode graph to base64 image
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)

        graph_encoded = ptydash.interface.bytes_to_base64(buffer.read())
        return graph_encoded

    def get_message(self):
        # type: () -> dict
        """
        Create the message that must be sent via WebSocket to update this Card.

        :return: WebSocket message dictionary
        """
        graph_encoded = self.get_graph(self.data)

        return {
            'topic': 'update',
            'id': self.id,
            'data': {
                'image': graph_encoded,
            }
        }
