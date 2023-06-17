"""
swat-s1 plc1.py
"""

from minicps.devices import PLC

import time

# TODO: real value tag where to read/write flow sensor
class Plc1(PLC):
    NAME = 'plc1'
    IP = '192.168.1.10'
    MAC = '00:1D:9C:C7:B0:01'
    STATE = {
        'name': 'swat_s1',
        'path': 'swat_s1_db.sqlite'
    }
    TAGS = (
        ('FIT101', 1, 'REAL'),
        ('MV101', 1, 'INT'),
        ('LIT101', 1, 'REAL'),
        ('P101', 1, 'INT'),
        # interlocks does NOT go to the statedb
        ('FIT201', 1, 'REAL'),
        ('MV201', 1, 'INT'),
        ('LIT301', 1, 'REAL'),
    )

    SERVER = {
        'address': IP,
        'tags': TAGS
    }
    PROTOCOL = {
        'name': 'enip',
        'mode': 1,
        'server': SERVER
    }
    DATA = {
        'TODO': 'TODO',
    }

    def __init__(self):
        PLC.__init__(self,
            name=Plc1.NAME,
            state= Plc1.STATE,
            protocol=Plc1.PROTOCOL,
            memory=Plc1.DATA,
            disk=Plc1.DATA)


    def pre_loop(self, sleep=1000):
        print 'DEBUG: swat-s1 plc1 enters pre_loop'
        print

        time.sleep(sleep)

    def main_loop(self):
        print 'DEBUG: swat-s1 plc1 enters main_loop.'
        print

        LIT101 = ('LIT101', 1)
        lit101 = float(self.get(LIT101))
        self.send(LIT101, lit101, Plc1.IP)

        print 'DEBUG swat plc1 shutdown'


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc1 = Plc1()
