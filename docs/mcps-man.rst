.. MCPS-MAN {{{1
.. _mcps-man:

****************************************
mcps man page (not included in the docs)
****************************************

========
Synopsis
========

``mcps`` [``--help``]
``mcps init`` [``--path`` path] [``--config`` file]

===========
Description
===========

The command line utility is called ``mcps``. It generates a scaffold directory which has
the minimum files necessary to set-up a simulation environment.

====================
Command Line Options
====================

``init``
--------

This generates a default scaffold using two PLCs in the current working directory.

``init [OPTIONS]``
------------------

``--path``
    Provide a custom path for generating the scaffold.

``--config``
    Provide a configuration file to generate template with custom devices and values.

    Note: This is **NOT** implemented yet.

``--help``
----------

This lists the available commands.

