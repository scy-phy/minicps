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

    # NOTE: network
    parser.add_argument('-i', type=str, dest='ip', help='server ip')
    # NOTE: allows non standard port to test without sudo
    parser.add_argument('-p', type=int, dest='port',
            default=502, help='port number')
    parser.add_argument('-m', type=int, dest='mode', choices=[1],
            default=1, help='mode')
    # NOTE: tags
    parser.add_argument('-d', type=int, dest='discrete_inputs',
            choices=range(1, 1000),
            default=10,
            help='number of discrete inputs')
    parser.add_argument('-c', type=int, dest='coils',
            choices=range(1, 1000),
            default=10,
            help='number of coils')
    parser.add_argument('-r', type=int, dest='input_registers',
            choices=range(1, 1000),
            default=10,
            help='number of input registers')
    parser.add_argument('-R', type=int, dest='holding_registers',
            choices=range(1, 1000),
            default=10,
            help='number of holding registers')

    args = parser.parse_args()

    # configure the service logging
    # import logging
    # logging.basicConfig()
    # log = logging.getLogger()
    # log.setLevel(logging.DEBUG)

    # NOTE: initialize everthing to 0
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0] * args.discrete_inputs),
        co=ModbusSequentialDataBlock(0, [0] * args.coils),
        ir=ModbusSequentialDataBlock(0, [0] * args.input_registers),
        hr=ModbusSequentialDataBlock(0, [0] * args.holding_registers),
        zero_mode=False,
    )

    # NOTE: use 0-based addressing mapped internally to 1-based
    context = ModbusServerContext(slaves=store, single=True)

    # TODO: server id information
    identity = ModbusDeviceIdentification()
    identity.VendorName  = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl   = 'http://github.com/bashwork/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName   = 'Pymodbus Server'
    identity.MajorMinorRevision = '1.0'


    # NOTE: currently only implements mode 1
    if args.mode == 1:
        # NOTE: ip is a str, port is an int
        StartTcpServer(context, identity=identity,
            address=(args.ip, args.port))

    else:
        pass
    # StartUdpServer(context, identity=identity, address=("localhost", 502))
    # StartSerialServer(context, identity=identity, port='/dev/pts/3',
    #     framer=ModbusRtuFramer)
    # StartSerialServer(context, identity=identity, port='/dev/pts/3',
    #     framer=ModbusAsciiFramer)

