"""
protocols_test.
"""

from minicps.protocols import Protocol, EnipProtocol

from nose.tools import eq_
from nose.plugins.skip import SkipTest

# TODO: still not spec of the dict
PROTOCOL = {
    'name': 'enip',
    'port': 4444,
    'mode': 1,
}

# TODO: add high level enip function tests
# import os


@SkipTest
def test_EnipProtocolClassMethods():

    pass


class TestProtocol():

    def test_init(self):

        enip = Protocol(
            protocol=PROTOCOL)

        eq_(enip._name, 'enip')
        eq_(enip._port, 4444)
        eq_(enip._mode, 1)


class TestEnipProtocol():

    def test_init(self):

        enip = EnipProtocol(
            protocol=PROTOCOL)

        eq_(enip._name, 'enip')
        eq_(enip._port, 4444)
        eq_(enip._mode, 1)
