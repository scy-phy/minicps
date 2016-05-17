"""
toy_tests.py
"""

from examples.toy.plc1 import ToyPLC1
from examples.toy.utils import DB_PATH, PLC1_ADDR, PLC2_ADDR
from examples.toy.utils import PLC1_TAG_DICT, PLC2_TAG_DICT


def test_ToyPLC1():

    plc1 = ToyPLC1(
        name='plc1',
        state=DB_PATH,
        protocol='enip',
        memory=PLC1_TAG_DICT,
        disk=PLC1_TAG_DICT)

    plc1.set('SENSOR1' '2')
    plc1.get('SENSOR2')
