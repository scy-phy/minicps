.. _swat-tutorial:

*************
SWaT Tutorial
*************

This tutorial shows how to use MiniCPS to simulate a subprocess of a
Water Treatment testbed. In particular, we demonstate basic controls through simulated PLCs, the network traffic, and simple physical layer simulation. We now provide a brief system overview, list the pre-requisites to run the tutorial, and then provide step-by-step instructions.


System Overview
=================

This tutorial is based on the *Secure Water
Treatment* (or short *SWaT*) which is used by SUTD (Singapore
University of Technology and Design) researcher and students in the
context of Cyber-physical systems security. SWaT subprocess are the
following:

Supply and Storage (P1):
   collect water from the source

Pre-treatment (P2):
   chemically pre-treat raw water

Ultrafiltration and Backwash (P3):
   purify water and periodically clean the backwash filter

De-Chlorination (P4):
   remove excess Chlorine

Reverse Osmosis (P5):
   purify water, discard RO reject water

Permeate Transfer, Cleaning and Back-wash (P6):
   storage of permeate (purified) water


Supply and Storage control
----------------------------

The simulation focuses on the first subprocess of the SWaT testbed.

.. TODO: add Nils pic
.. a image:: images/swat-p1.png

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

* PLC1 read LIT101
* PLC1 compare LIT101 with well defined thresholds
* PLC1 takes a decision (e.g.: open P101 or close MV101)
* PLC1 updates its status

Then PLC1 has to communicate (using *EtherNet/IP*) with PLC2 and PLC3 that
are monitoring subprocess2 and subprocess3.

* PLC1 asks to PLC2 FIT201's value
* PLC1 compare FIT201 with well defined thresholds
* PLC1 takes a decision
* PLC1 updates its status
* PLC1 asks to PLC3 LIT301's value
* PLC1 compare LIT301 with well defined thresholds
* PLC1 takes a decision
* PLC1 updates its status

Notice that *asking to a PLC* is different from *reading from a sensor*,
indeed our simulation separate the two cases using different functions.


.. [#] The real system uses two redundant pumps, one is working and the other
       is in stand-by mode.


Prerequisites
=============

This tutorial assumes that the reader has a basic understanding of Python 2.X
programming language, has familiarly with Linux OS, ``bash``, Mininet
and has a basic understanding of networking tools such
as: ``wireshark``, ``ifconfig`` and ``nmap``.

This tutorial will use the following convections for command syntax:

``command``
   is typed inside a terminal (running ``bash``)

``mininet> command``
   is typed inside mininet CLI

``C-d``
   it means to press and hold ``Ctrl`` and then press ``d``.

It is important that you run the commands from the minicps root folder, you
can monitor your current working directory using:

.. code-block:: console

   pwd

And you should see something like ``../minicps``.



First Steps and Exploration of SWaT
=============


SWaT topology
---------------

To start the simulation, open up a terminal, navigate into your ``minicps``
directory and type:
   
.. code-block:: console

   ./bin/swat-tutorial

Now you should see the ``mininet`` CLI:

.. code-block:: console

   mininet> 

Feel free to explore the network topology using ``mininet``'s built-in
commands such as: ``nodes``, ``dump``, ``net``, ``links`` etc.

At this time you should be able to answer questions such as:

* What is the IP address of PLC1?
* What is the network topology?
* Are there web servers running?

You can exit mininet typing:

.. code-block:: console

   mininet> C-d

You can clean the OS environment typing:

.. code-block:: console

   sudo mn -c


Changing initial values
----------------------

Open ``examples/swat/state_db.py``,
to change LIT101 initial value select one line from the following:

.. literalinclude:: ../examples/swat/state_db.py
   :start-after: ## SET LIT101DB
   :end-before: ## END SET LIT101DB

Open ``examples/swat/constants.py``,
to change process values set:

.. literalinclude:: ../examples/swat/constants.py
   :start-after: ## SET PROCESS
   :end-before: ## END SET PROCESS


Logs and Errors
----------------------

``logs/swat.log`` keeps track of all logged information
appending them to the same file. 

``examples/swat/err`` is a folder that may
contains a ``component.err`` file for each component that during the *last*
simulation has written to ``stderr`` (e.g.: ``hmi.err``).


.. _dumb-plc1:

Dumb plc1
----------

Open ``examples/swat/tutorial.py``,
uncomment the line containing ``..ImageContainer.py...`` :

.. literalinclude:: ../examples/swat/tutorial.py
   :start-after: ## SET POPUP
   :end-before: ## END SET POPUP

Run the simulation again... A window like the one below should pop-up (if you have an X server on your system):

.. TODO: add pop-up win pic
.. a image:: images/swat-pop-up.png

The window contains three subplots: *HMI_MV101-Status*, *HMI_LIT101-Pv*
and *HMI_P101-Status*

HMI_MV101-Status and HMI_P101-Status are using the same encoding:

* ``2.00`` means OPEN/ON
* ``1.00`` means CLOSED/OFF
* ``0.00`` means ERROR

HMI_LIT101-Pv shows a graph of the last fifteen samples of the water level
from the tank in :math:`mm`.

IF you let the time pass you will notice that the flow will increase and the
MV101 and P101 status will remain the same. That is because by default the
tutorial launches a *dumb* PLC1 script. You can check
``examples/swat/plc1a.py`` to gain more insights.

You can stop the simulation typing:

.. code-block:: console

   mininet> C-d

And optionally clean the OS environment typing:

.. code-block:: console

   sudo mn -c

.. _std-plc1:

Standard plc1
-----------------

Open ``examples/swat/tutorial.py`` and comment/uncomment the relevant lines
to call the standard plc1 script:

.. literalinclude:: ../examples/swat/tutorial.py
   :start-after: ## SET PLC1
   :end-before: ## END SET PLC1

Now start the simulation. You should see the same pop-up window like in
:ref:`dumb-plc1` but this time PLC1 will react according to the initial
conditions and the system thresholds.

If you have analyzed the services running on the mininet instance you
will have noticed a web server listening on ``192.160.1.100:80``. Try
to browse that IP within mininet during the simulation.

You can stop the simulation typing:

.. code-block:: console

   mininet> C-d

and optionally clean the OS environment typing:

.. code-block:: console

   sudo mn -c

POXSwat SDN Controller
--------------------------

Open ``examples/swat/tutorial.py``, uncomment:

.. literalinclude:: ../examples/swat/tutorial.py
   :start-after: ## SET SDN CONTROLLER
   :end-before: ## END SET SDN CONTROLLER

If you are familiar with SDN and the ``pox`` platform take a look at
``examples/swat/pox_controller.py``.
