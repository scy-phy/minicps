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

.. }}}


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
for a user or a developer, and it assumes that you *already* have installed
``mininet``.


.. INSTALL MINICPS {{{3

Install MiniCPS
---------------

MiniCPS is can be installed using ``pip``:

.. code-block:: console

   sudo pip install minicps

Test the installation downloading one of our examples from
https://github.com/scy-phy/minicps/tree/master/examples and try to run it.

For example, given that you downloaded the ``examples`` directory,
then you can ``cd swat-s1`` folder and run:

.. code-block:: console

   sudo python run.py

And you should see the following:

.. code-block:: console

   *** Ping: testing ping reachability
   attacker -> plc1 plc2 plc3
   plc1 -> attacker plc2 plc3
   plc2 -> attacker plc1 plc3
   plc3 -> attacker plc1 plc2
   *** Results: 0% dropped (12/12 received)
   mininet>


.. INSTALL OPTIONAL {{{3
.. _install-optional:

Install Optional Packages
-------------------------


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




If you want to contribute to the project please take a look at
:ref:`contributing`.

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

    ssh -Y mininet@mininetvm

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


