#!/usr/bin/env python2

# NOTE: https://pymodbus.readthedocs.io/en/latest/examples/asynchronous-server.html

from pymodbus.server.async import StartTcpServer
from pymodbus.server.async import StartUdpServer
from pymodbus.server.async import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
from pymodbus.server.async import StartTcpServer

import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, dest='ip', help='server ip')
    parser.add_argument('-p', type=int, dest='port', choices=[502],
            default=502, help='port number')
    parser.add_argument('-m', type=int, dest='mode', choices=[1],
            default=1, help='mode')
    args = parser.parse_args()

    # configure the service logging
    # import logging
    # logging.basicConfig()
    # log = logging.getLogger()
    # log.setLevel(logging.DEBUG)

    # NOTE: initialize your data store
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17] * 100),
        co=ModbusSequentialDataBlock(0, [17] * 100),
        hr=ModbusSequentialDataBlock(0, [17] * 100),
        ir=ModbusSequentialDataBlock(0, [17] * 100),
    )

    # NOTE: use 0-based addressing mapped internally to 1-based
    context = ModbusServerContext(slaves=store, single=True, zeromode=False)

    # NOTE: server id information
    identity = ModbusDeviceIdentification()
    identity.VendorName  = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl   = 'http://github.com/bashwork/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName   = 'Pymodbus Server'
    identity.MajorMinorRevision = '1.0'


    # NOTE: currently only implements mode 1
    if mode == 1:
        # NOTE: ip is a str
        # NOTE: port is an int
        StartTcpServer(context, identity=identity, address=(ip, port))
    else:
        pass
    # StartUdpServer(context, identity=identity, address=("localhost", 502))
    # StartSerialServer(context, identity=identity, port='/dev/pts/3',
    #     framer=ModbusRtuFramer)
    # StartSerialServer(context, identity=identity, port='/dev/pts/3',
    #     framer=ModbusAsciiFramer)

