"""
This module contains classes representing objects displayed on the dashboard.
"""

import base64
import copy

import six


def bytes_to_base64(bytes):
    return base64.b64encode(bytes).decode('utf-8')


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
            item = copy.deepcopy(item)
            type = item.pop('type')
            id = item.pop('id')

            card = Card.plugins[type](id, **item)
            cards.append(card)

        return cls(cards)

    def __getitem__(self, item):
        for card in self.cards:
            if card.id == item:
                return card
        raise KeyError(item)

    def __iter__(self):
        return iter(self.cards)


class Plugin(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = {}

        else:
            cls.plugins[name] = cls


class Card(six.with_metaclass(Plugin, object)):
    """
    An interface element to be represented on the dashboard.
    """
    template = None

    def __init__(self, id, text=None, update_delay=1000, **kwargs):
        """
        Init.

        :param id: A unique id for the element to be used to receive information via a WebSocket
        :param text: Text associated with this element - usually a description or caption
        :param update_delay: Delay between UI updates for this card in milliseconds
        """
        self.id = id
        self.text = text
        self.update_delay = update_delay

    def get_message(self):
        """
        Create the message that must be sent via WebSocket to update this Card.

        :return: WebSocket message dictionary
        """
        raise DoesNotUpdate(self)
