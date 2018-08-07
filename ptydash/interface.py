"""
This module contains classes representing objects displayed on the dashboard.
"""

import base64
import copy
import io

import six


def bytes_to_base64(bytes):
    """
    Convert a byte sequence (e.g. io.BytesIO) to a base64 string.

    :param bytes: Byte sequence to convert
    :return: Base64 string
    """
    return base64.b64encode(bytes).decode('utf-8')


def fig_to_base64(fig):
    """
    Render a matplotlib figure into a base64 string.

    :param fig: Figure to render
    :return: Base64 string
    """
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    return bytes_to_base64(buffer.read())


class MatplotlibBackend(object):
    def __init__(self, backend):
        self.backend = backend

    def __enter__(self):
        import matplotlib.pyplot

        self.old_backend = matplotlib.get_backend()
        matplotlib.pyplot.switch_backend(self.backend)

    def __exit__(self, exc_type, exc_val, exc_tb):
        import matplotlib.pyplot
        matplotlib.pyplot.switch_backend(self.old_backend)


class DoesNotUpdate(Exception):
    pass


class Layout(list):
    """
    Class holding a list of Cards to be displayed by the UI.
    """
    @classmethod
    def from_config(cls, config):
        """
        Read a Layout sequence of Cards from a config dictionary.

        :param config: Config dictionary
        :return: Instance of Layout
        """
        Card.load_plugins('ptydash/cards')

        obj = cls()

        for item in config['layout']:
            item = copy.deepcopy(item)
            type = item.pop('type')
            id = item.pop('id')

            card = Card.plugins[type](id, **item)
            obj.append(card)

        return obj


class Plugin(type):
    """
    Metaclass to allow classes to be loaded dynamically at start of runtime.
    """
    def __init__(cls, name, bases, attrs):
        """
        Register all concrete subclasses when they are defined.
        """
        if not hasattr(cls, 'plugins'):
            cls.plugins = {}

        else:
            cls.plugins[name] = cls

    # TODO can plugin loading be made more elegant?
    @staticmethod
    def load_plugins(plugin_dir):
        """
        Execute the plugin definitions so they are defined and registered.

        :param plugin_dir: Directory to search for plugins
        """
        import importlib
        import os

        for f in os.listdir(plugin_dir):
            module_name = f.split('.')[0]
            if module_name == '__init__':
                continue

            # Importing a module causes its class definitions to be executed
            # When class definitions are executed they are registered by the Plugin metaclass
            importlib.import_module('.'.join(plugin_dir.split('/')) + '.' + module_name)


class Card(six.with_metaclass(Plugin, object)):
    """
    Base class for all interface elements to be represented on the dashboard.

    When creating a Card plugin, inherit from this class.
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
