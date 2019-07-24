"""
this module allows a user to send an mqtt data string to a specified server and topic_id
"""

from __future__ import print_function

import paho.mqtt.client as mqtt

import ptydash.interface


class MqttCard(ptydash.interface.Card):
    """
    send mqtt data string to specified:
    clientname,
    hostname,
    topic_id,
    data-string (actual data to send)
    """
    template = 'modules/mqttcard.html'

    def __init__(self, text=None, update_delay=1000, hostname=None, topic_id=None):
        super(MqttCard, self).__init__(text, update_delay)

        # client ID
        self.client = 'PTYDASHCLIENT'
        # mqtt broker
        self.host = hostname
        # topic id
        self.topic = topic_id

        client = mqtt.Client(self.client)
        client.connect(self.host, port=1883, keepalive=60, bind_address="")

    def send_mqtt(self):
        """
        Send a message over an MQTT bus in a loop forever.
        """
        while True:
            print("Sending data " + self.data + "to host " + self.host + "topic-id " + self.topic + "as " + self.client)
            client.publish(self.topic, self.data)
            client.loop_start()
            client.subscribe(self.topic)
            client.loop_stop()
