"""
A Card representing a video feed.
"""

import ptydash.interface


class VideoCard(ptydash.interface.Card):
    """
    A Card representing a video feed.
    """
    template = 'modules/videocard.html'

    def __init__(self, text=None, update_delay=1000,
                 source=None, mimetype=None):
        # type: (str, int, str, str) -> None
        """
        :param text: Text associated with this element - usually a description or caption
        :param update_delay: Delay between UI updates for this card in milliseconds
        :param source: Video source file / URL
        :param mimetype: Mimetype of video source file - optional
        """
        super(VideoCard, self).__init__(text, update_delay)

        self.source = source
        self.mimetype = mimetype
