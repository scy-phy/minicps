"""
swat toy tests
"""

from examples.toy.plc1 import ToyPLC1

DB_PATH = 'examples/toy/db.sqlite'

PLC1_ADDR = '10.0.0.1'
PLC2_ADDR = '10.0.0.2'

PLC1_TAG_DICT = {
    'SENSOR1' '0',
    'SENSOR2' '0.0',
    'SENSOR3' '0',  # interlock with PLC2
    'ACTUATOR1' '1',  # 0 means OFF and 1 means ON
    'ACTUATOR2' '0',
}

PLC2_TAG_DICT = {
    'SENSOR3' '0',  # interlock with PLC1
}


def test_ToyPLC1():

    plc1 = ToyPLC1(
        name='plc1',
        state=DB_PATH,
        protocol='enip',
        memory=PLC1_TAG_DICT,
        disk=PLC1_TAG_DICT)

    plc1.set('SENSOR1' '2')
    plc1.get('SENSOR2')
