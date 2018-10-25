.. PtyDash documentation master file, created by
   sphinx-quickstart on Tue Aug  7 11:15:11 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PtyDash's documentation!
===================================

PtyDash is a web interface intended primarily intended to monitor the progress of image reconstruction when
using the ptychography library `PtyPy <https://ptycho.github.io/ptypy>`_.
It is licensed under GPLv2.

In a more general sense PtyDash provides a framework with which data dashboards may be constructed, from data
visualisation plugins referred to as 'cards'.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   user-guide
   developer-guide
   cards
   apidoc/modules


Installing PtyDash (under development)
======================================

PtyDash is listed in `PyPI <https://pypi.org/>`_ so is able to be installed using ``pip``.

::

  pip install ptydash


**Requirements**:

PtyDash is compatible with Python 2.7 and 3.
It requires a small number of third party Python packages, which will be installed automatically by ``pip``:

:matplotlib:
  Graphing library required for some interface cards to plot graphs

:numpy:
  Numerical library required for some interface cards to process numerical data

:six:
  Compatibility library required to enable compatibility with both versions of Python

:tornado:
  Web framework required to drive the web user interface


**Platforms**:

PtyDash was developed on both Linux and Windows machines and is expected to be compatible with
current versions of Linux, Mac OSX and Windows.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
