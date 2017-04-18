#!/usr/bin/python2
"""
synch-client.py

value is passed either as a ``str`` or as a ``bool``. In case of ``str`` the value is
converted to an ``int`` to be written in a holding register
"""

import argparse  # TODO: check if it is too slow at runtime
from pycomm.ab_comm.clx import Driver as ClxDriver

def read_tag(address, tag_name):
    plc = ClxDriver()
    try:
        if plc.open(address):
            tagg = plc.read_tag(tag_name)
            plc.close()
            if not tagg: return (False, )
            return (tagg)
        else:
            return ("u", )
    except Exception as e:
        return ("e",)

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

    if val == "e":
        print("Unable to open connection at : {}".format(address))
    elif val == "u":
        print("Unknown Error! Please check server log.")
    elif val == False:
        print("Read unsuccesful. Please check server log.")
    else:
        print("Success! Value: {0} for Tag: {1}. Type: {2}".format(val, tag_name, res[1]))

