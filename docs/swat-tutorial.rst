.. swat-tutorial_

*************
SWaT Tutorial
*************

Prerequisites
=============

This tutorial assumes that the reader has a basic understanding of Python 2.X
programming language, has familiarly with Mininet Command Line Interface and APIs and has a basic understanding of networking and network tools such as ``wireshark``, ``ifconfig`` and ``nmap``.

Look at the :doc:`misc` for more information.

python 2.X
-----------------------

For python 2.x start `here <https://docs.python.org/2/tutorial/index.html>`_.

mininet
-----------------------

If you need to get familiar with Mininet take a look at Mininet
`walkthrough <http://mininet.org/walkthrough/>`_ and Mininet
`APIs <https://github.com/mininet/mininet/wiki/Introduction-to-Mininet>`_.

SWaT simulation
===============

System Overview
-----------------

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
``plc1`` reads 

.. [#] The real system uses two redundant pumps, one is working and the other
       is in stand-by mode.


Implementation
----------------

TODO

Explore
=============

Subsection Title
-----------------------

Start the simulation:
   * opening up a terminal
   * navigating into you ``minicps`` directory 
   * and typing:
   
.. code-block:: bash

   # python examples/swat/tutorial.py

A window like the one below should pop up:

.. add pic
.. image:: images/tutorial.png

In your terminal window you should see the following prompt:

.. code-block:: bash

   mininet>
