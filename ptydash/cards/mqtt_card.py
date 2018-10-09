"""
this module allows a user to send an mqtt data string to a specified server and topic_id
"""

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

        self.client = 'PTYDASHCLIENT-' + self.id
        self.host = hostname
        self.topic = topic_id

        self.client = mqtt.Client(self.client)
        self.client.connect(self.host, port=1883, keepalive=60, bind_address="")

        self.latest_command = None

    def process_form(self, form_dict):
        if 'command' in form_dict:
            self.latest_command = form_dict['command'][0]
            self.client.publish(self.topic, form_dict['command'][0])
