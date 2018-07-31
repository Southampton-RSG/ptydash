"""
This module contains Tornado UIModules to display the objects defined in interface.py
"""

import tornado.web


class Image(tornado.web.UIModule):
    def render(self, image):
        return self.render_string('image.html', image=image)

    def javascript_files(self):
        return ['image.js']
