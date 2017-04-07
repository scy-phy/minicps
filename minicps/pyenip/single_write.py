#!/usr/bin/python2

"""
single_write.py

value is passed as a ``str``
"""

import argparse  # TODO: check if it is too slow at runtime
from pycomm.ab_comm.clx import Driver as ClxDriver

def convert_value_to_type(tag_type, val):
    if tag_type == "INT" or tag_type == "DINT" or tag_type == "SINT":  value = int(val)
    elif tag_type == "REAL": value = float(val)
    elif tag_type == "BOOL": value = bool(val)
    else: value = str(val)
    return value

def write_tag(tag_name, value, tag_type):
    plc = ClxDriver()
    try:
        if plc.open(address):
            temp = plc.write_tag(tag_name, value, tag_type)
            plc.close()
            return temp
        else:
            return "u"
    except Exception as e:
        return "e"

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', type=str, dest='ip', required=True,
                        help='request ip')

    parser.add_argument('-t', '--tag', type=str, dest='tag', required=True,
                        help='request tag with type')

    parser.add_argument('-v', '--val', type=str, dest='val', required=True,
                        help='value to be written')

    args = parser.parse_args()

    # split tags to retrieve type
    tag_name, tag_type = args.tag.split("@")

    # retrieve the ip and ignore the port
    address = args.ip.split(":")[0]

    value = convert_value_to_type(tag_type, args.val)

    res = write_tag(tag_name, value, tag_type)

    if res == "e":
        print("Unable to open connection at : {}".format(address))
    elif res:
        print("Successfully written value: {0} for tag: {1}".format(value, tag_name))
    else:
        print("Write unsuccesful. Please check server log.")



