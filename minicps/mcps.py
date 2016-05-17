"""
mcps.py

Main module for functional classes.

MiniCPS augments Mininet capabilities in the context of Cyber-Physical
Systems.
"""

from mininet.cli import CLI


# MiniCPS has:
#     a _pid dict
#     a sdn_controller (what about external?)

# Mininet TCLink used by default to shape
# TODO: Mininet listenPort
class MiniCPS(object):

    """Main container used to run the simulation."""

    # TODO: group mininet stuff using an obj
    def __init__(self, name, net):
        """MiniCPS initialization steps:

        net object usually contains reference to:
            - the topology
            - the link shaping
            - the CPU allocation
            - the SDN controller
            - etc

        :name: CPS name
        :net: Mininet object
        """

        self.name = name
        self.net = net

        self._init_mininet()

    def _init_mininet(self):
        """Init mininet network."""

        # TODO: decide wheter to store it or not
        self._topo = self.net.topo
        # print 'DEBUG self._topo:', self._topo

        self.net.start()
        CLI(self.net)
        self.net.stop()
