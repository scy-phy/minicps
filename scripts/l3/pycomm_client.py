#!/usr/bin/python2

"""
Read/Write atomic(single) tag and User Defined Tag
(array of atomic and/or UDT) from/to
a ControlLogix PLC.

Adapted from examples/test_ab_comm.py,
more on https://github.com/ruscito/pycomm
"""

# TODO: use minicps constants instead of hadcoded ip
# and log file
# Pycomm doesn't interface with the cpppo server.

import logging

from pycomm.ab_comm.clx import Driver as ClxDriver

# from minicps import constants as c


# log_filename = "%s/pycomm-client.log" % c.LOG_DIR
log_filename = "%s/pycomm-client.log" % '././temp/l3'
logging.basicConfig(
    filename=log_filename,
    # level=logging.WARNING,
    level=logging.DEBUG,  # more verbosity
    format="%(levelname)-10s %(asctime)s %(message)s"
)


def enip_write(plc_ip, tag_name, value, tag_type):
    """Write a plc tag and print the resutl

    :value: TODO
    :tag_type: TODO
    """

    plc = ClxDriver()
    if plc.open(plc_ip):
        print(plc.write_tag(tag_name, value, tag_type))
        plc.close()
    else:
        print("Unable to open", plc_ip)


def enip_read(plc_ip, tag_name):
    """Read a plc tag and print the rx data

    """

    plc = ClxDriver()
    if plc.open(plc_ip):
        print(plc.read_tag(tag_name))
        plc.close()
    else:
        print("Unable to open", plc_ip)


def main():
    # ip = c.L1_PLCS_IP('plc1')
    ip = '192.168.1.10'
    tag_name = 'pump3'
    for i in range(0, 10):
        enip_write(ip, tag_name, i, 'INT')
        enip_read(ip, tag_name)


if __name__ == '__main__':
    main()
