#!/usr/bin/env python3
from __future__ import absolute_import, division, print_function

import json
# import random
# import time

import tornado.ioloop
import tornado.web
import tornado.websocket

from ptydash import interface
from ptydash import uimodules


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
        # time.sleep(random.random())

        if message['topic'] == 'update':
            id = message['id']

            if id == 'all':
                for card in self.application.layout:
                    self.write_message({
                        'topic': 'update',
                        'id': card.id,
                        'data': card.card_message()
                    })

            else:
                self.write_message({
                    'topic': 'update',
                    'id': id,
                    'data': self.application.layout[id].card_message()
                })


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
        ui_modules=uimodules
    )

    app.layout = interface.Layout([
        interface.Image('img-ws-0'),
        interface.Image('img-ws-1'),
    ])

    return app


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print('Starting Tornado server on http://localhost:8888')
    tornado.ioloop.IOLoop.current().start()
