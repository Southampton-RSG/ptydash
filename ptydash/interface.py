"""
This module contains classes representing objects displayed on the dashboard.
"""

import base64
import copy
import io
import logging
import uuid

import six

import ptydash


logger = logging.getLogger(__name__)


def bytes_to_base64(byte_seq):
    # type: (...) -> str
    """
    Convert a byte sequence (e.g. io.BytesIO) to a base64 string.

    :param bytes: Byte sequence to convert
    :return: Base64 string
    """
    return base64.b64encode(byte_seq).decode('utf-8')


def fig_to_base64(fig):
    # type: (...) -> str
    """
    Render a matplotlib figure into a base64 string.

    :param fig: Figure to render
    :return: Base64 string
    """
    byte_buffer = io.BytesIO()
    fig.savefig(byte_buffer, format='png')
    byte_buffer.seek(0)

    return bytes_to_base64(byte_buffer.read())


class MatplotlibBackend(object):
    """
    Context Manager to temporarily switch Matplotlib backend.
    """
    def __init__(self, backend):
        self.backend = backend
        self.old_backend = None

    def __enter__(self):
        import matplotlib.pyplot

        self.old_backend = matplotlib.get_backend()
        matplotlib.pyplot.switch_backend(self.backend)

    def __exit__(self, exc_type, exc_val, exc_tb):
        import matplotlib.pyplot
        matplotlib.pyplot.switch_backend(self.old_backend)


class DoesNotUpdate(Exception):
    """
    Exception raised if a Card does not support updating via WebSocket.
    """


class CardInitializationError(Exception):
    """
    Exception which should be raised if a Card fails to initialize.
    """


class Layout(list):
    """
    Class holding a list of Cards to be displayed by the UI.
    """
    @classmethod
    def from_config(cls, config):
        # type: (dict) -> Layout
        """
        Read a Layout sequence of Cards from a config dictionary.

        :param config: Config dictionary
        :return: Instance of Layout
        """
        Card.load_plugins('ptydash/cards')

        obj = cls()

        for item in config['layout']:
            item = copy.deepcopy(item)
            card_type = item.pop('type')

            try:
                card = Card.get_plugin(card_type)(**item)
                obj.append(card)
            except CardInitializationError as exc:
                logger.error('Initializing card type \'%(card_type)s\' failed: %(message)s',
                             {'card_type': card_type, 'message': exc})

        return obj


class Plugin(type):
    """
    Metaclass to allow classes to be loaded dynamically at start of runtime.
    """
    def __init__(cls, name, bases, attrs):
        """
        Register all concrete subclasses when they are defined.
        """
        if not hasattr(cls, '_plugins'):
            cls._plugins = {}

        else:
            cls._plugins[name] = cls

    def get_plugin(cls, class_name):
        # type: (str) -> type
        """
        Find a particular plugin by class name.

        :param class_name: Name of plugin class
        :return: Plugin class
        """
        return cls._plugins[class_name]

    # TODO can plugin loading be made more elegant?
    @staticmethod
    def load_plugins(plugin_dir):
        # type: (str) -> None
        """
        Execute the plugin definitions so they are defined and registered.

        :param plugin_dir: Directory to search for plugins
        """
        import importlib
        import os

        for plugin_filename in os.listdir(os.path.join(ptydash.PROJECT_ROOT, plugin_dir)):
            module_name = plugin_filename.split('.')[0]
            # Exclude __init__.py and __pycache__
            if module_name == '__init__' or module_name == '__pycache__':
                continue

            # Importing a module causes its class definitions to be executed
            # When class definitions are executed they are registered by the Plugin metaclass
            importlib.import_module(plugin_dir.replace('/', '.') + '.' + module_name,
                                    package='ptydash')


class Card(six.with_metaclass(Plugin, object)):
    """
    Base class for all interface elements to be represented on the dashboard.

    When creating a Card plugin, inherit from this class.
    """
    #: Name of the HTML template which renders this :class:`Card`, relative to the PtyDash template directory.
    #: Subclasses of :class:`Card` **must** define this attribute.
    template = None

    def __init__(self, text=None, update_delay=1000):
        # type: (str, int) -> None
        """
        Init.

        :param text: Text associated with this element - usually a description or caption
        :param update_delay: Delay between UI updates for this card in milliseconds
        """
        self.id = str(uuid.uuid4())
        self.text = text
        self.update_delay = update_delay

    def get_message(self):
        # type: () -> dict
        """
        Create the message dictionary that must be sent via WebSocket to update this Card.
        This method is only required to be implemented by subclasses of :class:`Card` if
        they are to be dynamically updated.

        The message dictionary should be of the format:

        .. code-block:: python

           {
             'topic': 'update',
             'id': self.id,
             'data': {
               ...
             }
           }

        Where the dictionary ``data`` contains any data you wish to send to the interface.
        You must ensure that there is complementary JavaScript in the HTML template (:attr:`template`) of the :class:`Card`
        which will receive the ``data`` dictionary and update the HTML representation.

        :return: WebSocket message dictionary
        """
        raise DoesNotUpdate(self)
