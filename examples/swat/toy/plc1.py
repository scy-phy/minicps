import time

# PLC is a Device Obj

# Device attributes
#     has a name string -> used also by Topo
#     has a protocol -> network emulation
#     has a state -> PHY layer API backend
#     has a disk dict -> client
#     has a memory dict -> client

# Device methods
#     has a __init__: init memory and disk (eg: PLC boot process)
#     may have control capability: set and get a state value
#     may have monitoring capability: get a state value
#     may have networking capability: send and recieve a packet
#     may have a logic: compute over values or simply read and send


# PLC extra methods
#     has a network unit: send, receive
#     has a control unit: set, get
#     has a pre_loop: single state interaction
#     has a main_loop: repetitive state interaction

# PLC extra attributes


# tags are strings key-val pairs

# TODO: self.get is different from write to PLC memory ?

from minicps.devices import PLC

# from minicps.example.swat.utils import PLC1_TAG_DICT
PLC1_TAG_DICT = {
    'SENSOR1' '1',
    'SENSOR2' '20.0',
    'SENSOR3' '5',
    'ACTUATOR1' '1',
    'ACTUATOR2' '0',
}


class ToyPLC1(PLC):

    def pre_loop(sleep=0.4):

        # sensor reading
        sensor1 = self.get('SENSOR1')  # TODO: test it

        # update PLC memory
        self.memory('SENSOR1') = sensor1

        if sensor1 == '1':
            self.memory('TAG3') = '0'
            # ACTUATOR1 ON
            self.set('ACTUATOR1', '1')  # TODO: test it
        else:
            pass

        # wait for the other plcs
        time.sleep(sleep)  # TODO: test it

    def main_loop(sleep=0.0):

        while(time.time() - start_time < TIMEOUT):

            tag2 = self.get('TAG2')
            self.memory('TAG2') = tag2

            # do computation with tag values
            tag1_int = int(self.memory('TAG1'))
            tag2_int = int(self.memory('TAG2'))
            result = (tag1_int + tag2_int) / 2

            if result >= 2:
                self.memory('TAG2') = str(result)
            elif result == 0:
                self.memory('TAG2') = str(result + 1)
            else:
                pass

            # update state of the system
            self.set('TAG3', self.memory('TAG2'))

            # network interaction
            # ADDR = IP[:port]

            # receive
            self.memory('TAG4') = self.receive('TAG4', PLC2_ADDR)

            # send: TODO how to implement?
            self.send('TAG4', PLC2_ADDR)

            result = float(self.memory('TAG4'))

            if result <= 22.5:
                self.set('TAG5', '2')
            else:
                pass

            # Sleep
            time.sleep(sleep)


if __name__ == "__main__":

    # notice that memory init is different form disk init
    plc = PLC(
        name='plc1',
        state='sqlite',
        protocol='enip',
        memory={
            'TAG1' '1',
            'TAG2' '2',
            'TAG3' '3',
        },
        disk=PLC1_TAG_DICT)

    plc.boot(sleep=2)

    plc.mainloop(sleep=1)
