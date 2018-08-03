import io

import matplotlib.pyplot as plt
import numpy as np

import ptydash.interface


def get_graph():
    nums = np.random.normal(0, 1, 1000)

    fig = plt.figure()
    fig.suptitle('Ptydash Plot')
    ax = fig.subplots()
    ax.hist(nums)

    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)

    return buffer.read()


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
        graph = get_graph()
        graph_encoded = ptydash.interface.bytes_to_base64(graph)

        return {
            'topic': 'update',
            'id': self.id,
            'data': {
                'image': graph_encoded,
            }
        }
