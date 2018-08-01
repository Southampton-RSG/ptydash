"""
This module contains classes representing objects displayed on the dashboard.

These objects are displayed using the Tornado UIModules in uimodules.py
"""

import ptydash.graphing
import ptydash.utils


class DoesNotUpdate(Exception):
    pass


class Layout(object):
    def __init__(self, cards=None):
        self.cards = cards

    @classmethod
    def from_config(cls, config):
        cards = []
        for item in config['layout']:
            klass = globals()[item['type']]
            card = klass(id=item['id'],
                         text=item['text'])
            cards.append(card)

        return cls(cards)

    def __getitem__(self, item):
        for card in self.cards:
            if card.id == item:
                return card
        raise KeyError(item)

    def __iter__(self):
        return iter(self.cards)


class Card(object):
    template = None

    def __init__(self, id, text=None):
        """
        An auto-refreshing Image to be represented by a uimodules.Image module on the dashboard.

        :param id: A unique id for the image to be used to receive information via a WebSocket
        :param text: Text associated with this image - usually a description or caption
        """
        self.id = id
        self.text = text

    def get_message(self):
        raise DoesNotUpdate(self)


class ImageCard(Card):
    template = 'modules/imagecard.html'

    def get_message(self):
        graph = ptydash.graphing.get_graph()
        graph_encoded = ptydash.utils.bytes_to_base64(graph)

        return {
            'topic': 'update',
            'id': self.id,
            'data': graph_encoded
        }


class TextCard(Card):
    template = 'modules/textcard.html'
