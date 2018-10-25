"""
This module processes MQTT data into graphical images
"""

import io

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import numpy as np

import ptydash.interface
from ptydash.cards import image_card


class EmbeddedGraphsCard(image_card.ImageCard):
    """
    Create graphical images with embedded graphical images.
    """
    def get_graph(self, data):
        """
        Process MQTT data stream output into graphical points.

        We heard you like graphs, so here's a graph inside a graph

        :return: graph image of MQTT data
        """
        if data is None:
            return None

        # create the graph
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # split mqtt message stream into manageable chunks
        # header:, value, header:, value
        # we want value 1 and value 2, we'll use the headers in a mo.
        self.data_list = str.split(data)

        # add the data values to a list to populate the graph
        self.x_data_storage.append(int(self.data_list[1]))
        self.y_data_storage.append(int(self.data_list[3]))

        # set graph info before plotting/scattering
        plt.axis([0, 100, 0, 100])  # fix axis scale 0-100
        plt.xlabel(self.data_list[0])  # set xlabel to header 1
        plt.ylabel(self.data_list[2])  # set ylabel to header 2
        #  create scatter graph
        plt.scatter([self.x_data_storage], [self.y_data_storage], marker='s')

        # add subplots:
        inset_axes(ax, width="50%", height="50%", loc=1)

        # create hist graph from random data
        t = np.arange(0.0, 10.0, 0.001)
        r = np.exp(-t[:1000] / 0.05)  # impulse response
        x = np.random.randn(len(t))
        s = np.convolve(x, r)[:len(x)] * 0.001
        plt.hist(s, 400, density=1)

        # plot graph
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close()
        buffer.seek(0)

        graph_encoded = ptydash.interface.bytes_to_base64(buffer.read())
        return graph_encoded
