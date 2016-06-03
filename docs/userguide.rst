.. USERGUIDE {{{1
.. _userguide:

**********
User Guide
**********

.. INTRODUCTION {{{2

============
Introduction
============

MiniCPS is a lightweight simulator for accurate network traffic in an
industrial control system, with basic support for physical layer interaction.

This page summarizes the basic installation, configuration and testing of
MiniCPS. We provide a tutorial for beginners here: :ref:`swat-tutorial`. If
you need more information about a specific topic see :ref:`misc`.


.. INSTALLATION {{{2

============
Installation
============

.. REQUIREMENTS {{{3

Requirements
------------

You need to start MiniCPS installation by `installing
<http://mininet.org/download/>`_ Mininet and its dependencies.

Notice that Mininet can be installed either inside a Virtual Machine (VM)
or on your physical machine.
The official Mininet VM comes without an X-server that is an *optional*
requirements for MiniCPS (e.g., it can be used to display a pop-up window
with sensor data visualization).

The `Install MiniCPS`_ section provides instructions to install ``minicps``
on a machine that is running the **latest official mininet VM (Ubuntu)**. Please
refer to your distribution documentation if you need to install Mininet on 
other Linux distributions.


.. INSTALL MINICPS {{{3

Install MiniCPS
---------------

Login the OS containing ``mininet`` installation then navigate to your home
directory:

.. code-block:: console

   cd

Make sure that the distro is up to date (if necessary, restart the system):

.. code-block:: console

   sudo apt-get update
   sudo apt-get upgrade

Then clone ``minicps`` repository:

.. code-block:: console

    git clone https://github.com/scy-phy/minicps

and add ``minicps`` to the python path, for example using a soft link:

.. code-block:: console

    ln -s ~/minicps/minicps /usr/lib/python2.7/minicps

MiniCPS is compatible with *python 2.7.X*. Install dependencies using:

.. code-block:: console

   sudo apt-get install python-matplotlib python-networkx python-pil.imagetk

.. TODO: remove sudo and add pip -U?

For *Ethernet/IP* support install ``cpppo``

.. code-block:: console

   sudo pip install cpppo

.. TODO: add modbus maybe reorganize the deps

For *SDN controller development* there are many options,
``pox`` is a good starting point and Mininet's VM already includes it. If you
want to manually install it type:

.. code-block:: console

    cd
    git clone https://github.com/noxrepo/pox

MiniCPS pox controller files are tracked in the ``minicps`` repo itself.
To symlink them to pox's dedicated external controller folder ( ``pox/ext``)
execute the following:

.. code-block:: console

   ~/minicps/bin/pox-init.py [-p POX_PATH -m MINICPS_PATH -vv]

Notice that: 

* You can increase the verbosity level using either ``v`` or  ``-vv``
* ``POX_PATH`` defaults to ``~/pox`` and ``MINICPS_PATH`` defaults to
  ``~/minicps``, indeed ``~/minicps/bin/init`` should work for you.

.. INSTALL OPTIONAL {{{3
.. _install-optional:

Install optional dependencies
--------------------------------

For *testing* support install dependencies using:

.. code-block:: console

   sudo apt-get install python-pip python-nose python-coverage
   sudo pip install nose-cov

To generate the *documentation* from the source we use the ``sphinx`` tool.
Please type:

.. code-block:: console

    sudo apt-get install python-sphinx libjs-mathjax
    sudo pip install sphinx-rtd-theme



.. TESTING INSTALLATION {{{3

Testing installation
----------------------

Now you should be able to run:

.. code-block:: console

    cd ~/minicps
    make test

.. Which should start the command line with ``mininet>`` prompt. To directly
.. continue with the tutorial, look at :ref:`swat-tutorial`.


.. CONFIGURE MINICPS {{{2

Configure MiniCPS
==================

.. SSH {{{3

ssh
---

Mininet VM comes with a ssh server starting at boot. Check it using:

.. code-block:: console

   ps aux | grep ssh

You should see a ``/usr/sbin/sshd -D`` running process.

If you want to redirect X command to your host X-server ssh into mininet VM,
e.g., to display graphs even if your VM doesn't run an X server,
using the ``-Y`` option:

.. code-block:: console

    ssh -Y mininet@minnetvm


.. IPv6 {{{3

IPv6
----

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


.. OFFILNE DOCUMENTATION {{{3

Offline Documentation
---------------------

First install packages listed in `Install optional dependencies`_.

Then open ``docs/Makefile`` and check that ``SPHINXBUILD`` reference to
``sphinx-build`` command. (e.g., Arch Linux users can use ``sphinx-build2``)

Then to build the doc in ``html`` format type:

.. code-block:: console

    cd docs
    make html

Then to navigate a static version through a browser (e.g., ``firefox``) type:

.. code-block:: console

    firefox _build/html/index.html


.. LOGGING AND TESTING {{{2

.. Logging and Testing
.. ====================
.. TODO
