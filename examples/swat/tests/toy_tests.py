"""
swat toy tests
"""

from examples.swat.toy.plc1 import ToyPLC1


def test_ToyPLC1():

    PLC1_TAG_DICT = {
        'SENSOR1' '0',
        'SENSOR2' '0.0',
        'SENSOR3' '0',  # interlock with PLC2
        'ACTUATOR1' '1',  # 0 means OFF and 1 means ON
        'ACTUATOR2' '0',
    }

    plc1 = ToyPLC1(
        name='plc1',
        state='sqlite',
        protocol='enip',
        memory=PLC1_TAG_DICT,
        disk=PLC1_TAG_DICT)

    plc1.set('SENSOR1' '2')
    plc1.get('SENSOR2')
