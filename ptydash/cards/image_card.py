"""
A Card representing a graph which auto-refreshes.
"""

import matplotlib.pyplot as plt
import numpy as np

import ptydash.interface


def get_graph():
    """
    Produce a histogram of random normally distributed numbers.

    :return: Matplotlib Figure
    """
    nums = np.random.normal(0, 1, 1000)

    # TODO Is it possible to avoid having to plt.close()?
    with ptydash.interface.MatplotlibBackend('agg'):
        fig = plt.figure()
        fig.suptitle('Ptydash Plot')
        axes = fig.subplots()
        axes.hist(nums)

    return fig


class ImageCard(ptydash.interface.Card):
    """
    A Card representing a graph which auto-refreshes.
    """
    template = 'modules/imagecard.html'

    def get_message(self):
        """
        Create the message that must be sent via WebSocket to update this Card.

        :return: WebSocket message dictionary
        """
        fig = get_graph()
        graph_encoded = ptydash.interface.fig_to_base64(fig)
        plt.close(fig)

        return {
            'topic': 'update',
            'id': self.id,
            'data': {
                'image': graph_encoded,
            }
        }
