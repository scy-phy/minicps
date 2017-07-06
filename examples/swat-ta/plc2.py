"""
swat-ta plc2.py
"""

from minicps.devices import PLC
from utils import PLC2_DATA, STATE, PLC2_PROTOCOL
from utils import PLC_PERIOD_SEC
from utils import IP
from utils import FIT_201_THRESH, LS_201_L
from utils import LS201_2

import time

class SwatPLC2(PLC):

    def pre_loop(self, sleep=0.1):
        print 'DEBUG: swat-ta plc2 enters pre_loop'
        print

        time.sleep(sleep)

    def main_loop(self):
        """plc2 main loop.

            - TODO
        """

        print 'DEBUG: swat-ta plc2 enters main_loop.'
        print

        while(True):

            # NOTE: lit101 [meters]
            ls201 = float(self.get(LS201_2))
            print 'DEBUG plc2 ls201: %.5f' % ls201
            self.send(LS201_2, ls201, IP['plc2'])

            # TODO: read interlocks

            if ls201 <= LS_201_L['L']:
                # NOTE: close p202
                self.set(P201_2, 0)
                self.memory['P201'] = 0
                print('ALARM: ls201 below L: {}'.format(ls201))

            # NOTE: update internal enip server
            self.send(P201_2, self.memory['P201'], IP['plc2'])

            time.sleep(PLC_PERIOD_SEC)

        print 'DEBUG swat-ta plc2 shutdown'


if __name__ == "__main__":

    plc2 = SwatPLC2(
        name='plc2',
        state=STATE,
        protocol=PLC2_PROTOCOL,
        memory=PLC2_DATA,
        disk=PLC2_DATA)
