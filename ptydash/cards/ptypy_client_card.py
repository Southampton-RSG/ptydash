"""
A Card representing a PtyPy client which auto-refreshes.
"""

import ptydash.interface


class PtyPyClientCard(ptydash.interface.Card):
    """
    A Card representing a PtyPy client which auto-refreshes.
    """
    template = 'modules/ptypyclientcard.html'
    help_string = 'This card displays the progress of a running PtyPy image reconstruction'

    def __init__(self, text=None, update_delay=1000,
                 address=None, port=None):
        # type: (str, int, str, int) -> None
        """
        Initialize PtyPy client and plotter.

        :param text: Text associated with this element - usually a description or caption
        :param update_delay: Delay between UI updates for this card in milliseconds
        """
        try:
            import ptypy
            from ptypy.utils import plot_client
            from ptypy.utils.parameters import Param

            DEFAULT_autoplot = ptypy.core.Ptycho.DEFAULT.io.autoplot
            Client_DEFAULT = ptypy.io.interaction.Client.DEFAULT

        except ImportError as exc:
            raise ptydash.interface.CardInitializationError(exc)

        super(PtyPyClientCard, self).__init__(text, update_delay)

        self.plot_config = DEFAULT_autoplot.copy(depth=3)

        self.client_config = Param(Client_DEFAULT)
        if address is not None:
            self.client_config.address = address
        if port is not None:
            self.client_config.port = port

        self.plot_client = plot_client.PlotClient(self.client_config)
        self.plot_client.start()

        self.plotter = plot_client.MPLplotter()

        self.initialized = False

    def get_message(self):
        # type: () -> dict
        """
        Create the message that must be sent via WebSocket to update this Card.

        :return: WebSocket message dictionary
        """
        status = self.plot_client.status
        graph_encoded = None

        if status == self.plot_client.STOPPED:
            # Restart client so we can connect to a new server - not just one-shot
            self.plot_client.start()
            self.plot_client._has_stopped = False
            self.initialized = False

        elif status == self.plot_client.DATA:
            self.plotter.pr, self.plotter.ob, runtime = self.plot_client.get_data()
            self.plotter.runtime.update(runtime)

            if not self.initialized:
                if self.plot_client.config:
                    self.plot_config.update(self.plot_client.config)

                self.plotter.update_plot_layout(self.plot_config.layout)
                self.initialized = True

            self.plotter.plot_all()

            graph_encoded = ptydash.interface.fig_to_base64(self.plotter.plot_fig)

        return {
            'topic': 'update',
            'id': self.id,
            'data': {
                'connected': self.plot_client.client.connected,
                'status': status,
                'image': graph_encoded,
            }
        }
