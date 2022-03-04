"""
swat-s1 plc1.py
"""

from minicps.devices import IODevice
from utils import DEV6_DATA, STATE, DEV6_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP
from utils import PUMP_FLOWRATE_IN

import time

PLC3_ADDR = IP['plc3']
DEV6_ADDR = IP['dev6']

P301 = ('P301', 9)
P301_PLC = ('P301', 3)

# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatDev6(IODevice):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s2 dev4 enters pre_loop'
        self.set(P301, 1)
        self.send(P301_PLC, 1, PLC3_ADDR)
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
            p101_1 = float(self.receive(P301, DEV6_ADDR))
            print 'P301 value: %u'%p101_1
            self.set(P301, p101_1)

            time.sleep(PLC_PERIOD_SEC)
            count += 1

        print 'DEBUG swat-s2 dev4 shutdown'


if __name__ == "__main__":

    # notice that memory init is different form disk init
    dev6 = SwatDev6(
        name='dev6',
        state=STATE,
        protocol=DEV6_PROTOCOL,
        memory=DEV6_DATA,
        disk=DEV6_DATA)