import ptydash.interface


class VideoCard(ptydash.interface.Card):
    """
    A Card representing a video feed.
    """
    template = 'modules/videocard.html'

    def __init__(self, id, text=None, update_delay=1000,
                 source=None, mimetype=None):
        """
        :param id: A unique id for the element to be used to receive information via a WebSocket
        :param text: Text associated with this element - usually a description or caption
        :param update_delay: Delay between UI updates for this card in milliseconds
        :param source: Video source file / URL
        :param mimetype: Mimetype of video source file - optional
        """
        super(VideoCard, self).__init__(id, text, update_delay)

        self.source = source
        self.mimetype = mimetype
