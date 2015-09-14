.. userguide_

**********
User Guide
**********


Introduction
============

MiniCPS is a lightweight simulator for accurate network traffic in an
industrial control system, with basic support for physical layer interaction.

If you need more information about a specific topic see :ref:`add-res`.


Installation
============

Requirements
------------

`Install <http://mininet.org/download/>`_ Mininet and its dependencies.

Notice that Mininet can be installed either inside a Virtual Machine (VM)
or on your physical machine.
The official Mininet VM comes without an X-server that is an *optional*
requirements for MiniCPS (e.g.: it can be used to display a pop-up window
containing an image).

:ref:`install-minicps` section will present instructions to install ``minicps``
on a machine that is running the **latest official mininet vm (Ubuntu)**. Please
refer to your distribution documentation if you need to install mininet and
minicps on other distros.

.. _install-minicps:

Install MiniCPS
---------------

Login the OS containing ``mininet`` installation then navigate to your home
directory:

.. code-block:: console

   cd

Make sure that the distro is up to date (if necessary, restart the system):

.. code-block:: console

   sudo apt-get update; apt-get upgrade

Then clone ``minicps`` repository:

.. code-block:: console

    git clone https://github.com/scy-phy/minicps

MiniCPS is compatible with *python 2.7.X*. Install dependencies using:

.. code-block:: console

   sudo apt-get install python-pip python-matplotlib 
   sudo apt-get install python-networkx python-pil.imagetk
   sudo pip install nose nose-cov

For ENIP support install ``cpppo``

.. code-block:: console

   sudo pip install cpppo

For SDN support optionally install ``pox`` (``mininet`` already includes it):

.. code-block:: console

    cd
    git clone http://github.com/noxrepo/pox

MiniCPS pox controller files are tracked in the ``minicps`` repo itself.
To symlink them to pox's dedicated external controller folder ( ``pox/ext``)
execute the following:

.. code-block:: console

   ~/minicps/bin/init [-p POX_PATH -m MINICPS_PATH -vv]

Notice that: 

* You can increase the verbosity level using either ``v`` or  ``-vv``
* ``POX_PATH`` defaults to ``~/pox`` and ``MINICPS_PATH`` defaults to
  ``~/minicps``, indeed ``~/minicps/bin/init`` should work for you.

Testing installation
----------------------

Now you should be able to run:

.. code-block:: console

    ./bin/swat-tutorial

And see ``mininet>`` CLI.


Configure MiniCPS
==================

General
-----------------

Every switch listens to ``6634`` debugging port.
You can change it via ``OF_MISC`` dict in the ``minicps.constants``

Ssh
---

Mininet VM comes with a ssh server starting at boot. Check it using:

.. code-block:: console

   ps aux | grep ssh

You should see a ``sshd -D`` running process.

If you want to redirect X command to your host X-server ssh into mininet VM
using the ``-Y`` option:

.. code-block:: console

    ssh -Y mininet@minnetvm


Disable ipv6 traffic
-----------------------

In order to reduce the network traffic you can **disable** the
Linux ipv6 kernel module. (``mininet`` VM already disables it)

.. code-block:: console

    sudo vim /etc/default/grub

Search for ``GRUB_CMDLINE_LINUX_DEFAULT`` and **prepend** to the string
``ipv6.disable=1``. You should obtain something like this:

.. code-block:: console

    GRUB_CMDLINE_LINUX_DEFAULT="ipv6.disable=1 ..."

Where ``...`` is other text that you don't have to touch.

Then:

.. code-block:: console

    sudo update-grub

Then reboot your machine and check it with ``ifconfig`` that no
``inet6`` is listed.

Instruction taken from
`here <https://github.com/mininet/mininet/issues/454>`_

Generate sphinx doc
-------------------

First install:

.. code-block:: console

    sudo apt-get install python-sphinx
    sudo pip install sphinx_rtd_theme

Then open ``docs/Makefile`` and check that ``SPHINXBUILD`` reference to
``sphinx-build`` command. (e.g. Arch Linux users can use ``sphinx-build2``)

Then to build the doc in ``html`` format type:

.. code-block:: console

    cd docs
    make html

Then to navigate a static version through a browser (e.g. ``firefox``) type:

.. code-block:: console
    
    firefox _build/html/index.html

.. _logging:

Implementation
===============

Logging
---------

The relevant log files are stored in the ``logs`` dir.

Each minicps module and its associated testing module is managed by a
dedicated ``logging`` object. You can tweak the number of backups file that are
automatically rotating and their size, through the ``minicps.constants`` module.

Each ``scripts/pox/component`` generate a separate ``POXComponent.log`` that 
will be overwritten each time you run a new ``mininet`` configuration.

The swat tutorial produces a ``swat.log`` file. Each time you run a new swat
simulation the logger will append messages to that file. Please control
``swat.log``'s size and manage it manually.  

Nose Testing and Coverage
--------------------------

You can intentionally skip a particular test adding/uncommenting ``raise SkipTest``.
You can see skipped test summary in the nosetests output.

If you want to run all the tests contained in the `topology_tests` module, type:

.. code-block:: console

    sudo nosetests tests/topology_tests

To run a single test within a script use:

.. code-block:: console

    sudo nosetests tests/topology_tests:test_name

Some common and useful ``nosetests`` options:

* ``-s`` opt to prevent nosetests to capture stdout
* ``-v`` opt to obtain a more verbose output
* more on ``nosetests --help``
