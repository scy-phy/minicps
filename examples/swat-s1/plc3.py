
"""
swat-s1 plc3
"""

from minicps.devices import PLC
from utils import PLC3_DATA, STATE, PLC3_PROTOCOL
from utils import PLC_SAMPLES, PLC_PERIOD_SEC
from utils import IP

import time

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']
PLC3_ADDR = IP['plc3']

LIT301_3 = ('LIT301', 3)


class SwatPLC3(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-s1 plc3 enters pre_loop'
        print

        time.sleep(sleep)

    def main_loop(self):
        """plc3 main loop.

            - read UF tank level from the sensor
            - update internal enip server
        """

        print 'DEBUG: swat-s1 plc3 enters main_loop.'
        print

        count = 0
        while(count <= PLC_SAMPLES):

            lit301 = float(self.get(LIT301_3))
            print "DEBUG PLC3 - get lit301: %f" % lit301

            self.send(LIT301_3, lit301, PLC3_ADDR)

            time.sleep(PLC_PERIOD_SEC)
            count += 1

        print 'DEBUG swat plc3 shutdown'


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc3 = SwatPLC3(
        name='plc3',
        state=STATE,
        protocol=PLC3_PROTOCOL,
        memory=PLC3_DATA,
        disk=PLC3_DATA)
