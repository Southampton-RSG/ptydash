#!/usr/bin/env python

"""
This module defines the PtyDash server and is the intended entry point of the application.

PtyDash may be run from source by `python ptydash/server.py`.
"""

from __future__ import absolute_import, division, print_function

import argparse
import functools
import json

import tornado.ioloop
import tornado.web
import tornado.websocket

import ptydash.interface


class DashboardHandler(tornado.web.RequestHandler):
    """
    Handler for main dashboard view.
    """
    def get(self, *args, **kwargs):
        self.render('dashboard.html', layout=self.application.layout)


class DataWebSocket(tornado.websocket.WebSocketHandler):
    """
    Handler for WebSocket passing data to frontend.
    """
    def __init__(self, *args, **kwargs):
        super(DataWebSocket, self).__init__(*args, **kwargs)

        for card in self.application.layout:
            callback = tornado.ioloop.PeriodicCallback(
                functools.partial(self.update_card, card),
                card.update_delay,
                jitter=0.1
            )

            card.callback = callback

    def open(self, *args, **kwargs):
        for card in self.application.layout:
            try:
                self.write_message(card.get_message())
                card.callback.start()

            except ptydash.interface.DoesNotUpdate:
                pass

    def on_close(self):
        for card in self.application.layout:
            card.callback.stop()

    def update_card(self, card):
        """
        Callback function which sends an update message for a given Card.

        :param card: Card for which to send update message
        """
        message = card.get_message()
        if message is not None:
            self.write_message(message)


def main():
    """
    Initialise and run the PtyDash server.
    """
    parser = argparse.ArgumentParser(description='Data dashboard and PtyPy monitor')
    parser.add_argument('config', nargs='?', default='config.json')

    args = parser.parse_args()

    with open(args.config) as config_file:
        print('Reading config from \'{0}\''.format(args.config))
        config = json.load(config_file)

    app = tornado.web.Application(
        [
            (r'/', DashboardHandler),
            (r'/data', DataWebSocket),
        ],
        debug=config['app']['debug'],
        template_path='templates',
        static_path='static',
    )

    # Read UI layout from config
    app.layout = ptydash.interface.Layout.from_config(config)

    print('Starting PtyDash server on http://localhost:{0}'.format(config['app']['port']))
    try:
        app.listen(config['app']['port'])
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print('Shutting down...')


if __name__ == "__main__":
    main()
