"""
This module contains classes representing objects displayed on the dashboard.
"""

import copy
import io

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
            item = copy.deepcopy(item)
            type = item.pop('type')
            id = item.pop('id')

            klass = globals()[type]
            card = klass(id,
                         **item)
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

    def get_message(self, layout):
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

    def __init__(self, id, text=None, update_delay=1000, **kwargs):
        """
        Init.

        :param id: A unique id for the element to be used to receive information via a WebSocket
        :param text: Text associated with this element - usually a description or caption
        :param update_delay: Delay between UI updates for this card in milliseconds
        """
        super(ImageCard, self).__init__(id, text, update_delay)

        self.image = None

    def get_message(self, layout):
        """
        Create the message that must be sent via WebSocket to update this Card.

        :return: WebSocket message dictionary
        """
        self.image = ptydash.graphing.get_graph()
        graph_encoded = ptydash.utils.bytes_to_base64(self.image)

        return {
            'topic': 'update',
            'id': self.id,
            'data': {
                'image': graph_encoded,
            }
        }


class ImageChildCard(Card):
    template = 'modules/imagecard.html'

    def __init__(self, id, text=None, update_delay=1000, parent=None, **kwargs):
        """
        Init.

        :param id: A unique id for the element to be used to receive information via a WebSocket
        :param text: Text associated with this element - usually a description or caption
        :param update_delay: Delay between UI updates for this card in milliseconds
        """
        super(ImageChildCard, self).__init__(id, text, update_delay)

        self.parent = parent

    def get_message(self, layout):
        image = layout[self.parent].image
        if image is not None:
            graph_encoded = ptydash.utils.bytes_to_base64(layout[self.parent].image)
        else:
            graph_encoded = ''

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

    def __init__(self, id, text=None, update_delay=1000, **kwargs):
        """
        Initialize counter.

        :param id: A unique id for the element to be used to receive information via a WebSocket
        :param text: Text associated with this element - usually a description or caption
        :param update_delay: Delay between UI updates for this card in milliseconds
        """
        super(UpdateCounterCard, self).__init__(id, text, update_delay)

        self.counter = 0

    def get_message(self, layout):
        """
        Create the message that must be sent via WebSocket to update this Card.

        :return: WebSocket message dictionary
        """
        self.counter += 1

        return {
            'topic': 'update',
            'id': self.id,
            'data': {
                'count': self.counter,
            }
        }


class PtyPyClientCard(Card):
    """
    A Card representing a PtyPy client which auto-refreshes.
    """
    template = 'modules/ptypyclientcard.html'

    def __init__(self, id, text=None, update_delay=1000,
                 address=None, port=None):
        """
        Initialize PtyPy client and plotter.

        :param id: A unique id for the element to be used to receive information via a WebSocket
        :param text: Text associated with this element - usually a description or caption
        :param update_delay: Delay between UI updates for this card in milliseconds
        """
        from ptypy.core.ptycho import DEFAULT_autoplot
        from ptypy.io.interaction import Client_DEFAULT
        from ptypy.utils import plot_client
        from ptypy.utils.parameters import Param

        super(PtyPyClientCard, self).__init__(id, text, update_delay)

        self.plot_config = DEFAULT_autoplot.copy(depth=3)

        self.client_config = Param(Client_DEFAULT)
        if address is not None:
            self.client_config.address = address
        if port is not None:
            self.client_config.port = port

        self.pc = plot_client.PlotClient(self.client_config)
        self.pc.start()

        self.plotter = plot_client.MPLplotter()

        self.initialized = False

    def get_message(self, layout):
        """
        Create the message that must be sent via WebSocket to update this Card.

        :return: WebSocket message dictionary
        """
        status = self.pc.status
        graph_encoded = None

        if status == self.pc.STOPPED:
            # Restart client so we can connect to a new server - not just one-shot
            self.pc.start()
            self.pc._has_stopped = False
            self.initialized = False

        elif status == self.pc.DATA:
            self.plotter.pr, self.plotter.ob, runtime = self.pc.get_data()
            self.plotter.runtime.update(runtime)

            if not self.initialized:
                if self.pc.config:
                    self.plot_config.update(self.pc.config)

                self.plotter.update_plot_layout(self.plot_config.layout)
                self.initialized = True

            self.plotter.plot_all()

            buffer = io.BytesIO()
            self.plotter.plot_fig.savefig(buffer, format='png')
            buffer.seek(0)

            graph_encoded = ptydash.utils.bytes_to_base64(buffer.read())

        return {
            'topic': 'update',
            'id': self.id,
            'data': {
                'connected': self.pc.client.connected,
                'status': status,
                'image': graph_encoded,
            }
        }
