.. MCPS-MAN {{{1
.. _mcps-man:

****************************************
mcps man page (not included in the docs)
****************************************

TODO

=======================
Section
=======================

The command line utility is called ``mcps``. To get more information on the usage:

.. code-block:: console

   mcps --help

Subsection
----------

The base command generates a scaffold directory which has the minimum files necessary 
to set-up a simulation environment with two ``PLC``'s as the default device.

.. code-block:: console

   mcps init

Custom
-------

The command has additional options.

.. code-block:: console

   mcps init [OPTIONS]

``path``
     Provide a custom path for generating the scaffold.

``config``
     Provide a configuration file to generate template with custom devices and values.

     Note: This is **NOT** implemented yet.

