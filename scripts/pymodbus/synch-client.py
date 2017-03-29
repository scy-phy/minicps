#!/usr/bin/python2

# NOTE: https://pymodbus.readthedocs.io/en/latest/examples/synchronous-client.html

import argparse  # TODO: check if it is too slow
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

from sys import argv

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', type=str, dest='ip', help='port number')
    parser.add_argument('-p', type=int, dest='port', choices=[502],
            default=502, help='port number')
    parser.add_argument('-u', type=int, dest='unit',
            default=0, help='slave unit number')
    parser.add_argument('-t', type=str, dest='type',
            choices=['DI', 'CO', 'IR', 'HR'],
            help='request type')
    args = parser.parse_args()

    import logging
    logging.basicConfig()
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    IP = argv[1]
    PORT = argv[2]  # modbustcp 502
    UNIT = argv[3]  # slave number 0

    client = ModbusClient(ip, port=port,
            retries=3, retry_on_empty=True)

    client.connect()
