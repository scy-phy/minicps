"""
toy plc1.py
"""

import time

# tags are strings key-val pairs

# TODO: self.get is different from write to PLC memory ?

from minicps.devices import PLC
from examples.toy.utils import PLC1_TAG_DICT, PLC2_ADDR, PATH, NAME


# TODO: decide how to map what tuples into memory and disk
class ToyPLC1(PLC):

    def pre_loop(self, sleep=0.4):

        # sensor reading
        sensor1 = self.get(('SENSOR1', 1))

        # update PLC memory
        self.memory['SENSOR1'] = sensor1

        if sensor1 == '1':
            self.memory['SENSOR3'] = '0'

            # ACTUATOR1 ON
            self.memory['ACTUATOR1'] = '1'
            self.set(('ACTUATOR1',), self.memory['ACTUATOR1'])
        else:
            pass

        # wait for the other plcs
        time.sleep(sleep)  # TODO: test it

    def main_loop(self, sleep=0.0):

        pass
        # COUNT = 0
        # while(COUNT < 100):

        #     sensor2 = self.get(('SENSOR2',))
        #     self.memory['SENSOR2'] = sensor2

        #     # do computation with tag values
        #     sensor1_int = int(self.memory['SENSOR1'])
        #     sensor2_int = int(self.memory['SENSOR2'])
        #     result = (sensor1_int + sensor2_int) / 2

        #     if result >= 2:
        #         self.memory['SENSOR2'] = str(result)
        #     elif result == 0:
        #         self.memory['SENSOR2'] = str(result + 1)
        #     else:
        #         pass

        #     # update state of the system
        #     self.memory['ACTUATOR2'] = '0'   # TODO: test it
        #     self.set(('ACTUATOR2',), self.memory['ACTUATOR2'])

        #     # network interaction
        #     # ADDR = IP[:port]

        #     # receive: TODO and TEST
        #     # self.memory['SENSOR4'] = self.receive('SENSOR4', PLC2_ADDR)

        #     # send: TODO and TEST
        #     # self.send('TAG4', PLC2_ADDR)

        #     if self.memory['SENSOR4'] <= 5:
        #         self.memory['ACTUATOR2'] = '1'   # TODO: test it
        #         self.set(('ACTUATOR2',), self.memory['ACTUATOR2'])
        #     else:
        #         pass

        #     # Sleep
        #     time.sleep(sleep)

        #     COUNT += 1


if __name__ == "__main__":

    STATE = {
        'name': NAME,
        'path': PATH
    }
    # notice that memory init is different form disk init
    plc1 = ToyPLC1(
        name='plc1',
        state=STATE,
        protocol='enip',
        memory=PLC1_TAG_DICT,
        disk=PLC1_TAG_DICT)

    plc1.pre_loop(sleep=0.5)

    plc1.main_loop(sleep=0.5)
