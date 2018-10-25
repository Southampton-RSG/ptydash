Interface Cards
===============

The blocks visible on the PtyDash web interface are known as cards.
Some cards represent static content, while some will update themselves automatically.

While some cards have their own properties which **must** or **may** be defined, all cards have the following common
properties:

``type`` - required
  The type of card being used.
``text`` - optional
  Text to display on the card in addition to its main contents.
``update_delay`` - optional
  Time between card updates in ms.  Default is 1000 ms, 1 s.

It is possible to implement your own card types, but some are provided as a core part of PtyDash.
These types are:


TextCard
--------

TextCards are the simplest card type, representing a static block of text.

There are no additional properties belonging to TextCards.


UpdateCounterCard
-----------------

UpdateCounterCards simply display the number of times they have updated.
They may be useful as a simple timer to be displayed alongside other cards.

There are no additional properties belonging to UpdateCounterCards.


PtyPyClientCard
---------------

PtyPyClientCards connect to a PtyPy server and display the progress of a current image reconstruction.
The server may be running on the same computer as PtyDash, or a remote computer such as your local HPC cluster.o

Additional properties of PtyPyClientCards are:

``address`` - optional
  The address of the PtyPy server to which the card should connect.
  Default is localhost as set by PtyPy.

``port`` - optional
  The port on which the PtyPy server is listening.
  Default is set by PtyPy as the default PtyPy server port.


ImageCard (under development)
-----------------------------

ImageCards subscribe to an MQTT message bus and plot incoming data.

There are no additional properties belonging to ImageCards.


VideoCard
---------

VideoCards display a video by reference to either a file or a stream.

Additional properties of VideoCards are:

``source`` - required
  The URL at which the video file / stream may be accessed.

``mimetype`` - optional
  Media type of the video.  Aids the browser in selecting the correct video plugin.