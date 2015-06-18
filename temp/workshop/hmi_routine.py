#!/usr/bin/python

from HMI import HMI
import sys

def main():
    """
    Parses argv and creates an HMI object
    Then run the thread of this HMI object
    """
    ipaddr = sys.argv[1]
    directory = sys.argv[2]
    timer = float(sys.argv[3])
    timeout = float(sys.argv[4])
    file_name = sys.argv[5]
    
    tags = {}
    tags[sys.argv[6]] = sys.argv[7]
    tags[sys.argv[8]] = sys.argv[9]
    tags[sys.argv[10]] = sys.argv[11]

    hmi = HMI(tags, ipaddr, directory, timer, timeout, file_name)
    hmi.run()
    
if __name__ == '__main__':
    main()
