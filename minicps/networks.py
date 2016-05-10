"""
MiniCPS networks module

It contains data object used my Mininet to build the topology.

It contains data object used to specify topologies as graph files.
"""


# graph
class Edge(object):

    """Base class used to model links as edges in a graph"""

    def __init__(
            self, id, bandwidth, delay, 
            loss=0, max_queue_size=1000, use_htb=True):
        """
        :id: edge unique id
        :bandwidth: TODO
        :delay: TODO
        :loss: TODO
        :max_queue_size: TODO
        :use_htb: TODO
        """
        self.id = id
        self.bandwidth = bandwidth
        self.delay = delay
        self.loss = loss
        self.max_queue_size = max_queue_size
        self.use_htb = use_htb

    def get_params(self):
        """Wrapper around __dict__"""

        return self.__dict__


class EthLink(Edge):

    """EthLink"""
    pass


class WiFi(Edge):

    """EthLink"""
    pass
