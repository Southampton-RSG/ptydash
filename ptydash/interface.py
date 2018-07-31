"""
This module contains classes representing objects displayed on the dashboard.

These objects are displayed using the Tornado UIModules in uimodules.py
"""


class Image(object):
    def __init__(self, id, text=None):
        """
        An auto-refreshing Image to be represented by a uimodules.Image module on the dashboard.

        :param id: A unique id for the image to be used to receive information via a WebSocket
        :param text: Text associated with this image - usually a description or caption
        """
        self.id = id
        self.text = text
