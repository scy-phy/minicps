.. _swat-tutorial:

*************
SWaT Tutorial
*************

Prerequisites
=============

This tutorial assumes that the reader has a basic understanding of Python 2.X
programming language, has familiarly with ``bash``, Mininet Command Line Interface and
its APIs and has a basic understanding of networking and network tools such
as: ``wireshark``, ``ifconfig`` and ``nmap``.

This tutorial will use the following convetions for command syntax:

``command``
   is typed inside a terminal (running ``bash``)

``mininet> command``
   is typed inside mininet CLI

``<C-d>``
   it means to press and hold ``Ctrl`` and then press ``d``.

It is important that you run the commands from the minicps root folder, you
can monitor your current working directory using:

.. code-block:: console

   pwd

and you shuold see something like ``../minicps``.



System Overview
=================

This tutorial shows how to use MiniCPS to simulate a part of a real water
Treatment testbed. The testbed is called *SWaT* that stands for *Secure Water
Treatment* and it is used by SUTD (Singapore University of Technology and
Design) researcher as students in the context of Cyber-physical systems
security.

Process and Control Strategy
----------------------------

.. image:: images/tutorial.png

The simulation focuses on the first subprocess of the SWaT testbed. In normal
operating conditions the water flows into a Raw water tank (T101) passing through a
flow level sensors (FIT101) and an open motorized valve (MV101). T101 has a
water level indicator (LIT101) able to measure the quantity of water inside
the tank. A pump (P101) [#]_ is able to move the water to the next stage.

The whole subprocess is controlled by a set of *PLCs (Programmable Logic Controllers)*
.. TODO: add more explanation from swat/workshop files

.. [#] The real system uses two redundant pumps, one is working and the other
       is in stand-by mode.


Explore
=============

SWaT topology
---------------

To start the simulation, open up a terminal, navigate into your ``minicps``
directory and type:
   
.. code-block:: console

   ./bin/swat-tutorial

Now you shuld see the ``mininet`` CLI:

.. code-block:: console

   mininet> 

Feel free to explore the network topology using ``mininet``'s built-in
commands such as: ``nodes``, ``dump``, ``net``, ``links`` etc.

At this time you shuold be able to answer questions such as:

* What is the IP address of PLC1?
* What is the network topology?
* Are there webservers running?

You can exit mininet typing:

.. code-block:: console

   <C-d>

You can clean the OS environment typing:

.. code-block:: console

   sudo mn -c


Dumb plc1
----------

The image presents three subplots, the one at the bottom

Now try to change the to speed up the overflow process.

Standard plc1
-----------------

blablabla

Comment/uncomment secionts shuold start with ``##``

Play by yourself
------------------

blablabla

APIs
======

.. add autodoc generated 
