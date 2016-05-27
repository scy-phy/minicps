"""
toy_tests.py
"""


from nose.plugins.skip import SkipTest

from minicps.state import SQLiteState
from plc1 import ToyPLC1
from utils import toy_logger
# from utils import PLC1_ADDR, PLC2_ADDR
from utils import PLC1_DATA, PLC2_DATA, PLC1_PROTOCOL, PLC1_TAGS
from utils import STATE, PATH, SCHEMA, SCHEMA_INIT

import os


@SkipTest
def test_toy_logger():

    toy_logger.debug("TEST: debug message")
    toy_logger.info("TEST: info message")
    toy_logger.warning("TEST: warning message")
    toy_logger.error("TEST: error message")
    toy_logger.critical("TEST: critical message")


class TestToy():

    def test_ToyPLC1(self):

        plc1_server = {
            'address': 'localhost',
            'tags': PLC1_TAGS
        }
        plc1_protocol = {
            'name': 'enip',
            'mode': 1,
            'server': plc1_server
        }

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
                protocol=plc1_protocol,
                memory=PLC1_DATA,
                disk=PLC1_DATA)

            # SQLiteState._delete(PATH)
