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
    # NOTE: allows non standard port to test without sudo
    parser.add_argument('-p', type=int, dest='port',
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
            choices=range(0,2000),  # NOTE: empirical value
            default=0)
    parser.add_argument('--count', dest='count',
            help='count for multiple read and write',
            type=int, choices=range(1,2000),  # NOTE: bounds from the standard
            default=1)
    parser.add_argument('-r', dest='register',
            help='list of int values', type=int,
            choices=range(0, 65536), nargs='+',
            default=0)
    parser.add_argument('-c', dest='coil',
            help='list of 0 (False) or 1 (True) int values', type=int, nargs='+',
            default=0, choices=[0, 1])  #  argparse does not manage bool well

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
            if args.count == 1:
                hr_write = client.write_register(args.offset, args.register[0])
                assert(hr_write.function_code < 0x80)
            else:
                hrs_write = client.write_registers(args.offset, args.register)
                assert(hrs_write.function_code < 0x80)

        # NOTE: write_coil: map integers to bools
        elif args.type == 'CO':

            if args.count == 1:
                # NOTE: coil is a list with one bool
                if args.coil[0] == 1:
                    co_write = client.write_coil(args.offset, True)
                else:
                    co_write = client.write_coil(args.offset, False)
                assert(co_write.function_code < 0x80)

            else:
                coils = []
                for c in args.coil:
                    if c == 1:
                        coils.append(True)
                    else:
                        coils.append(False)
                cos_write = client.write_coils(args.offset, coils)
                assert(cos_write.function_code < 0x80)


    elif args.mode == 'r':

        # NOTE: read_holding_registers
        if args.type == 'HR':
            hr_read = client.read_holding_registers(args.offset,
                count=args.count)
            assert(hr_read.function_code < 0x80)
            print(hr_read.registers[0:args.count])

        # NOTE: read_holding_registers
        elif args.type == 'IR':
            ir_read = client.read_input_registers(args.offset,
                count=args.count)
            assert(ir_read.function_code < 0x80)
            print(ir_read.registers[0:args.count])

        # NOTE: read_discrete_inputs
        elif args.type == 'DI':
            di_read = client.read_discrete_inputs(args.offset,
                count=args.count)
            assert(di_read.function_code < 0x80)
            print(di_read.bits)

        # NOTE: read_discrete_inputs
        elif args.type == 'CO':
            co_read = client.read_coils(args.offset,
                count=args.count)
            assert(co_read.function_code < 0x80)
            print(co_read.bits)



    client.close()
