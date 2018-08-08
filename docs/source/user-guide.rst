User Guide
==========

As a user of PtyDash you will need to know how to:


Configuring PtyDash
-------------------

The layout of PtyDash's web interface is controlled by the configuration file ``config.json``.
This file contains two important sections:

app
  Global settings that affect the behaviour of the PtyDash server.
  These are:
    :debug: Run the server in debug mode - provides extra information if errors are encountered
    :port: Port on which to run the server

layout
  The layout of the PtyDash web interface as a list of card definitions.
  Each card type has a set of properties which **must** or **may** be defined.
  You will find a list of the available card types :doc:`here <cards>`.

A example valid PtyDash ``config.json`` is::

  {
    "app": {
      "debug": false,
      "port": 8888
    },
    "layout": [
      {
        "type": "TextCard",
        "id": "text-0",
        "text": "Hello World!"
      }
    ]
  }


Running PtyDash
---------------

Something else
