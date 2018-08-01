#!/usr/bin/env python3
from __future__ import absolute_import, division, print_function

import json
import random
import time

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
    def on_message(self, message):
        message = json.loads(message)
        time.sleep(random.random())

        if message['topic'] == 'update':
            if message['id'] == 'all':
                for card in self.application.layout:
                    self.write_message(card.get_message())

            else:
                card = self.application.layout[message['id']]
                self.write_message(card.get_message())


def make_app():
    app = tornado.web.Application(
        [
            (r'/', DashboardHandler),
            (r'/data', DataWebSocket),
        ],
        autoreload=True,
        debug=True,
        template_path='templates',
        static_path='static',
        websocket_max_message_size=1e9,
    )

    app.layout = ptydash.interface.Layout([
        ptydash.interface.Image('img-ws-0'),
        ptydash.interface.Image('img-ws-1'),
    ])

    return app


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print('Starting Tornado server on http://localhost:8888')
    tornado.ioloop.IOLoop.current().start()
