"""
swat-s1 plc1.py
"""

from minicps.devices import IODevice
from utils import DEV2_DATA, STATE, DEV2_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP
from utils import PUMP_FLOWRATE_IN

import time

PLC1_ADDR = IP['plc1']
DEV2_ADDR = IP['dev2']

MV101_5 = ('MV101', 5)
MV101_1 = ('MV101', 1)

# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatDev2(IODevice):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s2 dev2 enters pre_loop'
        self.set(MV101_5, 1)
        self.send(MV101_1, 1, PLC1_ADDR)
        self.send(MV101_5, 1, DEV2_ADDR)
        time.sleep(sleep)
        time.sleep(10)


    def main_loop(self):
        """mv101 main loop.

            - reads sensors value
            - updates its enip server
        """

        print 'DEBUG: swat-s2 dev2 enters main_loop.'
        print

        count = 0
        while(count <= PLC_SAMPLES):
            # TODO: SIMULATE VIRTUAL PROCESS
            mv101_1 = float(self.receive(MV101_1, PLC1_ADDR))
            self.set(MV101_5, mv101_1)
            self.send(MV101_1, mv101_1, PLC1_ADDR)
            self.send(MV101_5, mv101_1, DEV2_ADDR)

            time.sleep(PLC_PERIOD_SEC)
            count += 1

        print 'DEBUG swat-s2 dev2 shutdown'


if __name__ == "__main__":

    # notice that memory init is different form disk init
    dev2 = SwatDev2(
        name='dev2',
        state=STATE,
        protocol=DEV2_PROTOCOL,
        memory=DEV2_DATA,
        disk=DEV2_DATA)
