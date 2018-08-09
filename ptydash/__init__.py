"""
PtyDash is a web interface intended primarily intended to monitor the progress of image
reconstruction when using the ptychography library PtyPy.

It is licensed under GPLv2.

In a more general sense PtyDash provides a framework with which data dashboards may be constructed,
from data visualisation plugins referred to as 'cards'.
"""

import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))

del os
