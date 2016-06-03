.. SWAT {{{1
.. _swat-tutorial:

*************
SWaT tutorial
*************

This tutorial shows how to use MiniCPS to simulate a subprocess of a  
Water Treatment testbed. In particular, we demonstrate basic controls through
simulated PLCs, the network traffic, and simple physical layer simulation. We
now provide: 

* A list of the pre-requisites to run the tutorial
* A brief system overview
* Step-by-step instructions to run and modify the simulation


.. PREREQUISITES {{{2

=============
Prerequisites
=============

This tutorial assumes that the reader has a basic understanding of ``python
2.x``,  has familiarly with Linux OS, ``bash``, Mininet
and has a basic understanding of networking tools such
as: ``wireshark``, ``ifconfig`` and ``nmap``.

This tutorial will use the following conventions for command syntax:

``command``
   is typed inside a terminal (running ``bash``)

``mininet> command``
   is typed inside mininet CLI

``C-d``
   it means to press and hold ``Ctrl`` and then press ``d``.

Before continuing please read the :ref:`api` doc.

.. SYSTEM OVERVIEW {{{2

=================
System Overview
=================

This tutorial is based on the *Secure Water
Treatment* (*SWaT*) testbed, which is used by Singapore
University of Technology and Design (SUTD)'s researcher and students in the
context of Cyber-Physical systems security research.

SWaT's subprocess are the followings:

P1: Supply and Storage
   Collect the raw water from the source

P2: Pre-treatment
   Chemically pre-treat the raw water

P3: UltraFiltration (UF) and Backwash
   Purify water and periodically clean the backwash filter

P4: De-Chlorination
   Chemically and/or physically remove excess Chlorine from water

P5: Reverse Osmosis (RO)
   Purify water, discard RO reject water

P6: Permeate transfer, cleaning and back-wash
   Storage of permeate (purified) water


.. SUPPLY AND STORAGE {{{3

Supply and Storage control
----------------------------

The simulation focuses on the first subprocess of the SWaT testbed.

.. TODO: ask Nils new image

.. image:: images/swat-tutorial-subprocess.png

As you can see from the figure, during normal
operating conditions the water flows into a Raw water tank (T101) passing through
an open motorized valve *MV101*. A flow level sensor *FIT101* monitors the
flow rate providing a measure in m^3/h.
The tank has a water level indicator *LIT101* providing a measure in
mm. A pump *P101* [#]_ is able to move the water to the next stage.
In our simulation we assume that the pump is either on or off and that its
flow rate is **constant** and can instantly change value.

The whole subprocess is controlled by three *PLCs (Programmable Logic Controllers)*.
*PLC1* takes the final decisions with the help of *PLC2* and *PLC3*. The
following is a schematic view of subprocess's control strategy:

* PLC1 will first:
   * Read LIT101
   * Compare LIT101 with well defined thresholds
   * Take a decision (e.g.: open P101 or close MV101)
   * Update its status

Then PLC1 has to communicate (using *EtherNet/IP*) with PLC2 and PLC3 that
are monitoring subprocess2 and subprocess3.

* PLC1 will then:
   * Ask to PLC2 FIT201's value
   * Compare FIT201 with well defined thresholds
   * Take a decision
   * Update its status
   * Ask to PLC3 LIT301's value
   * Compare LIT301 with well defined thresholds
   * Take a decision
   * Update its status

Notice that *asking to a PLC* is different from *reading from a sensor*,
indeed our simulation separate the two cases using different functions.


.. [#] The real system uses two redundant pumps, one is working and the other
       is in stand-by mode.


.. SWAT EXPLOTATION {{{2

=====================
MiniCPS simulation
=====================


.. SWAT TOPOLOGY {{{3

Topology
---------------

To start the simulation, open up a terminal, navigate into the root 
``minicps`` directory, (the one containing a ``Makefile``) and type:
   
.. code-block:: console

   make swat-s1

Now you should see the ``mininet`` CLI:

.. code-block:: console

   mininet> 

Feel free to explore the network topology using ``mininet``'s built-in
commands such as: ``nodes``, ``dump``, ``net``, ``links`` etc.

At this time you should be able to answer questions such as:

* What is the IP address of PLC1?
* What are the (virtual) network interfaces?
* What is the network topology?

If you want to open a shell for a specific device, let's say ``plc1`` 
type:

.. code-block:: console

   mininet> xterm plc1


Now you can type any bash command from plc1 node, such that ``ping`` or
``ifconfig``.

At this time you should be able to answer questions such as:

* Are there web servers or ftp servers  running on some host ?
* Is the file system shared ?

Another convenient way to run bash commands is directly from the mininet prompt

.. code-block:: console

   mininet> s1 wireshark

You can exit mininet by pressing ``C-d`` or typing:

.. code-block:: console

   mininet> exit

You can optionally clean the OS environment typing:

.. code-block:: console

   make clean-simulation


.. CHANGING INITIAL VALUES {{{3

Customization
--------------

Open and terminal and ``cd examples/swat-s1/``. This folder can be used as a
template to implement a Cyber-Physical System simulation.

The ``init.py`` script can be run once to generate the sqlite database containing
the state information using two helper class methods.

The ``topo.py`` script contains the mininet ``SwatTopo(Topo)`` subclass used to set the
CPS topology and network parameters (e.g., IP, MAC, netmasks).

The ``run.py`` script contains the ``SwatS1CPS(MiniCPS)`` class that you can
use to customize your simulation. By default the user has to manually run the
PLC logic and physical process simulation script. 
You can start every script automatically uncommenting the following lines:

.. literalinclude:: ../examples/swat-s1/run.py
   :language: python
   :start-after: # SPHINX_SWAT_TUTORIAL RUN(
   :end-before:  # SPHINX_SWAT_TUTORIAL RUN)

In this example it is required to start ``plc2.py`` and ``plc3.py``
**before** ``plc1.py`` because the latter will start requesting Ethernet/IP
tags from the formers to drive the system.

If you want to change the initial values of the simulation open
``physical_process.py`` and look at:

.. literalinclude:: ../examples/swat-s1/physical_process.py
   :language: python
   :start-after: # SPHINX_SWAT_TUTORIAL STATE INIT(
   :end-before:  # SPHINX_SWAT_TUTORIAL STATE INIT)

The ``Device,set`` method requires a ``what`` tuple and a ``value`` that
depends on the sensor or actuator type. The same ``what`` tuple can be used
to address EtherNet/IP tags in the PLCs enip servers. These are the tags
``what`` tuples used for this simulation:

.. literalinclude:: ../examples/swat-s1/physical_process.py
   :language: python
   :start-after: # SPHINX_SWAT_TUTORIAL TAGS(
   :end-before:  # SPHINX_SWAT_TUTORIAL TAGS)

We are using two fields, the first is a ``str`` indicating the name of the
tag and the second is an ``int`` indicating the plc number. For example: 

- plc2 will store an addressable enip tag using  ``FIT201_2 = ('FIT201', 2)``
- plc1 will store in its enip server an addressable enip tag using  ``FIT201_1 = ('FIT201', 1)``

If you want to change any of the plcs logics take a look at ``plc1.py``,
``plc2.py`` and ``plc3.py``. If you want to change the physical process
simulation logic look at ``physical_process.py``. Notice that if you manually
run the logic script you can *plug-and-play* them in any fashion, e.g., you
can test the same plc logics in a scenario where a tank is supposed to
overflow and then stop the physical_process script and run another one where
the tank is supposed to underflow, without stopping the plcs scripts.

The ``log/`` directory is used to store log information about the simulation.


.. TODO: add HMI and ImageContainer and custom SDN controller from old swat


.. POXSwat SDN Controller
.. --------------------------

.. Open ``examples/swat/tutorial/run.py``, uncomment:

.. .. literalinclude:: ../examples/swat/tutorial/run.py
..    :start-after: # SPHINX_SWAT_TUTORIAL SET SDN CONTROLLER
..    :end-before:  # SPHINX_SWAT_TUTORIAL END SET SDN CONTROLLER

.. If you are familiar with SDN and the ``pox`` platform take a look at
.. ``examples/swat/pox_controller.py``.
