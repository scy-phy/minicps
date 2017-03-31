#!/usr/bin/python2


"""
synch-client.py

value is passed either as a ``str`` or as a ``bool``. In case of ``str`` the value is
converted to an ``int`` to be written in a holding register
"""

# NOTE: https://pymodbus.readthedocs.io/en/latest/examples/synchronous-client.html

import argparse  # TODO: check if it is too slow at runtime
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
#from pymodbus.client.sync import ModbusUdpClient as ModbusClient
#from pymodbus.client.sync import ModbusSerialClient as ModbusClient

from sys import argv

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, dest='ip', help='request ip')
    parser.add_argument('-p', type=int, dest='port', choices=[502],
            default=502, help='port number')
    parser.add_argument('-u', type=int, dest='unit',
            default=0, help='slave unit number')
    parser.add_argument('-t', type=str, dest='type',
            choices=['DI', 'CO', 'IR', 'HR'],
            help='request type')
    parser.add_argument('-m', type=str, dest='mode',
            choices=['r', 'w'],
            help='mode: read or write')
    parser.add_argument('-o', dest='offset', type=int,
            help='0-based modbus addressing offset',
            choices=range(0,1000),  # NOTE: empirical value
            default=0)
    parser.add_argument('-r', dest='register',
            help='register value', type=int, choices=range(0, 65536),
            default=0)
    parser.add_argument('-c', dest='coil',
            help='coil value', type=bool, default=True)  # NOTE: implicit True False choice

    args = parser.parse_args()

    # import logging
    # logging.basicConfig()
    # log = logging.getLogger()
    # log.setLevel(logging.DEBUG)

    # TODO: check retries, and other options
    client = ModbusClient(args.ip, port=args.port)
            # retries=3, retry_on_empty=True)

    client.connect()

    # TODO: check if asserts are slowing down read/write
    if args.mode == 'w':

        # NOTE: write_register
        if args.type == 'HR':
            hr_write = client.write_register(args.offset, int(args.register))
            assert(hr_write.function_code < 0x80)

        # NOTE: write_coil
        elif args.type == 'CO':
            co_write = client.write_coil(args.offset, args.coil)
            assert(co_write.function_code < 0x80)


    elif args.mode == 'r':

        # NOTE: read_holding_registers
        if args.type == 'HR':
            hr_read = client.read_holding_registers(args.offset, count=1)
            assert(hr_read.function_code < 0x80)
            print(hr_read.registers[0])

        # NOTE: read_holding_registers
        elif args.type == 'IR':
            ir_read = client.read_input_registers(args.offset, count=1)
            assert(ir_read.function_code < 0x80)
            print(ir_read.registers[0])



    client.close()
