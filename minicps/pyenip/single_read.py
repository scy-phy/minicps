#!/usr/bin/python2
"""
synch-client.py

value is passed either as a ``str`` or as a ``bool``. In case of ``str`` the value is
converted to an ``int`` to be written in a holding register
"""

import argparse  # TODO: check if it is too slow at runtime
import sys
from pycomm.clx import Driver as ClxDriver

def read_tag(address, tag_name):
    plc = ClxDriver()
    try:
        if plc.open(address):
            tagg = plc.read_tag(tag_name)
            plc.close()
            return (tagg)
        else:
            return ("u", )
    except Exception as e:
        raise ValueError(e)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', type=str, dest='ip', required=True,
                        help='request ip')

    parser.add_argument('-t', '--tag', type=str, dest='tag', required=True,
                        help='request tag with type')

    args = parser.parse_args()

    # split tags if possible to retrieve name
    tag_name = args.tag.split("@")[0]

    # retrieve the ip and ignore the port
    address = args.ip.split(":")[0]

    res = read_tag(address, tag_name)

    val = res[0]

    if val == "u" or res[1] == 'Check Encapsulation and Message Router Error':
        sys.stdout.write('check server log.')
    else:
        sys.stdout.write("%s" % val)

