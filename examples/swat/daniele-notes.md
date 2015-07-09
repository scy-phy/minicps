# Design #

## General view ##

![alt text](block-scheme.png)

* Each SWaT device is simulated in `mininet` as Linux container.
* Tags, sensors value and actuator values are modeled as DB records.
* I'll use `sqlite3` module from Python stdlib.

> TODO: use `multiprocesses`, `threading`, `pykka` or `gevent` ?

> TODO: use ENIP to communicate everywhere ?

## State DB ##

    examples/swat/state_db.py

> TODO: use crypto for records?

> TODO: implement read/write PLC access level?

> TODO: import db directly from real controller plc tags ?

* schema
    * dict table
        * TYPE,SCOPE,NAME,DESCRIPTION,DATATYPE,SPECIFIER,ATTRIBUTES
    * PLC1 can access only suprocess1 records but can retrieve other records
      communicating directly with PLC2

* tag_types
    * user defined -> use Class


## SWaT devices ##

### HMI ###

    examples/swat/hmi_logic.py

| Threads/Procs |
| ------------- |
| HTTP Server   |
| ENIP Client   |
| HMI_DB        |
| HMI_Logic     |

### PLC ###

    examples/swat/plcX_logic.py


| Threads/Procs |
| ------------- |
| ENIP Server   |
| ENIP Client   |
| PLC_DB        |
| PLC_Logic     |

* schema
    * name
    * type
        * TYPE,SCOPE,NAME,DESCRIPTION,DATATYPE,SPECIFIER,ATTRIBUTES
    * ...

* tag_types
    * user defined -> use Class
    * `program` accessible only by PLC_logic thread
    * `controller` accessible by all PLC threads

* logic
    * init the ENIP server db

## Simple example ##

> TODO: once ready move it as a tutorial doc

Simplifying assumptions:
* ignore PLC db
* implement only a subset of state db

Start Minicps with a star topology with two PLCs, HMI, the state db `sdb` and the
physical process `ppr` hosts.
* `sdb` will run `state_db.py`.
* `ppr` will run `physical_process.py`
* `plc1` will run `plc1_logic.py`
* `hmi` will run `hmi_logic.py`
* `physical_process.py` will periodically read/write the state db
* `plc1_logic.py` will periodically read/write the state db
* `hmi_logic.py` will periodically query plc1 enip server thread and show
  results through a webserver interface

## Another example ##

Like Simple example but with:

* `plc1_logic.py` will periodically read/write the state db tags regarding
  subprocess 1
* `plc2_logic.py` will periodically read/write the state db tags regarding
  subprocess 2
* `plc1` enip client thread will ask to plc2 enip server thread for some value
* `plc2` enip server will send the value
* `plc1_logic.py` will communicate with plc1 enip client thread and take a
  decision (write the state db)


