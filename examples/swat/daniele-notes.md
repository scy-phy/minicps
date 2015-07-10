# Design #

## General view ##

![alt text](block-scheme.png)

* Each device is simulated in `mininet` as Linux container.
* Tags, sensors value and actuator values are modeled as DB records.
* Use `sqlite3` module from Python stdlib.

> TODO: use multiprocess or multi-threading from one process inside a
> container?

> TODO: use `multiprocesses`, `threading`, `pykka` or `gevent` ?

## State DB ##

    examples/swat/state_db.py

* schema
    * Tag table
        * text not null: SCOPE, NAME, DATATYPE
        * text: VALUE
        * integer: PID
        * PRIMARY KEY(SCOPE, NAME, PID)
    * PLC1 can access only subprocess1 records but can retrieve other records
      communicating directly with PLC2
    * filter in: INT, DINT, BOOL, REAL

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
    * Tag
        * like state_db + timestamp
    * Use it like a cache
    * Re-use it for the Historian

* tag types:
    * user defined -> use Class
    * `program` accessible only by PLC_logic thread
    * `controller` accessible by all PLC threads

* tag attributes:
    * `Constant` writable only by RSLogix 5000 (default `True`)
    * `ExternalAccess` set permission for devices external to PLC (default `Read/Write`)
    * `RADIX` TODO

* logic
    * init the ENIP server db

## Simple example ##

> TODO: once ready move it as a sphinx tutorial doc

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

## Future ##



* Crypto DB
* Implement read/write PLC access
* Model User Defined Tags as dedicated classes and import them into the DB
* Use Hystorian node 

