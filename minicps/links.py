"""
Collection of Link subclasses to be used by MiniCPS.

Edge is the base link class, its subclasses represent a
particular link technology
e.g. 802.3 Ethernet, 802.11 Wifi
"""

class Edge(object):

    """Base Edge networkx -> mininet link object"""

    def __init__(self, id, bw, delay, loss=0, max_queue_size=1000, use_htb=True):
        """
        :name: edge unique id
        :bw: TODO
        :delay: TODO
        :loss: TODO
        :max_queue_size: TODO
        :use_htb: TODO

        """
        self.id = id
        self.bw = bw
        self.delay = delay
        self.loss = loss
        self.max_queue_size = max_queue_size
        self.use_htb = use_htb
    
    def get_params(self):
        """Wrapper around __dict__"""

        return self.__dict__


class EthLink(Edge):

    """EthLink"""


class WiFi(Edge):

    """EthLink"""
