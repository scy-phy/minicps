# Releases and change log

## Version 1.1.0 (2017-TODO-TODO)

### Public API

* Bug fixes

### Industrial protocol support

* Modbus through `pymodbus`

### Examples

* New water distribution simulation see `examples/wadi`

### Test suite

* Added `rednose` for better user interface
* Added `raises` decorator to test for expected Exceptions
* Bug fixes


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
