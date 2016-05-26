"""
mcps.py

Main module for functional classes.

MiniCPS augments Mininet capabilities in the context of Cyber-Physical
Systems.
"""


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

        self.net.start()
        self.net.pingAll()
        self.net.stop()
