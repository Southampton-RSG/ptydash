"""
Card that displays the number of updates that have been requested.
"""

import ptydash.interface


class UpdateCounterCard(ptydash.interface.Card):
    """
    Card that displays the number of updates that have been requested.

    Use this as an example of a Card which stores state.
    """
    template = 'modules/updatecountercard.html'

    def __init__(self, title=None, text=None, update_delay=1000):
        # type: (str, str, int) -> None
        """
        Initialize counter.

        :param text: Text associated with this element - usually a description or caption
        :param update_delay: Delay between UI updates for this card in milliseconds
        """
        super(UpdateCounterCard, self).__init__(title, text, update_delay)

        self.counter = 0

    def get_message(self):
        # type: () -> dict
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
