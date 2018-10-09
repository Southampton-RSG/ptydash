"""
this module allows a user to send an mqtt data string to a specified server and topic_id
"""

import ptydash.interface
import paho.mqtt.client as mqtt

class MqttCard(ptydash.interface.card):
    """
    send mqtt data string to specified:
    clientname,
    hostname,
    topic_id,
    data-string (actual data to send)
    """

    def __init__(self, clientname=None, hostname=None, topic_id=None, data_string=None):
        # client ID
        self.client = clientname
        # mqtt broker
        self.host = hostname
        # topic id
        self.topic = topic_id
        # data to send
        self.data = data_string
        self.send_mqtt()

    def send_mqtt(self):
        client = mqtt.Client(self.client)
        client.connect(self.host, port=1883, keepalive=60, bind_address="")
        while True:
            print("Sending data " + self.data + "to host " + self.host + "topic-id " + self.topic + "as " + self.client)
            client.publish(self.topic, self.data)
            client.loop_start()
            client.subscribe(self.topic)
            client.loop_stop()
        return

    template = 'modules/mqttcard.html'


