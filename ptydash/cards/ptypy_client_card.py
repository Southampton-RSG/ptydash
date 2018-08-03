import ptydash.interface


class PtyPyClientCard(ptydash.interface.Card):
    """
    A Card representing a PtyPy client which auto-refreshes.
    """
    template = 'modules/ptypyclientcard.html'

    def __init__(self, id, text=None, update_delay=1000,
                 address=None, port=None):
        """
        Initialize PtyPy client and plotter.

        :param id: A unique id for the element to be used to receive information via a WebSocket
        :param text: Text associated with this element - usually a description or caption
        :param update_delay: Delay between UI updates for this card in milliseconds
        """
        from ptypy.core.ptycho import DEFAULT_autoplot
        from ptypy.io.interaction import Client_DEFAULT
        from ptypy.utils import plot_client
        from ptypy.utils.parameters import Param

        super(PtyPyClientCard, self).__init__(id, text, update_delay)

        self.plot_config = DEFAULT_autoplot.copy(depth=3)

        self.client_config = Param(Client_DEFAULT)
        if address is not None:
            self.client_config.address = address
        if port is not None:
            self.client_config.port = port

        self.pc = plot_client.PlotClient(self.client_config)
        self.pc.start()

        self.plotter = plot_client.MPLplotter()

        self.initialized = False

    def get_message(self):
        """
        Create the message that must be sent via WebSocket to update this Card.

        :return: WebSocket message dictionary
        """
        status = self.pc.status
        graph_encoded = None

        if status == self.pc.STOPPED:
            # Restart client so we can connect to a new server - not just one-shot
            self.pc.start()
            self.pc._has_stopped = False
            self.initialized = False

        elif status == self.pc.DATA:
            self.plotter.pr, self.plotter.ob, runtime = self.pc.get_data()
            self.plotter.runtime.update(runtime)

            if not self.initialized:
                if self.pc.config:
                    self.plot_config.update(self.pc.config)

                self.plotter.update_plot_layout(self.plot_config.layout)
                self.initialized = True

            self.plotter.plot_all()

            graph_encoded = ptydash.interface.fig_to_base64(self.plotter.plot_fig)

        return {
            'topic': 'update',
            'id': self.id,
            'data': {
                'connected': self.pc.client.connected,
                'status': status,
                'image': graph_encoded,
            }
        }
