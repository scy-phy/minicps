"""
swat-s1 plc1.py
"""

from minicps.devices import IODevice
from utils import DEV4_DATA, STATE, DEV4_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP
from utils import PUMP_FLOWRATE_IN

import time

PLC1_ADDR = IP['plc1']
DEV4_ADDR = IP['dev4']

P101 = ('P101', 7)
P101_PLC = ('P101', 1)

# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatDev4(IODevice):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s2 dev4 enters pre_loop'
        self.set(P101, 1)
        self.send(P101_PLC, 1, PLC1_ADDR)
        self.send(P101, 1, DEV4_ADDR)
        time.sleep(sleep)

    def main_loop(self):
        """p101 main loop.

            - reads sensors value
            - updates its enip server
        """

        print 'DEBUG: swat-s2 dev4 enters main_loop.'
        print

        count = 0
        while(count <= PLC_SAMPLES):
            # TODO: SIMULATE VIRTUAL PROCESS
            p101_1 = float(self.receive(P101_PLC, PLC1_ADDR))
            self.set(P101, p101_1)
            self.send(P101_PLC, p101_1, PLC1_ADDR)
            self.send(P101, p101_1, DEV4_ADDR)

            time.sleep(PLC_PERIOD_SEC)
            count += 1

        print 'DEBUG swat-s2 dev4 shutdown'


if __name__ == "__main__":

    # notice that memory init is different form disk init
    dev4 = SwatDev4(
        name='dev4',
        state=STATE,
        protocol=DEV4_PROTOCOL,
        memory=DEV4_DATA,
        disk=DEV4_DATA)