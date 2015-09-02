# MiniCPS #

## Design ##

### Roadmap ###

* Audience: 
    * CPS researchers
    * students
    * professors

* Skillset:
    * programming
    * networking
    * security

* Plugins:
    * MySQL and NoSQL support
    * Modbus/TCP support
    * GUI and ncurses interfaces

* Use cases aka Requirements:
    * simulate a CPS testbed or a production system
    * emulate a CPS testbed or a production system

* Class hierarchy:
    * public
        * Bla
    * private 
        * \_Bla

* Docs:
    * Installations
        * pip
        * Debian
        * Arch
    * Public API
    * SWaT Tutorial

* Future:
    * RESTful interface
    * more graphics


### Public API ###

You provide a CPSNetwork as an input.
Minicps will read information from the CPSNetwork, launch a mininet topology
with the relevant configs (performance, controller, network addresses,
storage, protocol) and optionally store information about your CPSNetwork
e.g. network graph image using `matplotlib`.

A CPSNetwork has Devices, Links, a Process and a State. 
The Process generates PhysicalData.
Devices generates Commands, PhysicalData and Signals (e.g. Alarms, Info, Errors)
Devices can communicate among themselves using Protocols (e.g. ENIP and Modubus/TCP.
Devices and the Process has shared access to the State of the CPSNetwork
Devices can store information about the State of the CPSNetwork

Is a Process:
    WaterTreatment, ElectricGrid

A Link has:
    a bandwitdh, loss rate, delay

A Device has:
    an IP, a MAC, id

Is a Protocol:
    ENIP, Modbus/TCP,
    Signaling.

Is a Device:
    Sensor, Actuator, ControlDevice, Tank

Is a Sensor:
    FlowSensor, LevelSensor, PhSensor, PressureSensor

Is an Actuator:
    Valve, Pump, AlarmButton

Is a ControlDevice:
    PLC, HMI, Historian, Workstation, RIO



### Implementation ###

Minicps will be implemented in pure Python 2.7.x, will be compatible with `pypy`
and it will interface with the user through a CLI.

Mininet framework provides multiple features to start our implementation.

Mininet topologies can be provided in the form of text files and/or python
scripts. The user will have several inputs options like `gexf.xml` graph (`networkx`),
`topology.py` and `topology.txt`.

Mininet is based on Linux containers.
Linux containers allow to assign an arbitrary number of processes to emulate
a Device and the fact that it is connected, e.g. container A will emulate a PLC
and may contain at least one process representing the PLC logic and another
one emulating a PLC ENIP networking module.

Mininet allows performance setting like link shaping: bandwidth, loss rate,
delay and per-host CPU allocation

Mininet runs on a single Linux kernel (lightweight) and is compatible with
Linux tools and protocol suite library (realistic), it supports multi-threaded
and multiprocesses implementation and inter-process communications through
system calls because the scheduler is directly the Linux kernel (low overhead).

Mininet allows SDN controller development, testing and deployment.

The State of the CPS is emulated using shared storage units like files 
or databases backend (sqlite, mysql, nosql).
Devices and PhysicalProcess have shared access to it.
Test various SQL backends: [sqlfiddle](http://sqlfiddle.com/)
Test various NoSQL backend [TODO](aa)

The PhysicalProcess is emulated using any Linux process able to model the
relevant scenario e.g. GNU/Octave, Matlab script.

Due to the extensibility of our framework we envision the possibility to
extend its functionality via plugins (add new industrial protocol supports,
add a ncurses UI or a GUI) and its coverage through additional CPS
network simulations other than SWaT (WADI, etc)

> TODO: dedicated scy-phy accounts to upload the package and manage the docs

Minicps will be distributed using the following formats buildable using  `setup.py`

* cross-platform `pip` 
    * `twine` secure upload to PYPI
* Debian/Ubuntu package
* Arch Linux AUR package

Minicps will be documented using `sphinx` and, once opensourced, the
documentation will be hosted on `readthedocs.com`

Minicps will be tested/profiled using `nose` and `coverage`

### Use cases ###

**SWaT Interactive session example:**

    CPS path:
    minicps> ~/swat
    industrial protocol suite: [E]nip, [m]odbus
    minicps> e
    storing units: [S]qlite, [f]ile, [m]ysql 
    minicps> s
    topology representation: [G]raph, [m]ininet, 
    minicps> g
    graphs: [G]exf, g[m]l, [j]son
    minicps> g
    SDN support: [N]o or [y]es ?
    minicps> y
    SDN platform: [P]ox, [n]ox, [o]pendaylight
    minicps> p
    SDN controller path:
    minicps> ~/swat/pox/controller.py

**Config file example:**

    TODO

