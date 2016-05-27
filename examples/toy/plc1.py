"""
toy plc1.py
"""

from minicps.devices import PLC
from utils import PLC1_DATA, PLC2_ADDR, STATE
from utils import PLC1_PROTOCOL, PLC1_ADDR

import time
import os
import sys


# constant tag addresses
SENSOR1_1 = ('SENSOR1', 1)
SENSOR2_1 = ('SENSOR2', 1)
SENSOR3_1 = ('SENSOR3', 1)
ACTUATOR1_1 = ('ACTUATOR1', 1)
ACTUATOR2_1 = ('ACTUATOR2', 1)

SENSOR3_2 = ('SENSOR3', 2)


# TODO: decide how to map what tuples into memory and disk
class ToyPLC1(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: toy plc1 enters pre_loop'
        print

        # sensor1 = self.set(SENSOR1_1, 2)
        # print 'DEBUG: toy plc1 sensor1: ', self.get(SENSOR1_1)
        # self.memory['SENSOR1'] = sensor1
        self.send(SENSOR3_1, 2, PLC1_ADDR)

        time.sleep(sleep)

    def main_loop(self, sleep=0.5):
        print 'DEBUG: toy plc1 enters main_loop'
        print

        count = 0
        END = 6e6
        while(True):
            rec_s31 = self.recieve(SENSOR3_1, PLC1_ADDR)
            # print 'DEBUG: toy plc1 receive SENSOR3_1: ', rec_s31
            get_s32 = self.get(SENSOR3_2)
            print 'DEBUG: toy plc1 get SENSOR3_2: ', get_s32

            time.sleep(1)
            count += 1

            if count > END:
                print 'DEBUG toy plc1 shutdown'
                break


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc1 = ToyPLC1(
        name='plc1',
        state=STATE,
        protocol=PLC1_PROTOCOL,
        memory=PLC1_DATA,
        disk=PLC1_DATA)
