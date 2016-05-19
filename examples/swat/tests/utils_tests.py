"""
swat utils tests.
"""

from examples.swat.utils import nxgraph_sub1, swat_logger
from nose.tools import eq_


def test_swat_logger():

    swat_logger.debug("TEST: debug message")
    swat_logger.info("TEST: info message")
    swat_logger.warning("TEST: warning message")
    swat_logger.error("TEST: error message")
    swat_logger.critical("TEST: critical message")


def test_nxgraph_sub1():

    graph = nxgraph_sub1(attacker=False)
    eq_(len(graph), 5)

    graph2 = nxgraph_sub1(attacker=True)
    eq_(len(graph2), 6)
