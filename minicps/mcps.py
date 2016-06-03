"""
MiniCPS is a container class, you can subclass it with a specialized version
targeted for your CPS.

E.g., ``MyCPS(MiniCPS)`` once constructed runs an interactive simulation where
each PLC device also run a webserver and the SCADA runs an FTP server.
"""


class MiniCPS(object):

    """Main container used to run the simulation."""

    # TODO: validate inputs

    def __init__(self, name, net):
        """MiniCPS initialization steps:

        :param str name: CPS name
        :param Mininet net: Mininet object

        ``net`` object usually contains reference to:
            - the topology
            - the link shaping
            - the CPU allocation
            - the [remote] SDN controller
        """

        self.name = name
        self.net = net

        self.net.start()
        self.net.pingAll()
        self.net.stop()
