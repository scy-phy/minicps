.. CONTRIBUTING {{{1
.. _contributing:

*************
Contributing
*************

This doc provides information about how to contribute to the MiniCPS
projects.

.. HOW TO START {{{2

=============
How to start
=============


General design principles
-------------------------

MiniCPS follows an object-oriented design pattern. It is using ``python2.x``
for compatibility reasons with ``mininet``. We are trying to lower the number
of external dependencies, and eventually move to ``python3.x``.

* Design points:

  * separation of concerns (eg: public API vs private APi)
  * modularity (eg: different protocols and state backends)
  * testability (eg: unit tests and TDD)
  * performance (eg: real-time simulation)

* Security points:

  * avoid unsafe programming languages
  * user input is untrusted and has to be validated (eg: prepared statements)
  * safe vs unsafe code separation
  * automated static analysis

* Core components:

  * ``minicps`` module (should be in the ``PYTHONPATH``)
  * ``examples`` use cases (can be anywhere in the filesystem)


Development sytle
-----------------

MiniCPS is hosted on Github and encourages `canonical submission of
contributions
<https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution>`_
it uses
`semantic versioning <http://semver.org/>`_,
``nose`` for  `test-driven development
<https://in.pycon.org/2009/smedia/slides/tdd_with_python.pdf>`_ and
``make`` as a launcher for various tasks.

Required code
---------------

Clone the ``minicps`` repository:

.. code-block:: console

    git clone https://github.com/scy-phy/minicps

Add ``minicps`` to the python path, for example using a soft link:

.. code-block:: console

    ln -s ~/minicps/minicps /usr/lib/python2.7/minicps


Install the requirements using:

.. code-block:: console

    pip install -r ~/minicps/requirements-dev.txt

Run the tests with:

.. code-block:: console

    cd ~/minicps
    make tests

Code conventions
----------------

The project it is based on PEP8 (code) and PEP257 (docstring).

* Naming scheme:

    * Private data: prepend ``_`` eg: ``_method_name`` or ``_attribute_name``
    * Classes: ``ClassName`` or ``CLASSName``, ``method_name`` and ``instance_name``
    * Others: ``function_name``, ``local_variable_name``, ``GLOBAL_VARIABLE_NAME``
    * Filenames: ``foldername``, ``module.py``, ``another_module.py``
      and ``module_tests.py``
    * Test: ``test_ClassName`` ``test_function_name``
    * Makefile: ``target-name`` ``VARIABLE_NAME``
    * Makers: ``TODO``, ``FIXME``, ``XXX``, ``NOTE`` ``VIM MARKER {{{
      ... }}}``
    * Docs: ``doc.rst``, ``another-doc.rst`` \and ``SPHINX_DOC_NAME SOMETHING(`` for
      Sphinx's ``literalinclude``


Module docstring:

.. code-block:: python

   """
   ``modulename`` contains:

      - bla

   First paragraph.

   ...

   Last paragraph.
   """

Function docstrings:

.. code-block:: python

    def my_func():
        """Bla."""

        pass

    def my_func():
        """Bla.

        :returns: wow
        """

        pass

Class docstring to document (at least) public methods:

.. code-block:: python

    class MyClass(object):

        """Bla."""

        def __init__(self):
            """Bla."""

            pass

.. }}}

.. PROTOCOLS {{{2

=========
Protocols
=========

Compatibility with new (industrial) protocols depends on the availability of
a good open-source library implementing that protocol (eg: ``pymodbus`` for
Modbus protocols).

If you want to add a new protocol please look at the ``minicps/protocols.py``
module. ``Protocol`` is the base class, and the
``[NewProtocolName]Protocol(Protocol)`` should be your new child class
(inheriting from the ``Protocol`` class) containing
the code to manage the new protocol. A good point to start it to take a look
at ``tests/protocols_tests.py`` to see how other protocols classes
are unit-tested.

If you want to improve the compatibility of a supported protocol please take
a look at its implementation and unit-testing classes. For example, look at
``ModbusProtocol(Protocol)`` and ``TestModbusProtocol()`` if you want to improve
the Modbus protocol support.

.. }}}

.. STATES {{{2

======
States
======

The same reasoning presented in the Protocols section applies here. The
relevant source code is located in ``minicps/states.py`` and
``tests/states_tests.py``.

.. }}}

.. TESTING {{{2

========
Testing
========

Unit testing is hard to setup properly! Please if you find any inconsistent unit test or
decomposable unit test or you want to add a new one then send a PR.

.. }}}

.. EXAMPLES {{{2

========
Examples
========

Please feel free to send PRs about new use cases that are not already present
in the ``examples`` directory.

.. }}}

.. DOCS {{{2

========
Docs
========

All the docs are stored in the ``docs`` folder. We are using ``sphinx`` to
render the docs and the ``rst`` markup language to write them. Some of the
docs are automatically generated from the code and others are written by
hands.

To build you documentation locally use one of the target of the ``Makefile``
present in the ``docs`` folder. For example, to build and navigate an html
version of our docs type:

.. code-block:: console

   cd docs
   make html
   firefox _build/html/index.html

Please send a PR if you find any typo, incorrect explanation, etc.

.. }}}

.. }}}

