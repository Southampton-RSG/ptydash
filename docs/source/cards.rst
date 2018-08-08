Interface Cards
===============

The blocks visible on the PtyDash web interface are known as cards.
Some cards represent static content, while some will update themselves automatically.


Card Types
----------

All cards have the following properties:

``type`` - required
  The type of card being used
``text`` - optional
  Text to display on the card in addition to its main contents
``update_delay`` - optional
  Time between card updates in ms.  Default is 1000 ms, 1 s.

It is possible to implement your own card types, but some are provided as a core part of PtyDash.
These types are:


TextCard
^^^^^^^^

TextCards are the simplest card type, representing a static block of text.

There are no additional properties belonging to TextCards.


UpdateCounterCard
^^^^^^^^^^^^^^^^^

UpdateCounterCards simply display the number of times they have updated.
They may be useful as a simple timer to be displayed alongside other cards.

There are no additional properties belonging to UpdateCounterCards.


PtyPyClientCard
^^^^^^^^^^^^^^^

PtyPyClientCards connect to a PtyPy server and display the progress of a current image reconstruction.
The server may be running on the same computer as PtyDash, or a remote computer such as your local HPC cluster.o

Additional properties of PtyPyClientCards are:

``address``
