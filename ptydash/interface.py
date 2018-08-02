"""
This module contains classes representing objects displayed on the dashboard.
"""

import ptydash.graphing
import ptydash.utils


class DoesNotUpdate(Exception):
    pass


class Layout(object):
    """
    Class holding a sequence of Cards as displayed by the UI.
    """
    def __init__(self, cards=None):
        self.cards = cards

    @classmethod
    def from_config(cls, config):
        """
        Read a Layout sequence of Cards from a config dictionary.

        :param config: Config dictionary
        :return: Instance of Layout
        """
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
    """
    An interface element to be represented on the dashboard.
    """
    template = None

    def __init__(self, id, text=None):
        """
        An interface element to be represented on the dashboard.

        :param id: A unique id for the element to be used to receive information via a WebSocket
        :param text: Text associated with this element - usually a description or caption
        """
        self.id = id
        self.text = text

    def get_message(self):
        """
        Create the message that must be sent via WebSocket to update this Card.

        :return: WebSocket message dictionary
        """
        raise DoesNotUpdate(self)


class TextCard(Card):
    """
    A basic Card representing a simple block of text.
    """
    template = 'modules/textcard.html'


class ImageCard(Card):
    """
    A Card representing a graph which auto-refreshes.
    """
    template = 'modules/imagecard.html'

    def get_message(self):
        """
        Create the message that must be sent via WebSocket to update this Card.

        :return: WebSocket message dictionary
        """
        graph = ptydash.graphing.get_graph()
        graph_encoded = ptydash.utils.bytes_to_base64(graph)

        return {
            'topic': 'update',
            'id': self.id,
            'data': {
                'image': graph_encoded,
            }
        }


class UpdateCounterCard(Card):
    """
    Card that displays the number of updates that have been requested.

    Use this as an example of a Card which stores state.
    """
    template = 'modules/updatecountercard.html'

    def __init__(self, id, text=None):
        super(UpdateCounterCard, self).__init__(id, text)

        self.counter = 0

    def get_message(self):
        self.counter += 1

        return {
            'topic': 'update',
            'id': self.id,
            'data': {
                'count': self.counter,
            }
        }
