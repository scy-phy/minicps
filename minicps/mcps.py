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

    def __init__(self, name, net, nodes):
        """MiniCPS initialization steps:

        net object usually contains reference to:
            - the topology
            - the link shaping
            - the CPU allocation
            - the [remote] SDN controller

        Names in nodes tuple must match containers name of the net object.

        :name: CPS name
        :net: Mininet object
        :nodes: tuples of strings
        """

        self.name = name
        self.net = net
        self.nodes = nodes

        # self._topo = self.net.topo
        # print 'DEBUG self._topo:', self._topo

        # TODO: move to public API
        self.net.start()

        self._nodes = []
        # get container references
        for node in self.nodes:
            self._nodes.append(self.net.get(node))

        for _node in self._nodes:
            print _node.IP()

        # run them as python modules
        # TODO

        CLI(self.net)

        self.net.stop()
