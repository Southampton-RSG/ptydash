#!/usr/bin/env python3
from __future__ import absolute_import, division, print_function

import tornado.ioloop
import tornado.web
import tornado.websocket

from ptydash import graphing
from ptydash import interface
from ptydash import uimodules
from ptydash.utils import bytes_to_base64

import mqtt




class DashboardHandler(tornado.web.RequestHandler):
    """
    Handler for main dashboard view.
    """
    def get(self):
        images = [
            interface.Image('img-ws-0'),
            interface.Image('img-ws-1'),
        ]
        self.render('dashboard.html', images=images)


class DataWebSocket(tornado.websocket.WebSocketHandler):
    """
    Handler for WebSocket passing data to frontend.
    """
    def on_message(self, message):
        self.write_message({
            'images': {
                'img-ws-0': bytes_to_base64(graphing.get_graph()),
                'img-ws-1': bytes_to_base64(graphing.get_graph()),
            },
        })


def make_app():
    return tornado.web.Application(
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


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print('Starting Tornado server on http://localhost:8888')
    tornado.ioloop.IOLoop.current().start()
    mqtt()

