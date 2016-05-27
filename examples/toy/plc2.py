"""
toy plc2.py
"""

from minicps.devices import PLC
from utils import PLC2_DATA, PLC1_ADDR, STATE
from utils import PLC2_PROTOCOL

import time
import sys


SENSOR3_1 = ('SENSOR3', 1)
SENSOR3_2 = ('SENSOR3', 2)


class ToyPLC2(PLC):

    def pre_loop(self, sleep=0.6):
        print 'DEBUG: toy plc2 enters pre_loop'
        print

        # TODO

        # wait for the other plcs
        time.sleep(sleep)

    def main_loop(self, sleep=0.0):
        print 'DEBUG: toy plc2 enters main_loop'
        print

        count = 0
        END = 6e6
        while(True):
            set_s32 = self.set(SENSOR3_2, count)
            print 'DEBUG: toy plc2 set SENSOR3_2: ', set_s32
            self.send(SENSOR3_1, count, PLC1_ADDR)

            time.sleep(1)
            count += 1

            if count > END:
                print 'DEBUG toy plc1 shutdown'
                break


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc2 = ToyPLC2(
        name='plc2',
        state=STATE,
        protocol=PLC2_PROTOCOL,
        memory=PLC2_DATA,
        disk=PLC2_DATA)
