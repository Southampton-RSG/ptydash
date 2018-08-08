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
    :autoreload: Automatically reload the server when the source code is edited
    :debug: Run the server in debug mode - provides extra information if errors are encountered
    :port: Port on which to run the server

layout
  The layout of the PtyDash web interface as a list of card definitions.
  Each card type has a set of properties which **must** or **may** be defined.
  You will find a list of the available card types :doc:`here <cards>`.


Running PtyDash
---------------

Something else
