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
                    try:
                        self.write_message(card.get_message())
                    except ptydash.interface.DoesNotUpdate:
                        pass

            else:
                card = self.application.layout[message['id']]
                try:
                    self.write_message(card.get_message())
                except ptydash.interface.DoesNotUpdate:
                    pass


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

    app.layout = ptydash.interface.Layout.from_config(config)

    return app


if __name__ == "__main__":
    with open('config.json') as f:
        config = json.load(f)

    app = make_app(config)
    app.listen(config['app']['port'])

    print('Starting Tornado server on http://localhost:{0}'.format(config['app']['port']))
    tornado.ioloop.IOLoop.current().start()
