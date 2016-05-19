#!/usr/bin/env python2

from twisted.internet import reactor
from pymodbus.client.async import ModbusClientFactory


def process():
    factory = reactor.connectTCP(
        "localhost", 502,
        ModbusClientFactory())
    reactor.stop()

if __name__ == "__main__":
    reactor.callLater(1, process)
    reactor.run()
