"""
enip plc3
"""

from subprocess import call
from shlex import split
from minicps.devices_old import PLC
from utils import STATE_SWAT, PLC3_PROTOCOL
from utils import PLC_PERIOD_SEC
from utils import IP_SWAT

from random import randint
from utils import flag2


import time

PLC2_ADDR = IP_SWAT['plc2']
PLC3_ADDR = IP_SWAT['plc3']


COUNT = 5

class EnipPLC3(PLC):

    def pre_loop(self, sleep=0.5):
        """plc3 pre loop.

            - add a README:3 string tag to its enip server, where the flag is
              the text value

        """


        # NOTE: challenge 2, call it once (linked to plc2.py)
        with open('/root/flags/readme3', mode="r") as f:
            readme3 = f.read().strip()

        self.send(('README', 3), readme3, PLC3_ADDR)

        time.sleep(sleep)

    def main_loop(self):
        """plc3 main loop.

            - send a randint to plc2 where flag is the FLAG_2
        """

        count = 0
        while(True):

            # NOTE: challenge 2 extra-calls
            if count <= COUNT:

                with open('/root/flags/readme3', mode="r") as f:
                    readme3 = f.read().strip()

                self.send(('README', 3), readme3, PLC3_ADDR)

                count += 1

            # NOTE: challenge 1
            confuse = randint(0, 40)
            self.send((flag2,), confuse, PLC2_ADDR)



            time.sleep(PLC_PERIOD_SEC)


if __name__ == "__main__":

    plc3 = EnipPLC3(
        name='plc3',
        state=STATE_SWAT,
        protocol=PLC3_PROTOCOL)
