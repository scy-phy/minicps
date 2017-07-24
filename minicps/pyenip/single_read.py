#!/usr/bin/python2
import argparse
import sys
from pycomm.ab_comm.clx import Driver as ClxDriver

def read_tag(address, tag_name):
    plc = ClxDriver()
    if plc.open(address):
        tagg = plc.read_tag(tag_name)
        plc.close()
        return (tagg)
    else:
        return "false"


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

    val = "err" if (res is None or res=="false") else res[0]
    sys.stdout.write("%s" % val)
