# Releases and Changelog

## Version 1.1.2 (2017-05-14)

### Misc

* Remove `example/swat` directory
    * Kept some files in the `misc/` directory

## Version 1.1.1 (2017-05-10)

### Pypi

* [![PyPI version](https://badge.fury.io/py/minicps.svg)](https://badge.fury.io/py/minicps) requires `wheel`

### Modbus

* Fix `write_coil` bug

## Version 1.1.0 (2017-04-01)

### Public API

* Bug fixes

### Industrial protocol support

* Modbus through `pymodbus`

### Test suite

* Added `rednose` for better user interface
* Added `raises` decorator to test for expected Exceptions
* Bug fixes
* Removed `tests/utils_tests.py`


### Misc

* We are an awesome ICS security tool:
[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/hslatman/awesome-industrial-control-system-security)


## Version 1.0.0 (2016-07-01)

### Public API

* Network API core functions: `send` and `receive`
* Physical layer API core functions: `set` and `get`

### Industrial protocol support

* Subset of Ethernet/IP through `cpppo`

### Physical layer backend support

* SQLite3 through `sqlite3`
