"""
mcps.py

Main module for functional classes.

MiniCPS augments Mininet capabilities in the context of Cyber-Physical
Systems.
"""

from mininet.cli import CLI


# TODO: maybe return some pid
class MiniCPS(object):

    """Main container used to run the simulation."""

    # TODO: validate inputs

    def __init__(self, name, net):
        """MiniCPS initialization steps:

        net object usually contains reference to:
            - the topology
            - the link shaping
            - the CPU allocation
            - the [remote] SDN controller

        :name: CPS name
        :net: Mininet object
        """

        self.name = name
        self.net = net

        # self._topo = self.net.topo
        # print 'DEBUG self._topo:', self._topo

        # TODO: move to public API
        self.net.start()

        # run them as python modules
        # TODO

        CLI(self.net)

        self.net.stop()
