#!/usr/bin/env python3
from __future__ import absolute_import, division, print_function

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
    def get(self):
        self.render('dashboard.html', layout=self.application.layout)


class DataWebSocket(tornado.websocket.WebSocketHandler):
    """
    Handler for WebSocket passing data to frontend.
    """
    def open(self, *args, **kwargs):
        self.card_callbacks = []

        for card in self.application.layout:
            try:
                self.write_message(card.get_message(self.application.layout))

                if card.update_delay > 0:
                    callback = tornado.ioloop.PeriodicCallback(
                        functools.partial(self.update_card, card),
                        card.update_delay,
                        jitter=0.1
                    )

                    callback.start()
                self.card_callbacks.append(callback)

            except ptydash.interface.DoesNotUpdate:
                pass

    def update_card(self, card):
            self.write_message(card.get_message(self.application.layout))


def make_app(config):
    app = tornado.web.Application(
        [
            (r'/', DashboardHandler),
            (r'/data', DataWebSocket),
        ],
        autoreload=config['app']['autoreload'],
        debug=config['app']['debug'],
        template_path='templates',
        static_path='static',
    )

    # Read UI layout from config
    app.layout = ptydash.interface.Layout.from_config(config)

    return app


if __name__ == "__main__":
    with open('config.json') as f:
        config = json.load(f)

    app = make_app(config)
    app.listen(config['app']['port'])

    print('Starting Tornado server on http://localhost:{0}'.format(config['app']['port']))
    tornado.ioloop.IOLoop.current().start()
