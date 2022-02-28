"""
enip plc2.py
"""

from minicps.devices_old import PLC
from utils import STATE_SWAT, PLC2_PROTOCOL
from utils import PLC_PERIOD_SEC
from utils import IP_SWAT

from subprocess import call
from shlex import split

from random import randint

import time
from utils import flag3


PLC2_ADDR = IP_SWAT['plc2']
PLC3_ADDR = IP_SWAT['plc3']


COUNT = 5


class EnipPLC2(PLC):

    def pre_loop(self, sleep=0.5):
        """plc2 pre loop.

            - add a README:2 string tag to its enip server, where the flag is
              the text value

        """

        # NOTE: challenge 2
        with open('/root/flags/readme2', mode="r") as f:
            readme2 = f.read().strip()
        self.send(('README', 2), readme2, PLC2_ADDR)

        time.sleep(sleep)

    def main_loop(self):
        """plc2 main loop.

            - send a randint to plc3 where flag is the FLAG_3

        """

        count = 0
        while(True):

            # NOTE: challenge 2 extra-calls
            if count <= COUNT:

                with open('/root/flags/readme2', mode="r") as f:
                    readme2 = f.read().strip()

                self.send(('README', 2), readme2, PLC2_ADDR)

                count += 1


            # NOTE: challenge 1
            confuse = randint(0, 40)
            self.send((flag3,), confuse, PLC3_ADDR)



            time.sleep(PLC_PERIOD_SEC)


if __name__ == "__main__":

    plc2 = EnipPLC2(
        name='plc2',
        state=STATE_SWAT,
        protocol=PLC2_PROTOCOL)
