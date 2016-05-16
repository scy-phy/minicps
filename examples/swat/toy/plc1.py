"""
plc1.py
"""

import time

# tags are strings key-val pairs

# TODO: self.get is different from write to PLC memory ?

from minicps.devices import PLC

PLC1_TAG_DICT = {
    'SENSOR1' '0',
    'SENSOR2' '0.0',
    'SENSOR3' '0',  # interlock with PLC2
    'ACTUATOR1' '1',  # 0 means OFF and 1 means ON
    'ACTUATOR2' '0',
}

PLC2_ADDR = '10.0.0.2'
DB_PATH = 'examples/swat/toy/db.sqlite'


class ToyPLC1(PLC):

    def pre_loop(self, sleep=0.4):

        # sensor reading
        sensor1 = self.get('SENSOR1')  # TODO: test it

        # update PLC memory
        self.memory['SENSOR1'] = sensor1

        if sensor1 == '1':
            self.memory['TAG3'] = '0'

            # ACTUATOR1 ON
            self.memory['ACTUATOR1'] = '1'  # TODO: test it
            self.set('ACTUATOR1', self.memory['ACTUATOR1'])  # TODO: test it
        else:
            pass

        # wait for the other plcs
        time.sleep(sleep)  # TODO: test it

    def main_loop(self, sleep=0.0):

        COUNT = 0
        while(COUNT < 100):

            sensor2 = self.get('SENSOR2')
            self.memory['SENSOR2'] = sensor2

            # do computation with tag values
            sensor1_int = int(self.memory['SENSOR1'])
            sensor2_int = int(self.memory['SENSOR2'])
            result = (sensor1_int + sensor2_int) / 2

            if result >= 2:
                self.memory['SENSOR2'] = str(result)
            elif result == 0:
                self.memory['SENSOR2'] = str(result + 1)
            else:
                pass

            # update state of the system
            self.memory['ACTUATOR2'] = '0'   # TODO: test it
            self.set('ACTUATOR2', self.memory['ACTUATOR2'])

            # network interaction
            # ADDR = IP[:port]

            # receive
            self.memory['SENSOR4'] = self.receive('SENSOR4', PLC2_ADDR)

            # send: TODO how to implement?
            # self.send('TAG4', PLC2_ADDR)

            if self.memory['SENSOR4'] <= 5:
                self.memory['ACTUATOR2'] = '1'   # TODO: test it
                self.set('ACTUATOR2', self.memory['ACTUATOR2'])
            else:
                pass

            # Sleep
            time.sleep(sleep)

            COUNT += 1


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc1 = ToyPLC1(
        name='plc1',
        state=DB_PATH,
        protocol='enip',
        memory=PLC1_TAG_DICT,
        disk=PLC1_TAG_DICT)

    plc1.boot(sleep=0.5)

    plc1.mainloop(sleep=0.5)
