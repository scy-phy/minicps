"""
Collection of Link subclasses to be used by MiniCPS.
"""

class Edge(object):

    """
    Base networkx -> mininet link object
    
    """

    def __init__(self, bw, delay, loss=0, max_queue_size=1000, use_htb=True):
        """

        :bw: TODO
        :delay: TODO
        :loss: TODO
        :max_queue_size: TODO
        :use_htb: TODO

        """
        self.opts = {
            'bw': bw,
            'delay': delay,
            'loss': loss,
            'max_queue_size': max_queue_size,
            'use_htb': use_htb,
        }


class EthLink(Edge):

    """EthLink"""
