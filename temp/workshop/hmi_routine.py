#!/usr/bin/python

from HMI import HMI

def main():
    tags = {}
    tags["flow"] = "REAL"
    tags["pump1"] = "INT"
    tags["pump2"] = "INT"
    hmi = HMI(tags, "192.168.1.10", 1, 120, "hmi/graphs.pdf")
    hmi.run()

if __name__ == '__main__':
    main()
