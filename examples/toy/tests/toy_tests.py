"""
toy_tests.py
"""

from minicps.state import SQLiteState
from examples.toy.plc1 import ToyPLC1
# from examples.toy.utils import PLC1_ADDR, PLC2_ADDR
from examples.toy.utils import PLC1_TAG_DICT, PLC2_TAG_DICT
from examples.toy.utils import PATH, NAME, SCHEMA, SCHEMA_INIT

STATE = {
    'name': NAME,
    'path': PATH
}


class TestToy():

    def test_ToyPLC1(self):

        SQLiteState._create(PATH, SCHEMA)
        SQLiteState._init(PATH, SCHEMA_INIT)

        plc1 = ToyPLC1(
            name='plc1',
            state=STATE,
            protocol='enip',
            memory=PLC1_TAG_DICT,
            disk=PLC1_TAG_DICT)

        SQLiteState._delete(PATH)
