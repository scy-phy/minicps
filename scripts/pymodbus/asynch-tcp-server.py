#!/usr/bin/env python2

# NOTE: https://pymodbus.readthedocs.io/en/latest/examples/asynchronous-server.html

# import the various server implementations
from pymodbus.server.async import StartTcpServer

from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from sys import argv

if __name__ == "__main__":

    # configure the service logging
    import logging
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    # initialize your data store
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17] * 100),
        co=ModbusSequentialDataBlock(0, [17] * 100),
        hr=ModbusSequentialDataBlock(0, [17] * 100),
        ir=ModbusSequentialDataBlock(0, [17] * 100))
    context = ModbusServerContext(slaves=store, single=True)

    # run the server you want
    StartTcpServer(context)
