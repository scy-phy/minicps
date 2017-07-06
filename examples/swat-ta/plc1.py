"""
swat-ta plc1.py
"""

from minicps.devices import PLC
from utils import PLC1_DATA, STATE, PLC1_PROTOCOL
from utils import PLC_PERIOD_SEC
from utils import IP, LIT_101_M, LIT_301_M, FIT_201_THRESH

import time


class SwatPLC1(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-ta plc1 enters pre_loop'
        print

        time.sleep(sleep)

    def main_loop(self):
        """plc1 main loop.

            - reads sensors value
            - drives actuators according to the control strategy
            - updates its enip server
        """

        print 'DEBUG: swat-ta plc1 enters main_loop.'
        print

        while(True):

            # NOTE: lit101 [meters]
            lit101 = float(self.get(LIT101))
            print 'DEBUG plc1 lit101: %.5f' % lit101
            self.send(LIT101, lit101, IP['plc1'])

            # NOTE: blocking read fit201 and lit301 interlocks
            fit201 = float(self.receive(FIT201_2, IP['plc2']))
            print "DEBUG PLC1 - receive fit201: %f" % fit201
            self.send(FIT201_1, fit201, IP['plc1'])
            lit301 = float(self.receive(LIT301_3, IP['plc3']))
            print "DEBUG PLC1 - receive lit301: %f" % lit301
            self.send(LIT301_1, lit301, IP['plc1'])

            if lit101 <= LIT_101_M['L']:
                # NOTE: close mv101
                self.set(MV101, 1)
                self.memory['MV101'] = 1
            if lit101 >= LIT_101_M['H']:
                # NOTE: close mv101
                self.set(MV101, 0)
                self.memory['MV101'] = 0
            if lit101 <= LIT_101_M['LL']:
                # NOTE: stop p101
                self.set(P101, 0)
                self.memory['P101'] = 0
                # TODO: add alarm to state
                print('ALARM: lit101 below LL: {}'.format(lit101))
            if lit101 >= LIT_101_M['HH']:
                print('ALARM: lit101 above HH: {}'.format(lit101))

            # FIXME: no check about lit301 integrity
            if lit301 <= LIT301_1['L']:
                # NOTE: start p101
                self.set(P101, 1)
                self.memory['P101'] = 1
            if lit301 >= LIT301_1['H'] or fit201 <= FIT_201_THRESH:
                # NOTE: stop p101
                self.set(P101, 0)
                self.memory['P101'] = 0

            # NOTE: update internal enip server
            self.send(MV101, self.memory['MV101'], IP['plc1'])
            self.send(P101, self.memory['P101'], IP['plc1'])

            time.sleep(PLC_PERIOD_SEC)

        print 'DEBUG swat-ta plc1 shutdown'


if __name__ == "__main__":

    plc1 = SwatPLC1(
        name='plc1',
        state=STATE,
        protocol=PLC1_PROTOCOL,
        memory=PLC1_DATA,
        disk=PLC1_DATA)
