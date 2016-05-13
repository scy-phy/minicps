"""
swat utils tests.
"""

from examples.swat.utils import nxgraph_sub1
from nose.tools import eq_


def test_nxgraph_sub1():

    graph = nxgraph_sub1(attacker=False)
    eq_(len(graph), 5)

    graph2 = nxgraph_sub1(attacker=True)
    eq_(len(graph2), 6)
