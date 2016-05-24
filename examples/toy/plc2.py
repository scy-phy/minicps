"""
toy plc2.py
"""

import time

from minicps.devices import PLC
from examples.toy.utils import PLC2_DATA, PLC1_ADDR, STATE
from examples.toy.utils import PLC2_PROTOCOL


class ToyPLC2(PLC):

    def pre_loop(self, sleep=0.4):

        # TODO

        # wait for the other plcs
        time.sleep(sleep)

    def main_loop(self, sleep=0.0):

        while(True):
            try:
                pass
            except Exception:
                self._protocol._server_subprocess.kill()
        # TODO
        # COUNT = 0
        # while(COUNT < 100):

        #     time.sleep(sleep)
        #     COUNT += 1


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc2 = ToyPLC2(
        name='plc2',
        state=STATE,
        protocol=PLC2_PROTOCOL,
        memory=PLC2_DATA,
        disk=PLC2_DATA)
