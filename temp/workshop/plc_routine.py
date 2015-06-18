#!/usr/bin/python

from PLC import PLC
import sys

def main():
    """
    Parses argv and creates an PLC object
    Then run the thread of this PLC object
    """
    ipaddr = sys.argv[1]
    directory = sys.argv[2]
    timer = float(sys.argv[3])
    timeout = float(sys.argv[4])
    file_name = sys.argv[5]
    logfile = sys.argv[6]
    port = int(sys.argv[7])

    tags = {}
    tags[sys.argv[8]] = sys.argv[9]
    tags[sys.argv[10]] = sys.argv[11]
    tags[sys.argv[12]] = sys.argv[13]

    plc = PLC(tags, ipaddr, directory, timer, timeout, file_name)
    plc.start_enip_server(logfile)
    plc.start_http_server(port)
    plc.run()

if __name__ == '__main__':
    main()
