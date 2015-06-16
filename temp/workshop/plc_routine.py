#!/usr/bin/python

from PLC import PLC

def main():
    tags = {}
    tags["flow"] = "REAL"
    tags["pump1"] = "INT"
    tags["pump2"] = "INT"
    plc = PLC(tags, "192.168.1.10", 1, 120, "plc1/in_pump.txt", "plc1/out_pump.txt", "plc1/sensor.txt")
    plc.start_server("plc1/server.log")
    plc.run()

if __name__ == '__main__':
    main()
