"""
toy_tests.py
"""

from nose.plugins.skip import SkipTest

from minicps.state import SQLiteState
from examples.toy.plc1 import ToyPLC1
from examples.toy.utils import toy_logger
# from examples.toy.utils import PLC1_ADDR, PLC2_ADDR
from examples.toy.utils import PLC1_TAG_DICT, PLC2_TAG_DICT
from examples.toy.utils import PATH, NAME, SCHEMA, SCHEMA_INIT

STATE = {
    'name': NAME,
    'path': PATH
}


def test_toy_logger():

    toy_logger.debug("TEST: debug message")
    toy_logger.info("TEST: info message")
    toy_logger.warning("TEST: warning message")
    toy_logger.error("TEST: error message")
    toy_logger.critical("TEST: critical message")


@SkipTest
class TestToy():

    def test_ToyPLC1(self):

        SQLiteState._create(PATH, SCHEMA)
        SQLiteState._init(PATH, SCHEMA_INIT)

        plc1 = ToyPLC1(
            name='plc1',
            state=STATE,
            protocol='enip',  # TODO: fix protocol once ready
            memory=PLC1_TAG_DICT,
            disk=PLC1_TAG_DICT)

        SQLiteState._delete(PATH)
