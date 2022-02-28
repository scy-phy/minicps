"""
rtu2a.py
"""

from minicps.devices_old import RTU

from utils import STATE, RTU2A_PROTOCOL
from utils import RTU_PERIOD_SEC
from utils import IP

# rtu2a tags
from utils import CO_0_2a, CO_1_2a, CO_2_2a, CO_3_2a
from utils import HR_0_2a, HR_1_2a, HR_2_2a
from utils import wadi1, wadi1_bin

import time

RTU2A_ADDR = IP['rtu2a'] + ':502'
RTU2B_ADDR = IP['rtu2b'] + ':502'
SCADA_ADDR = IP['scada'] + ':502'

class RTU2a(RTU):

    def pre_loop(self, sleep=0.6):
        """rtu2a pre loop.

            - sleep
        """

        time.sleep(sleep)

    def main_loop(self):
        """rtu2a main loop.

            - challenge 1
        """
        # print('DEBUG: wadi1: {}'.format(wadi1))
        # print('DEBUG: wadi1_bin: {}'.format(wadi1_bin))

        assert (len(wadi1_bin) / 8) == len(wadi1)
        # print('DEBUG: len(wadi1): {}'.format(len(wadi1)))
        # print('DEBUG: len(wadi1_bin): {}'.format(len(wadi1_bin)))
        # print('DEBUG: len(wadi1_bin)/8: {}'.format(len(wadi1_bin) / 8))

        count = 0
        while(True):

            if count >= len(wadi1_bin):
                count = 0

            if wadi1_bin[count] == '1':
                #self.send(CO_0_2a, True, RTU2A_ADDR)
                self.send(CO_0_2a, True, SCADA_ADDR)
                # print("DEBUG: rtu2a send {} count {}".format(True, count))
            else:
                #self.send(CO_0_2a, False, RTU2A_ADDR)
                self.send(CO_0_2a, False, SCADA_ADDR)
                # print("DEBUG: rtu2a send {} count {}".format(False, count))

            count += 1

            # NOTE: read sensors
            # co_0_2a = True if self.get(CO_0_2a) == '1' else False

            # print("DEBUG: rtu2a co_0_2a: {}".format(co_0_2a))
            # print("DEBUG: self.receive co_0_2a: \
            #         {}".format(self.receive(CO_0_2a, RTU2A_ADDR)))


            # print("DEBUG: rtu2a main loop")
            time.sleep(RTU_PERIOD_SEC)


if __name__ == "__main__":

    rtu2a = RTU2a(
        name='rtu2a',
        state=STATE,
        protocol=RTU2A_PROTOCOL)
