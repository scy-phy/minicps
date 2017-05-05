#!/usr/bin/python2

"""
single_write.py

value is passed as a ``str``
"""

import argparse  # TODO: check if it is too slow at runtime
import sys
from pycomm.ab_comm.clx import Driver as ClxDriver

def convert_value_to_proper_type(tag_type, val):
    if tag_type == "INT": value = int(val)
    elif tag_type == "REAL": value = float(val)
    elif tag_type == "BOOL":
        if val == "False" or val == 0: value = False
        else: value = True
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
        raise Exception(e)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', type=str, dest='ip', required=True,
                        help='request ip')

    parser.add_argument('-t', '--tag', type=str, dest='tag', required=True,
                        help='request tag with type. format: NAME[:ID][:ID]...')

    parser.add_argument('-v', '--val', dest='val', required=True,
                        help='value to be written.')

    parser.add_argument('--type', dest='typ', required=True,
                        help='[INT][STRING][REAL]')

    args = parser.parse_args()

    tag_name = args.tag
    tag_type = args.typ
    value = convert_value_to_proper_type(tag_type, args.val)

    # retrieve the ip and ignore the port
    address = args.ip.split(":")[0]

    if tag_type not in ["INT", "STRING", "REAL"]:
        print("single_write.py: error: tag type is invalid.")
        print("usage: single_write.py -h for help")
        raise ValueError("single_write.py: error: tag type is invalid. Only INT, STRING, and FLOAT is supported.")

    res = write_tag(tag_name, value, tag_type)
