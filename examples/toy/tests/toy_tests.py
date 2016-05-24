"""
toy_tests.py
"""

import os

from nose.plugins.skip import SkipTest

from minicps.state import SQLiteState
from examples.toy.plc1 import ToyPLC1
from examples.toy.utils import toy_logger
# from examples.toy.utils import PLC1_ADDR, PLC2_ADDR
from examples.toy.utils import PLC1_DATA, PLC2_DATA, PLC1_PROTOCOL
from examples.toy.utils import STATE, PATH, SCHEMA, SCHEMA_INIT


@SkipTest
def test_toy_logger():

    toy_logger.debug("TEST: debug message")
    toy_logger.info("TEST: info message")
    toy_logger.warning("TEST: warning message")
    toy_logger.error("TEST: error message")
    toy_logger.critical("TEST: critical message")


class TestToy():

    def test_ToyPLC1(self):

        try:
            os.remove(PATH)
        except OSError:
            pass

        finally:
            SQLiteState._create(PATH, SCHEMA)
            SQLiteState._init(PATH, SCHEMA_INIT)

            plc1 = ToyPLC1(
                name='plc1',
                state=STATE,
                protocol=PLC1_PROTOCOL,
                memory=PLC1_DATA,
                disk=PLC1_DATA)

            SQLiteState._delete(PATH)
