"""
swat-s1 plc1.py
"""

from minicps.devices import PLC
from utils import PLC1_DATA, STATE, PLC1_PROTOCOL
from utils import PLC_PERIOD_SEC, PLC_SAMPLES
from utils import IP, LIT_101_M, LIT_301_M, FIT_201_THRESH
from Logger import hlog

import time

PLC1_ADDR = IP['plc1']
PLC2_ADDR = IP['plc2']
PLC3_ADDR = IP['plc3']

FIT101 = ('FIT101', 1)
MV101 = ('MV101', 1)
LIT101 = ('LIT101', 1)
P101 = ('P101', 1)
# interlocks to be received from plc2 and plc3
LIT301_1 = ('LIT301', 1)  # to be sent
LIT301_3 = ('LIT301', 3)  # to be received
FIT201_1 = ('FIT201', 1)
FIT201_2 = ('FIT201', 2)
MV201_1 = ('MV201', 1)
MV201_2 = ('MV201', 2)
# SPHINX_SWAT_TUTORIAL PLC1 LOGIC)

# TODO: real value tag where to read/write flow sensor
class SwatPLC1(PLC):
    NAME = 'plc1'
    IP = ' 10.0.2.110'
    MAC = '00:1D:9C:C7:B0:10'

    def pre_loop(self, sleep=0.1):
        hlog ('DEBUG: swat-s1 plc1 enters pre_loop')
        print

        time.sleep(sleep)

    def main_loop(self):
        """plc1 main loop.

            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """

        hlog ('DEBUG: swat-s1 plc1 enters main_loop.')
        print

        count = 0
        while(count <= PLC_SAMPLES):

            # lit101 [meters]
            lit101 = float(self.get(LIT101))
            hlog ('DEBUG plc1 lit101: %.5f' % lit101)
            self.send(LIT101, lit101, PLC1_ADDR)

            if lit101 >= LIT_101_M['HH']:
                hlog ("WARNING PLC1 - lit101 over HH: %.2f >= %.2f." % (
                    lit101, LIT_101_M['HH']))

            if lit101 >= LIT_101_M['H']:
                # CLOSE mv101
                hlog ("INFO PLC1 - lit101 over H -> close mv101.")
                self.set(MV101, 0)
                self.send(MV101, 0, PLC1_ADDR)

            elif lit101 <= LIT_101_M['LL']:
                hlog ("WARNING PLC1 - lit101 under LL: %.2f <= %.2f." % (
                    lit101, LIT_101_M['LL']))

                # CLOSE p101
                hlog ("INFO PLC1 - close p101.")
                self.set(P101, 0)
                self.send(P101, 0, PLC1_ADDR)

            elif lit101 <= LIT_101_M['L']:
                # OPEN mv101
                hlog ("INFO PLC1 - lit101 under L -> open mv101.")
                self.set(MV101, 1)
                self.send(MV101, 1, PLC1_ADDR)

            # TODO: use it when implement raw water tank
            # read from PLC2 (constant value)
            fit201 = float(self.receive(FIT201_2, PLC2_ADDR))
            hlog ("DEBUG PLC1 - receive fit201: %f" % fit201)
            self.send(FIT201_1, fit201, PLC1_ADDR)

            time.sleep(PLC_PERIOD_SEC)
            count += 1

        hlog ('DEBUG swat plc1 shutdown')


if __name__ == "__main__":

    hlog('DEBUG swat plc1 start')
    # notice that memory init is different form disk init
    plc1 = SwatPLC1(
        name='plc1',
        state=STATE,
        protocol=PLC1_PROTOCOL,
        memory=PLC1_DATA,
        disk=PLC1_DATA)
