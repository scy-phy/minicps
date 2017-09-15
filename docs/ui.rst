.. UI {{{1
.. _ui:

***************
User Interface
***************

.. CLI {{{2

This section documents the CLI for minicps.

=======================
Command Line Interface
=======================

The command line utility is called ``mcps``. To get more information on the usage:

.. code-block:: console

   mcps --help

Default
--------

The base command generates a default scaffold directory which has the minimum files necessary 
to set-up a simulation environment with two ``PLC``'s as the default device.

.. code-block:: console

   mcps init

Custom
-------

The command has additional options.

.. code-block:: console

   mcps init [NAME] [OPTIONS]

``[NAME]``
     Custom name of the directory to be generated.

``path``
     Provide a custom path for generating the scaffold.

``config``
     Provide a configuration file to generate template with custom devices and values.

     Note: This is **NOT** implemented yet.

