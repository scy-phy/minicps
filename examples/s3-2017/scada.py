"""
scada.py
"""

from minicps.devices_old import SCADAServer
from utils import SCADA_PROTOCOL, STATE
from utils import SCADA_PERIOD_SEC
from utils import IP
from utils import CO_0_2a, CO_1_2a, CO_2_2a, CO_3_2a
from utils import HR_0_2a

import time

RTU2A_ADDR = IP['rtu2a'] + ':502'
RTU2B_ADDR = IP['rtu2b'] + ':502'
SCADA_ADDR = IP['scada'] + ':502'

class SCADAServer(SCADAServer):

    def pre_loop(self, sleep=0.5):
        """scada pre loop.

            - sleep
        """

        time.sleep(sleep)


    def main_loop(self):
        """scada main loop.

        For each RTU in the network
            - Read the pump status
        """

        while(True):

            #co_00_2a = self.receive(CO_0_2a, RTU2A_ADDR)
            co_00_2a = self.receive(CO_0_2a, SCADA_ADDR)

            # NOTE: used for testing first challenge
            #print('DEBUG scada from rtu2a: CO 0-0 2a: {}'.format(co_00_2a))

            # NOTE: used for testing second challenge
            # NOTE: comment out
            # hr_03_2a = self.receive(HR_0_2a, RTU2B_ADDR, count=3)
            # print('DEBUG scada from rtu2b: HR 0-2 2a: {}'.format(hr_03_2a))


            # print("DEBUG: scada main loop")
            time.sleep(SCADA_PERIOD_SEC)


if __name__ == "__main__":

    scada = SCADAServer(
        name='scada',
        state=STATE,
        protocol=SCADA_PROTOCOL)
