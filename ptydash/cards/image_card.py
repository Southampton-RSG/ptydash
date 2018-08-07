import matplotlib.pyplot as plt
import numpy as np
import io

import ptydash.interface

data = None
Xdatastorage = []
Ydatastorage = []

def get_graph():
    # data management
    print("this is the data: " + data)

    # split mqtt message stream into manageable chunks
    # header:, value, header:, value
    # we want value 1 and value 2, discard the headers for now.
    datalist = str.split(data)
    print datalist[0] + datalist[1]
    print datalist[2] + datalist[3]

    # add the data values to a list to populate a graph once the length of the list is equal to 10 data points
    Xdatastorage.append(datalist[1])
    Ydatastorage.append(datalist[3])

    # create the graph: using matplotlib.pyplot
    # set graph info before plotting/scattering
    plt.axis([0, 100, 0, 100]) # fix axis scale 0-100
    plt.xlabel(datalist[0]) # set xlabel to header 1
    plt.ylabel(datalist[2]) # set ylabel to header 2
    plt.scatter([Xdatastorage], [Ydatastorage], marker='s')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    graph_encoded = ptydash.interface.bytes_to_base64(buffer.read())
    return graph_encoded


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
        graph_encoded = get_graph()

        return {
            'topic': 'update',
            'id': self.id,
            'data': {
                'image': graph_encoded,
            }
        }
