"""
swat-s1 plc1.py
"""

from minicps.devices import PLC
from utils import PLC1_DATA, STATE
from utils import PLC1_PROTOCOL, PLC1_ADDR
from utils import IP

import time
import os
import sys

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']
PLC3_ADDR = IP['plc3']

AI_FIT_101_FLOW = ('NO', 'AI_FIT_101_FLOW', 1)
DO_MV_101_OPEN = ('NO', 'DO_MV_101_OPEN', 1)
AI_LIT_101_LEVEL = ('NO', 'AI_LIT_101_LEVEL', 1)
DO_P_101_START = ('NO', 'DO_P_101_START', 1)
# interlocks to be received from plc2 and plc3
AI_LIT_301_LEVEL = ('NO', 'AI_LIT_301_LEVEL', 3)
AI_FIT_201_FLOW = ('NO', 'AI_FIT_201_FLOW', 2)
DO_MV_201_OPEN = ('NO', 'DO_MV_201_OPEN', 2)


# TODO: real value tag where to read/write flow sensor
class SwatPLC1(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s1 plc1 enters pre_loop'
        print

        time.sleep(sleep)

    def main_loop(self, sleep=0.5):
        print 'DEBUG: swat-s1 plc1 enters main_loop'
        print

        count = 0
        END = 6
        while(True):
            self.set(AI_FIT_101_FLOW, count)
            fit101 = self.get(AI_FIT_101_FLOW)
            print 'DEBUG: swat plc1 get FIT101: ', fit101
            self.send(AI_FIT_101_FLOW, count, PLC1_ADDR)

            time.sleep(1)
            count += 1

            if count > END:
                print 'DEBUG swat plc1 shutdown'
                break


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc1 = SwatPLC1(
        name='plc1',
        state=STATE,
        protocol=PLC1_PROTOCOL,
        memory=PLC1_DATA,
        disk=PLC1_DATA)
