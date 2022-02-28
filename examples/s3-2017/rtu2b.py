"""
rtu2b.py
"""

from minicps.devices_old import RTU

from utils import STATE, RTU2B_PROTOCOL
from utils import RTU_PERIOD_SEC
from utils import IP
# rtu2b tags
from utils import wadi2, wadi2_list
from utils import HR_0_2a, HR_1_2a, HR_2_2a

import time
# import sys

RTU2A_ADDR = IP['rtu2a'] + ':502'
RTU2B_ADDR = IP['rtu2b'] + ':502'
SCADA_ADDR = IP['scada'] + ':502'

class RTU2b(RTU):

    def pre_loop(self, sleep=0.6):
        """rtu2b pre loop.

            - sleep
        """

        time.sleep(sleep)

    def main_loop(self):
        """rtu2b main loop.

            - challenge 2
        """
        # print('DEBUG: wadi2: {}'.format(wadi2))
        # print('DEBUG: wadi2_list: {}'.format(wadi2_list))
        # print('DEBUG: len(wadi2_list): {}'.format(len(wadi2_list)))

        count = 0
        offset = 0
        while(True):

            registers = []

            # NOTE: check that result of len is an integer
            if count >= len(wadi2_list) / 3:
                # print("DEBUG: restart count and offset")
                count = 0
                offset = 0

            # NOTE: hop1: 0, 1, 2
            if count <= 2:
                registers.append(wadi2_list[offset ])
                registers.append(wadi2_list[offset +1])
                registers.append(wadi2_list[offset +2])
                # print("DEBUG: hop1 rtu2b send {} count {}".format(registers, count))
                self.send(HR_0_2a, registers, RTU2B_ADDR, count=3)

            # NOTE: hop2: 2, 0, 1
            elif count <= 5:
                registers.append(wadi2_list[offset +2])
                registers.append(wadi2_list[offset ])
                registers.append(wadi2_list[offset +1])
                # print("DEBUG: hop2 rtu2b send {} count {}".format(registers, count))
                self.send(HR_0_2a, registers, RTU2B_ADDR, count=3)

            # NOTE: hop3: 1, 2, 0
            elif count <= 8:
                registers.append(wadi2_list[offset +1])
                registers.append(wadi2_list[offset +2])
                registers.append(wadi2_list[offset ])
                # print("DEBUG: hop3 rtu2b send {} count {}".format(registers, count))
                self.send(HR_0_2a, registers, RTU2B_ADDR, count=3)

            # NOTE: hop4: 2, 1, 0
            elif count <= 11:
                registers.append(wadi2_list[offset +2])
                registers.append(wadi2_list[offset +1])
                registers.append(wadi2_list[offset ])
                # print("DEBUG: hop4 rtu2b send {} count {}".format(registers, count))
                self.send(HR_0_2a, registers, RTU2B_ADDR, count=3)

            else:
                pass
                # print("ERROR")

            count += 1
            offset += 3

            # print("DEBUG: rtu2b main loop")
            time.sleep(RTU_PERIOD_SEC)


if __name__ == "__main__":

    rtu2b = RTU2b(
        name='rtu2b',
        state=STATE,
        protocol=RTU2B_PROTOCOL)
