Developer Guide
===============


Installing PtyDash for Development
----------------------------------

If you wish to contribute to PtyDash, you will probably want to install it in 'editable' mode.
To do so:

#. Clone the PtyDash repository - accessible at https://github.com/Southampton-RSG/ptydash
#. From the PtyDash project directory install in editable mode with ``pip``

::

  pip install -e .


PtyDash Architecture
--------------------

The PtyDash interface is defined by subclasses of :class:`ptydash.interface.Card`.
Each block on the interface represents an instance of one of these subclasses,
each of these instances is referred to as a 'card'.

The implementation of these Card subclasses can be found in the :mod:`ptydash.cards` package.


When the PtyDash server is started and a client web browser is connected, the required cards are initialised by the
following process:

#. When the server is started, the list of required cards is read from a configuration file - by default ``config.json``
#. The set of available Card subclasses is collected from the contents of :mod:`ptydash.cards`.
   This allows further card types to be added, simply by dropping the file in the correct directory
#. For each required card, an instance of the correct type is initialised.
   Some card types may attempt to initiate connections to other processes at this point.
#. When the interface is loaded in a web browser, the template for each card is rendered and each card that supports
   dynamic updates will register a periodic callback which pushes an update message to the browser.


Implementing New Cards
----------------------

The implementation of an interface card consists of two parts:

- The card behaviour definition in Python
- The card display definition in HTML + JavaScript


The Behaviour Definition
^^^^^^^^^^^^^^^^^^^^^^^^

The card behaviour is defined by creating a subclass of :class:`ptydash.interface.card` inside the :mod:`ptydash.cards`
package.


The Display Definition
^^^^^^^^^^^^^^^^^^^^^^

How the card is displayed is defined in a template file in ``templates/modules``.
This template is responsible for the presentation of the card, defined in HTML using
`Bootstrap <https://getbootstrap.com/>`_ v4, and for updating the content with the information received via WebSocket.
