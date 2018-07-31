"""
This module contains classes representing objects displayed on the dashboard.

These objects are displayed using the Tornado UIModules in uimodules.py
"""


from ptydash import graphing
from ptydash import uimodules
from ptydash.utils import bytes_to_base64


class Layout(object):
    def __init__(self, cards=None):
        self.cards = cards

    def send_cards(self):
        return [
            {
                'topic': 'update',
                'id': card.id,
                'data': card.card_message()
            } for card in self.cards
        ]

    def __iter__(self):
        return iter(self.cards)


class Image(object):
    def __init__(self, id, text=None):
        """
        An auto-refreshing Image to be represented by a uimodules.Image module on the dashboard.

        :param id: A unique id for the image to be used to receive information via a WebSocket
        :param text: Text associated with this image - usually a description or caption
        """
        self.id = id
        self.text = text

    def card_message(self):
        return bytes_to_base64(graphing.get_graph())

    @property
    def uimodule(self):
        return uimodules.Image
