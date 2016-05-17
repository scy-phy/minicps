"""
toy plc2.py
"""

import time

# tags are strings key-val pairs

# TODO: self.get is different from write to PLC memory ?

from minicps.devices import PLC
from examples.toy.utils import PLC2_TAG_DICT, PLC1_ADDR, DB_PATH


class ToyPLC2(PLC):

    def pre_loop(self, sleep=0.4):

        # TODO

        # wait for the other plcs
        time.sleep(sleep)  # TODO: test it

    def main_loop(self, sleep=0.0):

        # TODO
        COUNT = 0
        while(COUNT < 100):

            # TODO

            # Sleep
            time.sleep(sleep)

            COUNT += 1


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc2 = ToyPLC2(
        name='plc2',
        state=DB_PATH,
        protocol='enip',
        memory=PLC2_TAG_DICT,
        disk=PLC2_TAG_DICT)

    plc2.boot(sleep=0.5)

    plc2.mainloop(sleep=0.5)
