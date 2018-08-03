import matplotlib.pyplot as plt
import numpy as np

import ptydash.interface


def get_graph():
    nums = np.random.normal(0, 1, 1000)

    # TODO avoid plt API so we don't need to plt.close()
    fig = plt.figure()
    fig.suptitle('Ptydash Plot')
    ax = fig.subplots()
    ax.hist(nums)

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
