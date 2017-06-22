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
of external dependencies, and eventually will move to ``python3.x``.

* design drivers:

  * separation of concerns (eg: public API vs private APi)
  * modularity (eg: different protocols and state backends)
  * testability (eg: unit tests and TDD)
  * performance (eg: real-time simulation)

* security drivers:

  * avoid unsafe programming languages
  * user input is untrusted and has to be validated (eg: prepared statements)
  * safe vs unsafe code separation
  * automated static analysis

* core components:

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

    pip install -r ~/minicps/requirements.txt

Run the tests with:

.. code-block:: console

    cd ~/minicps
    make tests

Code conventions
----------------

The project it is based on PEP8 (code) and PEP257 (docstring).

* naming scheme:

    * private: prepend ``_`` eg: ``_method_name`` or ``_attribute_name``
    * classes: ``ClassName`` or ``CLASSName``, ``method_name`` and ``instance_name``
    * others: ``function_name``, ``local_variable_name``, ``GLOBAL_VARIABLE_NAME``
    * filenames: ``foldername``, ``module.py``, ``another_module.py``
      and ``module_tests.py``
    * test: ``test_ClassName`` ``test_function_name``
    * make: ``target-name`` ``VARIABLE_NAME``
    * makers: ``TODO``, ``FIXME``, ``XXX``, ``NOTE``
    * doc: ``doc.rst``, ``another-doc.rst`` \and ``SPHINX_DOC_NAME SOMETHING(`` for
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
``NewProtocolNameProtocol(Protocol)`` should be your new child class containing
the code to manage it. A good point to start it to take a look
at ``minicps/tests/protocols_tests.py`` to see how other protocols classes
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

The same reasoning presented in the Protocols section applies here.

.. }}}

.. EXAMPLES {{{2

========
Examples
========

Please feel free to send PRs about new use cases that are not already present
in the ``examples`` directory.

.. }}}

.. }}}

